from functools import wraps
from flask import (session, request, redirect, url_for, abort,
                   flash)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            flash('You must be logged in to do that', category='error')
            return redirect(url_for('account.login', after=request.url_root))
        return f(*args, **kwargs)
    return decorated_function


def get_or_404(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        obj = f(*args, **kwargs)
        if obj is None:
            abort(404)
        else:
            return obj
    return decorated_function
