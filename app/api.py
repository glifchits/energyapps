
from flask import redirect, url_for, render_template, session, request, abort,\
        g
from flask import Blueprint, current_app as app
from flask.ext.login import login_required

from __init__ import db

import requests
import urllib
import time
from base64 import b64encode
from xml.etree import ElementTree

import parsedata as data
import api_points as apipt
import secret_config as secret
from config import exported as config

api = Blueprint('api', __name__)

def auth_header():
    auth_string = '%s:%s' % (secret.CLIENT_ID, secret.CLIENT_SECRET)
    auth_b64 = b64encode(auth_string)
    return { 'Authorization' : 'Basic %s' % auth_b64 }

def bearer(access_code):
    return { 'Authorization': 'Bearer %s' % access_code }


@api.route('/to_data_custodian')
@login_required
def to_data_custodian():
    return redirect(apipt.AUTH_URL)


@api.route('/auth')
@login_required
def auth():
    app.logger.debug( '/auth GET %s' % request.args )
    params = {
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
        'redirect_uri': config.REDIRECT_URI
    }
    r = requests.post(apipt.TOKEN_URL, data=params, headers=auth_header(),
            verify=False)
    app.logger.debug(r.text)
    if not r.text:
        # the user clicked "Cancel" at the data custodian's end
        abort(401)
    request_data = r.json()
    access_token = request_data.get('access_token')
    token_type = request_data.get('token_type')
    refresh_token = request_data.get('refresh_token')
    expires_in = request_data.get('expires_in')

    if access_token is None:
        raise ValueError("bad request")

    app.logger.debug(access_token)
    session['access_token'] = access_token

    user = g.user
    app.logger.debug(user)
    user.update_access_token(access_token)

    db.session.commit()

    return redirect(url_for('home'))


@api.route('/subscribe')
def create_subscription():
    params = {
        'frequency': 'daily',
        'type': 'data'
    }
    r = requests.post(apipt.CREATE_SUBSCRIPTION,
            params=params,
            headers=bearer(session.get('access_token')),
            verify=False)
    print r.text
    if r.status_code != 200:
        app.logger.debug("failed to create subscription")
        abort(r.status_code)
    return r.text


@api.route('/read/service_status')
def read_service_status():
    r = requests.get(apipt.SERVICE_STATUS,
            headers=auth_header(), verify=False)
    app.logger.debug(r.text)
    return r.text


@api.route('/read/auth_status')
def read_auth_status():
    r = requests.get(apipt.AUTH_STATUS,
            headers=bearer(session.get('access_token')), verify=False)
    if r.status_code != 200:
        app.logger.debug("failed to read auth status")
        app.logger.debug("got this request text:\n%s" % r.text)
        abort(r.status_code)
    return r.text


@api.route('/eui')
@login_required
def get_eui():
    '''
    Route which controls downloading a users energy usage information
    '''
    '''
    # code for getting eui from a file temporarily
    with open("app/testdata/E1 Small pge_electric_interval_data_2011-04-04_to_2012-05-04 zipcode cost.xml") as f:
        app.logger.debug('processing file')
        data.process_data(f.read())
        app.logger.debug('done')
        return 'success'
    '''
    r = requests.get(
            apipt.AUTH_STATUS,
            headers = bearer(session.get('access_token')),
            verify=False)
    if r.status_code != 200:
        app.logger.debug("failed to read auth status before getting EUI")
        abort(r.status_code)
    if not r.text:
        abort(401)
    root = ElementTree.fromstring(r.text)
    current_status, expiry, scope = root.getchildren()
    app.logger.debug(scope.text)

    scopedata = scope.text.split(' ')
    app.logger.debug(scopedata)

    auth_params = dict([param.split('=') for param in scopedata[1:]])
    app.logger.debug(auth_params)

    # the maximum possible duration in seconds (2 years for now)
    max_duration = int(auth_params['HistoryLength']) * 60 * 60 * 24
    # the default start time (now - max_duration)
    start_time = int(time.time()) - max_duration - 60 # 1 min offset

    # the start time to use for the request
    start = request.args.get('start') or start_time

    # number of seconds between now and the start time
    diff_duration = int(time.time()) - int(start)

    # duration will be specified or the minimum between difference and max
    duration = request.args.get('duration') or min(diff_duration, max_duration)

    app.logger.debug("start, duration are %s %s" % (start, duration))

    params = {
        'start' : start, #1380600000,
        'duration' : duration #1296000
    }
    url = apipt.GET_EUI + '?' + urllib.urlencode(params)
    app.logger.debug('getting url %s' % url)

    r = requests.get(url,
            headers=bearer(session.get('access_token')),
            verify=False)

    if r.status_code != 200:
        app.logger.debug("failed to get EUI from url\n%s\n%s\n%s\n%s" % \
                (r, r.url, r.text, r.headers))
        abort(r.status_code)

    if r.text:
        app.logger.debug('processing EUI data now')
        data.process_data(r.text)
    else:
        abort(401)
    return 'success'


