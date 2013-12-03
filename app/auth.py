
from flask import redirect, url_for, render_template, session, request, flash,\
        g
from flask import Blueprint, current_app as app

from functools import wraps

from __init__ import db
import schema
from constants import *

auth = Blueprint('auth', __name__)


db.create_all()
connection = db.session()
connection.rollback()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            flash((CSS_ERR, "You must login before you can do that!"))
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = schema.User.query.filter_by(email=email).first()
        if user.check_password(password):
            app.logger.debug("logging in as %s" % user)
            g.user = user
            app.logger.debug('g.user is %s' % g.user)
            flash((CSS_SUCC, "Success!"))
            return redirect(url_for('home'))

        flash((CSS_ERR, "Username or password incorrect"))
        return redirect(url_for('home'))

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = schema.User()
            user.name = name
            user.email = email
            user.set_password(password)
            connection.add(user)
            connection.commit()
            flash((CSS_SUCC, 'Success!'))
        except Exception as e:
            flash((CSS_ERR, str(e)))

        return redirect(url_for('home'))

    return render_template('register.html')
