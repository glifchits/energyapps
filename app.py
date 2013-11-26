
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
    app.logger.debug( request.args )
    app.logger.debug( request.args.get('state') )
    app.logger.debug( request.args.get('code') )

    params = {
        'grant_type': request.args.get('code'),
        'code': request.args.get('code'),
        'redirect_uri': config.GET_TOKEN_URL
    }
    from base64 import b64encode
    auth_string = '%s%s' % (config.CLIENT_ID, config.CLIENT_SECRET)
    auth_b64 = b64encode(auth_string)
    headers = {
        'Authorization' : 'Basic %s' % auth_b64
    }
    r = requests.post(config.TOKEN_URL, data=params, headers=headers)

    return 'hi'

@app.route('/token')
def get_token():

    return 'hi'

if __name__ == '__main__':
    app.run()
