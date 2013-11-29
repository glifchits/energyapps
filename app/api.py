
from flask import redirect, url_for, render_template, session, request
from flask import Blueprint, current_app as app

import requests
from base64 import b64encode

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
    return redirect(url_for('index'))


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
    return r.text


@api.route('/eui')
def get_eui():
    params = {
        'start' : 1380600000,
        'duration' : 1296000
    }
    url = apipt.GET_EUI + '?' + urllib.urlencode(params)
    app.logger.debug('getting url %s' % url)
    r = requests.get(url, headers=bearer(session.get('access_token')),
            verify=False)

    if r.text:
        username = "%d %s" % (time.time(), session.get('access_token')[:10])
        f = open('/Users/glifchits/Development/energyapi/data/%s.xml' % \
                username, 'w')
        f.write(r.text)
        f.close()

    return r.text


