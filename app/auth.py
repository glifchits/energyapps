
from flask import redirect, url_for, render_template, session, request, flash
from flask import Blueprint, current_app as app

from schema import *

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        flash("Success!")
        return redirect(url_for('home'))

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash('Success!')
        return redirect(url_for('home'))

    return render_template('register.html')
