import os

from flask import Flask,jsonify

from app.api import survey
from app.config import PORT
from app.errors import SurveyProblem
from app.modules.ledger.storage import Archive
from app.web import workbench


def create_app(database=None):
    app=Flask(__name__)
    app.config['MAX_CONTENT_LENGTH']=2_000_000
    app.extensions['survey_archive']=Archive(database or os.getenv('SURVEY_ARCHIVE','var/survey.db'))
    app.register_blueprint(survey)
    app.register_blueprint(workbench)
    app.register_error_handler(SurveyProblem,lambda e:(jsonify(code=e.code,message=str(e)),e.status))
    app.register_error_handler(413,lambda _:(jsonify(code='TOO_LARGE',message='回收原件体积超限'),413))
    app.add_url_rule('/health',view_func=lambda:jsonify(status='ok'))
    return app


if __name__=='__main__':
    create_app().run(host='127.0.0.1',port=PORT)
