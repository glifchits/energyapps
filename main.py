from flask import render_template, g, session, redirect, url_for
from flask.ext.login import current_user

from app import app

from app.api import api
app.register_blueprint(api)
from app.auth import auth
app.register_blueprint(auth)
from app.data import data
app.register_blueprint(data)


@app.before_request
def before_request():
    g.appname = 'mPowr'
    g.user = current_user
    if g.user.is_authenticated() and 'access_token' not in session:
        access_token = g.user.access_token
        if access_token:
            session['access_token'] = access_token
            app.logger.info('added access token (user %s)' % g.user)


@app.route('/')
def home():
    if g.user.get_id():
        if g.user.agreed_to_eui():
            app.logger.debug('user %s is active' % g.user.get_id())
            if g.user.access_token is None:
                app.logger.debug('user has no access token, to data custodian')
                return render_template('redirect.html', url=url_for('api.to_data_custodian'))

            if g.user.has_eui():
                app.logger.debug('user has data, showing dashboard')
                return render_template('dashboard.html')

            else:
                app.logger.debug('user has no eui data... going to wait page')
                return redirect(url_for("auth.get_eui"))

        app.logger.debug('user is logged in but inactive, go to get eui')
        return redirect(url_for('auth.eui_agreement'))

    app.logger.debug('not logged in')
    return render_template('landing.html')


@app.route('/favicon.ico')
def favicon():
    import os
    cwd = os.getcwd()
    path = 'app/static/img/favicon.ico'
    return redirect(url_for('static', filename='img/favicon.ico'))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = 5000
    app.run(port = int( port ))
