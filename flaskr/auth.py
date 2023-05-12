import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db, close_db, init_db_command
from flaskr.models import User


bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user is not None:
                error = f"User {username} is already registered."
            else:
                new_user = User(username=username, password=generate_password_hash(password))
                db.add(new_user)
                db.commit()
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = User.query.filter_by(username = username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id #cookie 
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    '''Check if user id is stored in a session'''
    user_id = session.get('user_id') # stored in session on the login
    db = get_db()
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id = user_id).first()

@bp.route('/logout')
def logout():
    '''define logout logic'''
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    '''Check if user is logged in for a certain view'''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view