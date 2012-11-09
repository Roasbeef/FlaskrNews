from google.appengine.ext import ndb
from .user import User
from math import log
from datetime import datetime, timedelta
from ..helpers import time_ago


class Voter(ndb.Model):
    voter_id = ndb.KeyProperty(kind=User)
    direction = ndb.StringProperty()


class Post(ndb.Model):
    votes = ndb.IntegerProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    num_comments = ndb.IntegerProperty()
    hot_score = ndb.ComputedProperty(lambda self: hotness(self.date_created, self.votes), indexed=True)
    ago = ndb.ComputedProperty(lambda self: time_ago(self.date_created))
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    link = ndb.StringProperty()
    author = ndb.KeyProperty(kind=User)
    voters = ndb.StructuredProperty(Voter, repeated=True)

    def add(self, title, link, desc, key):
        self.title = title
        self.link = link
        self.description = desc
        self.author = key
        self.votes = 0
        self.put()

    def get_comment_tree(self, single_root_id=None):
        from .comment import Comment

        def make_comment_tree(base_comment, depth=1):
            siblings = Comment.query() \
                              .filter(Comment.parent == base_comment.key) \
                              .order(-Comment.votes) \
                              .fetch()
            base_comment.children = []
            base_comment.depth = depth - 1
            for comment in siblings:
                comment.depth = depth + 1
                base_comment.children.append(comment)
                make_comment_tree(comment, depth=depth + 1)

            return base_comment

        if single_root_id is not None:
            root_comments = [Comment.get_by_id(single_root_id)]
        else:
            root_comments = Comment.query() \
                                   .filter(Comment.post == self.key) \
                                   .filter(Comment.parent == None) \
                                   .order(-Comment.votes) \
                                   .fetch()

        comment_tree = [make_comment_tree(root)
                        for root in root_comments]

        return comment_tree


def hotness(date, score):

    if date is None:
        return

    def epoch_seconds(date):

        epoch = datetime(1970, 1, 1)
        td = date - epoch

        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

    order = log(max(abs(score), 1), 10)
    sign = 1 if score > 0 else -1 if score < 0 else 0
    seconds = epoch_seconds(date) - 1134028003

    return round(order + sign * seconds / 45000, 7)
