from flask import Flask
import config
from models import *

def create_app():
    ## DB 없는 경우에 생성
    Question()
    Answer()
    User()

    app = Flask(__name__)
    app.config.from_object(config)

    # 블루프린트
    from .views import main_views, question_views,answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
