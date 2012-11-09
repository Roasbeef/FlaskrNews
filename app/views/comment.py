from flask import (Blueprint, url_for, render_template, session,
                   request, redirect, g, jsonify, flash)

from ..decorators import login_required
from ..models.user import User
from ..models.comment import Comment

from app import api

mod = Blueprint('comment', __name__, url_prefix='/comment')


@mod.route('/<int:comment_id>/delete', methods=['DELETE', 'POST'])
def delete_comment(comment_id):

    origin_post = api.delete_post_comment(comment_id)

    flash('Comment deleted successfully', category='success')
    return redirect(url_for('post.view_post', post_id=origin_post))


@mod.route('/<int:comment_id>/edit', methods=['POST'])
def edit_comment(comment_id):
    updated_comment = request.form['new_comment']
    api.edit_comment(comment_id, updated_comment)

    resp = jsonify(message='ok')
    resp.status_code = 200
    return resp


@mod.route('/<int:comment_id>/', methods=['GET'])
def view_comment(comment_id):
    perma_comment = api.get_single_comment(comment_id)
    post = api.get_single_post(via_comment=perma_comment)
    context_tree = api.get_post_comments(post[0], context_id=perma_comment.key.id())

    return render_template("post.html", content=post, comments=context_tree)
