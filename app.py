# local package imports
from flask import Flask, redirect, url_for, render_template, session, \
        request, g
import requests
# stdlib imports
import os
import urllib
from base64 import b64encode
# my app imports
import config

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True


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


@app.route('/')
def index():
    return render_template('index.html', auth_url = config.AUTH_URL)

@app.route('/auth')
def auth():
    app.logger.debug( '/auth GET %s' % request.args )
    params = {
        'grant_type': 'authorization_code', #request.args.get('code'),
        'code': request.args.get('code'),
        'redirect_uri': config.REDIRECT_URI
    }
    r = requests.post(config.TOKEN_URL, data=params, headers=auth_header(), \
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


@app.route('/read/service_status')
def read_service_status():
    url = 'https://greenbutton.affsys.com/ldc/api/v1/ReadServiceStatus'
    r = requests.get(url, headers=auth_header(), verify=False)
    app.logger.debug(r.text)
    return r.text


@app.route('/read/auth_status')
def read_auth_status():
    url = 'https://greenbutton.affsys.com/ldc/api/v1/ReadAuthorizationStatus'
    r = requests.get(url, headers=bearer(session.get('access_token')), \
            verify=False)
    return r.text


@app.route('/eui')
def get_eui():
    url = 'https://greenbutton.affsys.com/ldc/api/v1/UsagePoint?'
    params = {
        'start' : 1380600000,
        'duration' : 1296000
    }
    url += urllib.urlencode(params)
    app.logger.debug('getting url %s' % url)
    r = requests.get(url, headers=bearer(session.get('access_token')), \
            verify=False)
    return r.text


if __name__ == '__main__':
    app.run()
