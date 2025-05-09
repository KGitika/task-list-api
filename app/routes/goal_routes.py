from flask import Blueprint,make_response, abort, request, Response
from ..models.goal import Goal
from app.routes.route_utilities import validate_model
from app import db

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goal_bp.post("")
def create_goal():

    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError as error:
        message = {
            # "message": f"Missing '{error.args[0]}' attribute"
            "details": "Invalid data"
        }
        abort(make_response(message, 400))
    db.session.add(new_goal)
    db.session.commit()

    response =  {"goal": new_goal.to_dict()}
    return response, 201

@goal_bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query) #This executes the SQL query

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return goals_response

@goal_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}

@goal_bp.put("/<goal_id>")
def update_goal(goal_id):

    goal = validate_model(Goal,goal_id)

    request_body = request.get_json()

    try:
        goal.title = request_body["title"]
    except KeyError as error:
        message = {
            "message": f"Missing '{error.args[0]}' attribute"
        }
        abort(make_response(message, 400))

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goal_bp.delete("/<goal_id>")
def remove_task(goal_id):

    goal = validate_model(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")




