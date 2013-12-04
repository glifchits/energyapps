
from flask import redirect, url_for, render_template, session, request, flash, g
from flask import Blueprint, current_app as app
from flask.ext.login import login_user, logout_user, login_required

from functools import wraps

from app import db, lm
import schema
from constants import *

auth = Blueprint('auth', __name__)


db.create_all()
connection = db.session()
connection.rollback()


@lm.user_loader
def load_user(id):
    return schema.User.query.get(int(id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = True

        user = schema.User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            app.logger.debug("logging in as %s" % user)
            login_user(user, remember = remember_me)
            flash((CSS_SUCC, "Success!"))
            return redirect(request.args.get('next') or url_for('home'))

        flash((CSS_ERR, "Username or password incorrect"))
        return redirect(url_for('.login'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


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
