from google.appengine.datastore.datastore_query import Cursor
from decorators import get_or_404

from models.post import Post
#from models.user import User
from models.comment import Comment

from flask import abort


@get_or_404
def get_posts(sort_by, cur_string):

    curs = Cursor(urlsafe=cur_string) if cur_string is not None else None

    try:
        sort_attr = getattr(Post, sort_by)
        posts, next_cur, more = Post.query().order(-sort_attr).fetch_page(10, start_cursor=curs)
        content = [(post, map(lambda x: x.voter_id, post.voters))
                   for post in posts]
    except AttributeError:
        abort(404)

    return content, next_cur, more


@get_or_404
def get_single_post(post_id=None, via_comment=None):
    if post_id is not None:
        post = Post.get_by_id(post_id)
    else:
        post_id = via_comment.post.id()
        post = Post.get_by_id(post_id)
    try:
        content = (post, map(lambda x: x.voter_id, post.voters))
    except AttributeError:
        abort(404)

    return content


@get_or_404
def get_post_comments(post, context_id=None):
    comments = post.get_comment_tree(single_root_id=context_id)

    return comments


def add_comment(post_id, comment_body, user, parent_id=None):

    post = Post.get_by_id(post_id)
    if parent_id is not None:
        parent = Comment.get_by_id(parent_id).key

    comment = Comment()
    comment.add(
        text=comment_body,
        author=user,
        post=post.key,
        parent=None if parent_id is None else parent)

    if post.num_comments is None:
        post.num_comments = 0

    post.num_comments += 1
    post.put()


def delete_post_comment(comment_id):
    comment = Comment.get_by_id(comment_id)
    origin_post = comment.post.get()
    origin_post.num_comments -= 1
    origin_post.put()
    comment.key.delete()

    return origin_post.key.id()


@get_or_404
def get_single_comment(comment_id):
    comment = Comment.get_by_id(comment_id)
    return comment


def edit_comment(comment_id, new_text):
    comment = Comment.get_by_id(comment_id)
    comment.comment_text = new_text
    comment.put()
