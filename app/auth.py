
from flask import redirect, url_for, render_template, session, request, flash, g
from flask import Blueprint, current_app as app
from flask.ext.login import login_user, logout_user, login_required
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

from functools import wraps

from app import lm
from __init__ import db
import schema
from constants import *

auth = Blueprint('auth', __name__)


@lm.user_loader
def load_user(id):
    return schema.User.query.get(int(id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    class LoginForm(Form):
        email = TextField('email', validators=[DataRequired()])
        password = PasswordField('password')

    form = LoginForm()
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

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@auth.route('/agreement', methods=['GET', 'POST'])
def eui_agreement():
    if request.method == 'POST':
        print request.form
        agree = request.form.get('agree')
        if agree:
            g.user.eui_agreed = True
            app.logger.debug('agreed to eui, committing')
            print db.session.new
            print db.session.dirty
            db.session.commit()
            return redirect(url_for('home'))
        g.user.eui_agreed = False
        app.logger.debug('disagreed to eui, committing')
        db.session.commit()
        flash((CSS_ERR, 'You chose not to agree'))
        return redirect(url_for('auth.logout'))
    return render_template('auth/agree_eui.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db.create_all()
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = schema.User()
            user.name = name
            user.email = email
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash((CSS_SUCC, 'Success!'))
            # log in the user
            login_user(user, remember = True)
        except Exception as e:
            flash((CSS_ERR, str(e)))

        return redirect(url_for('home'))

    return render_template('auth/register.html')


@auth.route('/getting_eui')
@login_required
def get_eui():
    return render_template('auth/wait_for_eui.html')


@auth.route('/profile')
@login_required
def edit_profile():
    goals = schema.Goal.query.all()
    goal_scopes = [r[0] for r in db.engine.execute("select scope from scope;")]
    return render_template('auth/edit_profile.html', goals=goals,
            enumerate=enumerate, goal_scopes=goal_scopes)


@auth.route('/profile/edit', methods=['POST'])
@login_required
def change_userinfo():
    name = request.form.get('name')
    email = request.form.get('email')

    user = g.user
    user.name = name
    user.email = email
    db.session.commit()

    app.logger.debug('got args, name: %s email: %s' % (name, email))
    return redirect(url_for('.edit_profile'))
