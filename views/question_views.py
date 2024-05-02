import math

from flask import Blueprint,render_template,request, url_for
from models import Question,Answer
from forms import QuestionForm, AnswerForm
from werkzeug.utils import redirect

bp = Blueprint("question",__name__, url_prefix="/question")

@bp.route('/list/')
def _list():

    page = request.args.get('page', type=int, default=1)

    ## 직접 주소창에 페이지 입력하는 경우 1보다 작으면 1로 가게끔
    if int(page) <1:
        page = 1

    question_list = Question.select_all_order_list()

    ###하드코딩 주의!!!!!!!!!!!!!!!#######################
    ##모듈화 하면 좋겠지만...일단 이렇게 구현
    pagination = {}
    pagination['items'] = question_list
    pagination['count'] = len(question_list) ## 총 개수 보관용
    pagination['per_page'] = 10  ## 원하는 개수만큼 조정
    pagination['total'] = len(question_list) // pagination['per_page'] +1 if len(question_list) % pagination['per_page']  != 0 else len(question_list) // pagination['per_page']
    pagination['current_page'] = page


    if pagination['total'] > 10 and pagination['current_page'] <=5 :
        pagination['iter_pages'] = list(range(1, 11))
    elif pagination['total'] > 10 and pagination['current_page'] + 4 >= pagination['total']:
        # 현재 페이지 기준으로 마지막 10개 페이지 출력
        pagination['iter_pages'] = list(range(pagination['current_page'] - 9, pagination['total'] + 1))
    elif pagination['total'] > 10 :
        pagination['iter_pages'] = list(range(pagination['current_page'] - 4, pagination['current_page'] + 6))
    else :
        # 10페이지보다 적은 경우
        pagination['iter_pages'] = [i + 1 for i in range((pagination['total']))]

   ### 답변 개수 산출용
    for item in pagination['items']:
        item['count'] = Answer.how_many_answers(item['id'])


    pagination['prev_num'] = pagination['current_page'] - 1
    pagination['next_num'] = pagination['current_page'] + 1
    pagination['has_prev'] = pagination['current_page'] > 1
    pagination['has_next'] = pagination['current_page'] < pagination['total']

    ## 다음페이지가 있고 개수가 10개 안 되는 경우
    if (pagination['has_next'] and len(question_list) % pagination['per_page'] != 0):
        pagination['items'] = question_list[  (pagination['current_page']-1) * pagination['per_page'] :  pagination['current_page'] * pagination['per_page']]
    ## 현재 페이지가 마지막 페이지이며, 하나밖에 없는 경우
    elif(len(pagination['iter_pages'])==1 ):
        pagination['items'] = question_list
    else:
        pagination['items'] = question_list[(pagination['current_page'] - 1) * pagination['per_page']: ]

    question_list = pagination


    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.select_one(question_id)
    if question is None:
        return render_template('404.html'), 404
    question = dict(question)

    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()

    if request.method == 'POST' and form.validate_on_submit():
        subject = form.subject.data
        content = form.content.data
        Question.insert_question(subject,content)
        return redirect(url_for('main.index'))

    return render_template('question/question_form.html', form=form)