from flask import Flask, render_template, g, session
from views import frontend, account, post, comment
from models.user import User
import settings


def create_app():
    """
    Create your application. Files outside the app directory can import
    this function and use it to recreate your application -- both
    bootstrap.py and the `tests` directory do this.
    """
    app = Flask(__name__)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.before_request
    def load_user():
        if session.get('username') is not None:
            user = User.query(User.username == session.get('username')).get()
            g.user = user

    app.config.from_object(settings)
    app.register_blueprint(frontend.mod)
    app.register_blueprint(account.mod)
    app.register_blueprint(post.mod)
    app.register_blueprint(comment.mod)
    return app
