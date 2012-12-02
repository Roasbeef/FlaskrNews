from flask import (Blueprint, url_for, render_template,
                   request, redirect, g)

from ..models.post import Post
from ..decorators import login_required

from app import api


mod = Blueprint('frontend', __name__)


@mod.route('/', methods=['GET', 'POST'])
def index():

    page_num = request.values.get('page_num', 0)
    db_cur_string = request.values.get('cur_string')

    order = 'date_created' if request.values.get('sort') == 'new' else 'hot_score'
    content, page_cur, more_content = api.get_posts(order, db_cur_string)

    return render_template('index.html', content=content, page_number=int(page_num),
                           cur_string=page_cur if page_cur else "",
                           more=str(more_content).lower())


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
