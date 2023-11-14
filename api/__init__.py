from flask import Flask
from flask_restx import Api, Resource

from .model.task import Task

from .controller.tasks_controller import tasks_namespace

from .config import config_by_name
from .database import db

def create_app(config_name=config_by_name["dev"]):
    app = Flask(__name__)

    app.config.from_object(config_name)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app,
            title="Books API",
            description="A REST API for tasks",
    )

    api.add_namespace(tasks_namespace, path='/v1')

    return app