from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect
from forms import AnswerForm
from models import Answer

import pymysql

# MySQL 서버에 연결
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='0000',
    database='flaskproject',
    cursorclass=pymysql.cursors.DictCursor
)

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Answer.select_question(question_id)
    if question is None:

        return render_template('404.html'), 404
    if form.validate_on_submit():

        content = request.form['content']
        Answer.insert_answer(question_id, content)
        return redirect(url_for('question.detail', question_id=question_id))
    else:
        return render_template('question/question_detail.html', question=question[0], form=form)