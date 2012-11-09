from google.appengine.ext import ndb

from .user import User
from .post import Post


from ..helpers import time_ago


class Comment(ndb.Model):
    comment_text = ndb.TextProperty(indexed=True)
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    author = ndb.KeyProperty(kind=User)
    post = ndb.KeyProperty(kind=Post)
    votes = ndb.IntegerProperty()
    parent = ndb.KeyProperty(kind='Comment')
    ago = ndb.ComputedProperty(lambda self: time_ago(self.date_created))

    def add(self, text, author, post, parent=None):
        self.comment_text = text
        self.author = author
        self.post = post
        self.parent = parent
        self.votes = 0
        self.put()
