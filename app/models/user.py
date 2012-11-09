from google.appengine.ext import ndb


class User(ndb.Model):
    username = ndb.StringProperty()
    pwhash = ndb.StringProperty()
    karma = ndb.IntegerProperty()
    date_joined = ndb.DateTimeProperty(auto_now_add=True)

    def register(self, user, phash):
        self.username = user
        self.pwhash = phash
        self.karma = 0
        self.put()
