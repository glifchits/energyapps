from flask import render_template, g, session, redirect, url_for
from flask.ext.login import current_user

from app import app
from app import config

from app.api import api
app.register_blueprint(api)
from app.auth import auth
app.register_blueprint(auth)
from app.data import data
app.register_blueprint(data)
from app.charts import charts
app.register_blueprint(charts)


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated() and 'access_token' not in session:
        access_token = g.user.access_token
        if access_token:
            session['access_token'] = access_token
            app.logger.info('added access token (user %s)' % g.user)


@app.route('/')
def home():
    if g.user.get_id():
        if g.user.has_eui():
            app.logger.debug('user is active, showing dashboard')
            return render_template('dashboard.html')
        app.logger.debug('user is logged in but inactive, go to get eui')
        return redirect(url_for('auth.eui_agreement'))
    app.logger.debug('not logged in')
    return render_template('landing.html')


if __name__ == '__main__':
    app.run()
