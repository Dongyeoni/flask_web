from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from forms import UserCreateForm
from models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.select_one(username=form.username.data)
        if not user:
            User.create_user(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            return redirect(url_for('main.index'))

        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)