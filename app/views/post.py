from flask import (Blueprint, url_for, render_template, session,
                   request, redirect, g, jsonify, flash)

from ..models.user import User
from ..models.post import Post, Voter
from ..decorators import login_required

from app import api

mod = Blueprint('post', __name__, url_prefix='/post')


@mod.route('/<int:post_id>/', methods=['GET'])
def view_post(post_id):
    post = api.get_single_post(post_id)
    comments = api.get_post_comments(post[0])

    return render_template('post.html', content=post, comments=comments)


@mod.route("/<int:post_id>/addcomment", methods=['GET', 'POST'])
@mod.route("/<int:post_id>/<int:parent_id>/reply", methods=['GET', 'POST'])
@login_required
def add_comment(post_id, parent_id=None):

    if request.method == 'POST':
        comment_text = request.form['comment']
        if comment_text:
            flash('Comment added successfully', category='success')
            api.add_comment(post_id, comment_text, g.user.key, parent_id)
        else:
            flash('Comment cannot be blank.', category='error')

    return redirect(url_for('post.view_post', post_id=post_id))


@mod.route('/_vote/<int:post_id>', methods=['POST'])
def vote(post_id):

    post = Post.get_by_id(post_id)
    past_voters = map(lambda x: x.voter_id, post.voters)
    author = post.author.get()
    direction = request.form['direction']

    if g.user.key in past_voters:
        #if user has voted, update his direction
        previous_vote = post.voters[past_voters.index(g.user.key)]
        previous_vote.direction = direction
    else:
        #else create new voter
        new_voter = Voter(voter_id=g.user.key, direction=direction)
        post.voters.append(new_voter)

    post.votes += int(direction)
    author.karma += int(direction)

    post.put()
    author.put()

    return jsonify(result='ok')


@mod.route('/')
@login_required
def all_posts():

    return redirect(url_for('frontend.index'))

'''
@mod.route('/', methods=['POST'])
@login_required
def submit_post():

    if request.method == "POST":
        title = request.form['title']
        link = request.form['link']
        desc = request.form['description']
        user = g.user

        p = Post()
        p.add(title, link, desc, user.key)

        return redirect(url_for('frontend.index'))
'''
