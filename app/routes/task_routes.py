from flask import Blueprint,make_response, abort, request, Response
from ..models.task import Task
from app import db

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.post("")
def create_task():

    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError as error:
        message = {
            "message": f"Missing '{error.args[0]}' attribute"
        }
        abort(make_response(message, 400))
    db.session.add(new_task)
    db.session.commit()

    response = new_task.to_dict()
    return response, 201

# def get_task_or_404(task_id):
#     task = Task.query.get(task_id) #This tries to find a Task in the database with ID If exists return Task object else None
#     if task is None:
#         abort(404, description=f"Task with id {task_id} not found")
#     return task