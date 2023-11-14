from flask_restx import Namespace, Resource, fields, abort, reqparse
from http import HTTPStatus
from flask import request

from ..model.task import Task
from ..database import db

tasks_namespace = Namespace('tasks', description="Definitions for task routes")

task_model = tasks_namespace.model('Task',
    {
        'id': fields.Integer(description="Id for tasks"),
        'title': fields.String(description="Title for the task", required=True),
        'is_completed': fields.Boolean(description="Task is completed or not", default=False)
    }
)

bulk_delete_model = tasks_namespace.model('BulkDeleteModel',
    {
        'tasks': fields.List(fields.Raw, required=True, description='List of tasks to delete')
    }
)

bulk_add_model = tasks_namespace.model('BulkAddModel',
    {
        'tasks': fields.List(fields.Raw, required=True, description='List of tasks to add')
    }
)


@tasks_namespace.route('/tasks')
class TaskResource(Resource):

    @tasks_namespace.marshal_with(bulk_add_model)
    @tasks_namespace.doc(description="Retrieve all the tasks")
    def get(self):
        """
        Get all the tasks
        """

        query = Task.query.all()

        tasks = []

        for task in query:
            task_data = {
                'id': task.id,
                'title': task.title,
                'is_completed': task.is_completed
            }
            tasks.append(task_data)

        return {'tasks': tasks}, HTTPStatus.OK
    

    @tasks_namespace.expect(task_model, validate=True)
    @tasks_namespace.doc(description="Create a new task")
    def post(self):
        """
        Create a new task
        """
        data = request.get_json()

        new_task = Task(
            title=data['title'],
            is_completed=data.get('is_completed', False)
        )

        new_task.save()

        created_task = {
            'id': new_task.id
        }

        return created_task, HTTPStatus.CREATED

    
    @tasks_namespace.expect(bulk_add_model, validate=True)
    @tasks_namespace.doc(
        description="Bulk add tasks",
        params={"tasks": "List of tasks to add"}
    )
    def post_bulk(self):
        """
        Bulk add tasks
        """
        data = request.get_json()

        if 'tasks' not in data or not isinstance(data['tasks'], list):
            abort(HTTPStatus.BAD_REQUEST, message="Invalid input format")

        created_tasks = []

        for task_data in data['tasks']:
            # The validation error will be caught here
            new_task = Task(
                title=task_data.get('title', ''),
                is_completed=task_data.get('is_completed', False)
            )
            new_task.save()
            created_tasks.append({'id': new_task.id})

        return {'tasks': created_tasks}, HTTPStatus.CREATED


@tasks_namespace.route('/tasks/<int:task_id>')
class CRUDTasksById(Resource):

    @tasks_namespace.marshal_with(task_model)
    @tasks_namespace.doc(
        description="Retrieve a task by Id",
        params={"task_id": "An Id for a given task"}
    )
    def get(self, task_id):
        """
        Retrieve a task by id
        """
        data = Task.query.get(task_id)

        if not data:
            abort(HTTPStatus.NOT_FOUND, message="There is no task at that id")

        tasks_data = {
            'id': data.id,
            'title': data.title,
            'is_completed': data.is_completed
        }

        return tasks_data, HTTPStatus.OK

    @tasks_namespace.expect(task_model)
    @tasks_namespace.doc(
        description="Update a task by Id",
        params={"task_id": "An Id for a given task"}
    )
    def put(self, task_id):
        """
        Update a task by id
        """
        data = request.get_json()
        existing_task = Task.query.get(task_id)

        if not existing_task:
            abort(HTTPStatus.NOT_FOUND, message="There is no task at that id")

        if 'title' in data:
            existing_task.title = data['title']
        if 'is_completed' in data:
            existing_task.is_completed = data['is_completed']

        existing_task.save()

        return '', HTTPStatus.NO_CONTENT 

    @tasks_namespace.doc(
    description="Delete a task by Id",
    params={"task_id": "An Id for a given task"}
    )
    def delete(self, task_id):
        """
        Delete a task by id
        """
        existing_task = Task.query.get(task_id)

        if not existing_task:
            abort(HTTPStatus.NOT_FOUND, message="There is no task at that id")

        existing_task.delete()

        return '', HTTPStatus.NO_CONTENT  

