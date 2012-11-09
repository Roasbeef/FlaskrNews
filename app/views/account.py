from flask import (Blueprint, url_for, render_template,
                   request, redirect, session, jsonify)

from ..models.user import User

from pybcrypt import bcrypt

mod = Blueprint('account', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    error = False

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query(User.username == username).get()
        if user is not None and bcrypt.hashpw(password, user.pwhash) == user.pwhash:
            session['username'] = username
            return redirect(url_for('frontend.index'))
        else:
            error = True

    return render_template('login.html', error=error)


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
