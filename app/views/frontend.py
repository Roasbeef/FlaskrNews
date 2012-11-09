from flask import (Blueprint, url_for, render_template, session,
                   request, redirect, g, jsonify)

from ..models.user import User
from ..models.post import Post
from ..decorators import login_required

from app import api


mod = Blueprint('frontend', __name__)


@mod.route('/', methods=['GET', 'POST'])
def index():

    page_num = 0 if request.values.get('page_num') is None else request.values.get('page_num')
    cur_string = request.values.get('cur_string')

    if request.values.get('sort') == 'new':
        content = api.get_posts(sort='new', cur_string=cur_string)
    else:
        content = api.get_posts(cur_string=cur_string)

    return render_template('index.html', content=content, page_number=int(page_num),
                           cur_string=g.page_cur.urlsafe(), more=str(g.is_more_content).lower())


@mod.route('/submit', methods=['POST'])
@login_required
def submit():

    if request.method == "POST":
        title = request.form['title']
        link = request.form['link']
        desc = request.form['description']
        user = g.user

        p = Post()
        p.add(title, link, desc, user.key)

        return redirect(url_for('frontend.index'))
