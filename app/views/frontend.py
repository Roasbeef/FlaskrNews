from flask import Blueprint, render_template, request


from app import api


mod = Blueprint('frontend', __name__)


@mod.route('/', methods=['GET', 'POST'])
def index():

    page_num = request.values.get('page_num', 0)
    db_cur_string = request.values.get('cur_string')

    order = 'date_created' if request.values.get('sort') == 'new' else 'hot_score'
    content, page_cur, more_content = api.get_posts(order, db_cur_string)

    return render_template('index.html', content=content, page_number=int(page_num),
                           cur_string=page_cur.urlsafe() if page_cur else "",
                           more=str(more_content).lower())
