
from flask import Flask, redirect, url_for, render_template, session, \
        request, g
import requests
import config

app = Flask(__name__)
app.debug = True

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
    from base64 import b64encode
    auth_string = '%s:%s' % (config.CLIENT_ID, config.CLIENT_SECRET)
    auth_b64 = b64encode(auth_string)
    headers = {
        'Authorization' : 'Basic %s' % auth_b64
    }
    r = requests.post(config.TOKEN_URL, data=params, headers=headers, \
            verify=False)
    access_token = r.json().get('access_token')
    if access_token is None:
        raise ValueError("bad request")
    app.logger.debug(access_token)
    session['access_token'] = access_token
    return render_template('basic.html')


if __name__ == '__main__':
    app.run()
