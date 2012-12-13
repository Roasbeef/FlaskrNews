from flask import (Blueprint, url_for, render_template,
                   request, redirect, session, jsonify,
                   flash)

from ..models.user import User

from pybcrypt import bcrypt

mod = Blueprint('account', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    error = False
    next_url = request.args.get('after') if request.args.get('after') is not None else url_for('frontend.index')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query(User.username == username).get()
        if user is not None and bcrypt.hashpw(password, user.pwhash) == user.pwhash:
            session['username'] = username
            next_url = request.args.get('after')
            flash('Successfully logged in!', category='success')
            return redirect(next_url)
        else:
            error = True

    return render_template('login.html', error=error, next_url=next_url)


@mod.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pwhash = bcrypt.hashpw(password, bcrypt.gensalt())
        u = User()
        u.register(username, pwhash)
        session['username'] = username
        return redirect(url_for('frontend.index'))

    else:
        return render_template('register.html')


@mod.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully', category='success')
    return redirect(url_for('frontend.index'))


@mod.route('/_check_username')
def check_username():
    pending_username = request.args.get('username')
    is_taken = User.query(User.username == pending_username).get()

    if is_taken is None:
        response = "all good"
    else:
        response = "taken"

    return jsonify(result=response)
