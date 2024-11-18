from flask import Blueprint, request
from flask_restful import Resource, Api
from app import db
from app.models import Task


task_bp = Blueprint("api_task", __name__)
task_api = Api(task_bp)

class TaskGet(Resource):
    # Handle GET requests for a specific task by ID
    def get(self, task_id):
        try:
            task = db.get_or_404(Task, task_id)
            return {
                "task_id": task.task_id,
                "task_name": task.task_name,
                "task_description": task.task_description,
                "task_order_id": task.task_order_id,
                "column_id": task.column_id
            }
        except Exception as e:
            return {"error": "There is an error getting the task"}, 500


class TaskPost(Resource):
    # Handle POST requests for creating a new task
    def post(self):
        try:
            # Get data from request JSON
            data = request.json
            task_name = data.get("task_name")
            task_description = data.get("task_description")
            task_order_id = data.get("task_order_id")
            column_id = data.get("column_id")

            # Create a new task instance
            task = Task(task_name=task_name, task_description=task_description, task_order_id=task_order_id, column_id=column_id)
            db.session.add(task)
            db.session.commit()

            return {
                "task_id": task.task_id,
                "task_name": task.task_name,
                "task_description": task.task_description,
                "task_order_id": task.task_order_id,
                "column_id": task.column_id
            }, 201
            
        except Exception as e:
            return {"error": "There is an error posting the task"}, 500


class TaskDelete(Resource):
    def delete(self, task_id):
        try:
            task = db.session.execute(db.select(Task).filter_by(task_id = task_id)).scalar_one()

            db.session.delete(task)
            db.session.commit()

            return(
                {
                    "Success" : f"Successfully deleted {task_id}"
                }
            ), 200
        except Exception as e:
            return (
                {"error" : f"Could not delete the id {task_id}{e}"}
            ), 500


class TaskPatch(Resource):
    def patch(self, task_id):
        data = request.json
        task_name = data.get("task_name")
        task_description = data.get("task_description")
        task_order_id = data.get("task_order_id")
        column_id = data.get("column_id")
        try:
            task =  db.session.execute(db.select(Task).filter_by(task_id = task_id)).scalar_one()
            task.task_name = task_name
            task.task_description = task_description
            task.task_order_id = task_order_id
            task.column_id = column_id
            db.session.commit()
            return(
                {
                    "Success" : f"You have edited the id {task_id}"
                }
            ), 200
        except Exception as e:
            return(
                {
                    "error" : f"There was an error with patching {task_id} {e}"
                }
            ), 500

# Register the resources with distinct routes
task_api.add_resource(TaskGet, '/tasks/<int:task_id>', endpoint="get_task")
task_api.add_resource(TaskPost, '/tasks', endpoint="post_task")
task_api.add_resource(TaskDelete, '/tasks/<int:task_id>', endpoint="delete_task")
task_api.add_resource(TaskPatch, "/tasks/<int:task_id>", endpoint="patch_task")