'''
    flaskext.bcrypt
    ---------------
    
    A Flask extension providing bcrypt hasing and comparison facilities.
    
    :copyright: (c) 2011 by Max Countryman.
    :license: BSD, see LICENSE for more details.
'''

from __future__ import absolute_import

__version__ = '0.5.2'

try:
    from pybcrypt import bcrypt
except ImportError, e:
    print 'py-bcrypt is required to use Flask-Bcrypt'
    raise e


def generate_password_hash(password, rounds=None):
    '''This helper function wraps the eponymous method of :class:`Bcrypt`. It 
    is intended to be used as a helper function at the expense of the 
    configuration variable provided when passing back the app object. In other 
    words this shortcut does not make use of the app object at all.
    
    To this this function, simple import it from the module and use it in a 
    similar fashion as the method would be used. Here is a quick example::
        
        from flask.ext.bcrypt import generate_password_hash
        pw_hash = generate_password_hash('hunter2', 10)
    
    :param password: The password to be hashed.
    :param rounds: The optional number of rounds.
    '''
    return Bcrypt().generate_password_hash(password, rounds)


def check_password_hash(pw_hash, password):
    '''This helper function wraps the eponymous method of :class:`Bcrypt.` It 
    is intended to be used as a helper function at the expense of the 
    configuration variable provided when passing back the app object. In other 
    words this shortcut does not make use of the app object at all.
    
    To this this function, simple import it from the module and use it in a 
    similar fashion as the method would be used. Here is a quick example::
        
        from flask.ext.bcrypt import check_password_hash
        check_password_hash(pw_hash, 'hunter2') # returns True
    
    :param pw_hash: The hash to be compared against.
    :param password: The password to compare.
    '''
    return Bcrypt().check_password_hash(pw_hash, password)


def _constant_time_compare(val1, val2):
    '''Returns True if the two strings are equal, False otherwise.
    
    The time taken is independent of the number of characters that match.
    '''
    
    if len(val1) != len(val2):
        return False
    
    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    
    return result == 0


class Bcrypt(object):
    '''Bcrypt class container for password hashing and checking logic using 
    bcrypt, of course. This class may be used to intialize your Flask app 
    object. The purpose is to provide a simple interface for overriding 
    Werkzeug's built-in password hashing utilities.
    
    Although such methods are not actually overriden, the API is intentionally 
    made similar so that existing applications which make use of the previous 
    hashing functions might be easily adapted to the stronger facility of 
    bcrypt.
    
    To get started you will wrap your application's app object something like 
    this::
        
        app = Flask(__name__)
        bcrypt = Bcrypt(app)
    
    Now the two primary utility methods are exposed via this object, `bcrypt`.
    So in the context of the application, important data, such as passwords, 
    could be hashed using this syntax::
        
        password = 'hunter2'
        pw_hash = bcrypt.generate_password_hash(password)
    
    Once hashed, the value is irreversible. However in the case of validating 
    logins a simple hashing of candidate password and subsequent comparison. 
    Importantly a comparison should be done in constant time. This helps 
    prevent timing attacks. A simple utility method is provided for this::
        
        candidate = 'secret'
        bcrypt.check_password_hash(pw_hash, candidate)
    
    If both the candidate and the existing password hash are a match 
    `check_password_hash` returns True. Otherwise, it returns False.
        
    .. admonition:: Namespacing Issues 
        
        It's worth noting that if you use the format, `bcrypt = Bcrypt(app)` 
        you are effectively overriding the bcrypt module. Though it's unlikely 
        you would need to access the module outside of the scope of the 
        extension be aware that it's overriden.
        
        Alternatively consider using a different name, such as `flask_bcrypt 
        = Bcrypt(app)` to prevent naming collisions.
    
    Additionally a configuration value for `BCRYPT_LOG_ROUNDS` may be set in 
    the configuration of the Flask app. If none is provided this will 
    internally be assigned to 12. (This value is used in determining the 
    complexity of the encryption, see bcrypt for more details.)
    
    :param app: The Flask application object. Defaults to None.
    '''
    
    _log_rounds = 12
    
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        '''Initalizes the application with the extension.
        
        :param app: The Flask application object.
        '''
        self.app = app
        self._log_rounds = app.config.get('BCRYPT_LOG_ROUNDS', 12)
    
    def generate_password_hash(self, password, rounds=None):
        '''Generates a password hash using bcrypt. Specifying `rounds` 
        sets the log_rounds parameter of `bcrypt.gensalt()` which determines 
        the complexity of the salt. 12 is the default value.
        
        Example usage of :class:`generate_password_hash` might look something 
        like this::
            
            pw_hash = bcrypt.generate_password_hash('secret', 10)
        
        :param password: The password to be hashed.
        :param rounds: The optional number of rounds.
        '''
        
        if not password:
            raise ValueError('Password must be non-empty.')
        
        if rounds is None:
            rounds = self._log_rounds
        if isinstance(password, unicode):
            password = password.encode('u8')
        password = str(password)
        return bcrypt.hashpw(password, bcrypt.gensalt(rounds))
    
    def check_password_hash(self, pw_hash, password):
        '''Tests a password hash against a candidate password. The candidate 
        password is first hashed and then subsequently compared in constant 
        time to the existing hash. This will either return `True` or `False`.
        
        Example usage of :class:`check_password_hash` would look something 
        like this::
            
            pw_hash = bcrypt.generate_password_hash('secret', 10)
            bcrypt.check_password_hash(pw_hash, 'secret') # returns True
        
        :param pw_hash: The hash to be compared against.
        :param password: The password to compare.
        '''
        if isinstance(password, unicode):
            password = password.encode('u8')
        password = str(password)
        return _constant_time_compare(bcrypt.hashpw(password, pw_hash), pw_hash)
