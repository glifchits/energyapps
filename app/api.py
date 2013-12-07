
from flask import redirect, url_for, render_template, session, request, abort
from flask import Blueprint, current_app as app
from flask.ext.login import login_required

import requests
import urllib
import time
from base64 import b64encode

import parsedata as data
import config
import api_points as apipt

api = Blueprint('api', __name__)

def auth_header():
    auth_string = '%s:%s' % (config.CLIENT_ID, config.CLIENT_SECRET)
    auth_b64 = b64encode(auth_string)
    return {
        'Authorization' : 'Basic %s' % auth_b64
    }

def bearer(access_code):
    return {
        'Authorization': 'Bearer %s' % access_code
    }


@api.route('/to_data_custodian')
@login_required
def to_data_custodian():
    return redirect(config.AUTH_URL)


@api.route('/auth')
def auth():
    app.logger.debug( '/auth GET %s' % request.args )
    params = {
        'grant_type': 'authorization_code', #request.args.get('code'),
        'code': request.args.get('code'),
        'redirect_uri': config.REDIRECT_URI
    }
    r = requests.post(config.TOKEN_URL, data=params, headers=auth_header(),
            verify=False)
    app.logger.debug(r.text)
    request_data = r.json()
    access_token = request_data.get('access_token')
    token_type = request_data.get('token_type')
    refresh_token = request_data.get('refresh_token')
    expires_in = request_data.get('expires_in')

    if access_token is None:
        raise ValueError("bad request")

    app.logger.debug(access_token)
    session['access_token'] = request_data.get('access_token')
    return redirect(url_for('home'))


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
        abort(r.status_code)
    return r.text


@api.route('/eui')
@login_required
def get_eui():
    params = {
        'start' : 1380600000,
        'duration' : 1296000
    }
    url = apipt.GET_EUI + '?' + urllib.urlencode(params)
    app.logger.debug('getting url %s' % url)

    r = requests.get(url, headers=bearer(session.get('access_token')),
            verify=False)

    if r.status_code != 200:
        abort(r.status_code)

    if r.text:
        data.process_data(r.text)
    else:
        return 'not logged in with greenbutton'
    return r.text


