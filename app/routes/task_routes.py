from flask import Blueprint,make_response, abort, request, Response
from ..models.task import Task
from app.routes.route_utilities import validate_model
from app import db
from sqlalchemy import asc, desc
from datetime import datetime, timezone
import os
import requests

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.post("")
def create_task():

    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError as error:
        message = {
            # "message": f"Missing '{error.args[0]}' attribute"
            "details": "Invalid data"
        }
        abort(make_response(message, 400))
    db.session.add(new_task)
    db.session.commit()

    response =  {"task": new_task.to_dict()}
    return response, 201

@task_bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort")

    query = db.select(Task)
    if sort_param == "asc":
        query = query.order_by(asc(Task.title))
    elif sort_param == "desc":
        query = query.order_by(desc(Task.title))

    tasks = db.session.scalars(query) #This executes the SQL query

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response

@task_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task,task_id)
    # return task.to_dict()
    return {"task": task.to_dict()}


# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except ValueError:
#         response = {"message" : f"task {task_id} invalid"}
#         abort(make_response(response, 400))

#     # task = Task.query.get(task_id)
#     query = db.select(Task).where(Task.id == task_id)
#     task = db.session.scalar(query)
#     # db.session.get(Task, task_id)

#     if task is None:
#         message = {
#             "message": f"task ID ({task_id}) not found."
#         }
#         abort(make_response(message, 404))
#     return task

@task_bp.put("/<task_id>")
def update_task(task_id):

    task = validate_model(Task,task_id)

    request_body = request.get_json()

    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except KeyError as error:
        message = {
            "message": f"Missing '{error.args[0]}' attribute"
        }
        abort(make_response(message, 400))

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@task_bp.delete("/<task_id>")
def remove_task(task_id):

    task = validate_model(Task,task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

def send_slack_message(task_title):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL", "task-notifications")

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": f"#{channel}",
        "text": f"Someone just completed the task {task_title}"
    }

    requests.post(url, json=payload, headers=headers)

@task_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task,task_id)

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    send_slack_message(task.title)

    return Response(status=204, mimetype="application/json")

@task_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task,task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")

