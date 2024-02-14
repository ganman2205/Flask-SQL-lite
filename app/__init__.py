import os
from flask import Flask
from app.config import Config
from app.models import db
from app.routes import students_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(students_bp, url_prefix='/api')
    return app

