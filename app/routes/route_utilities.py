from flask import abort, make_response
from app import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"message" : f"id {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    instance = db.session.scalar(query)

    if instance is None:
        abort(make_response({"message": f"{cls.__name__} ID ({model_id}) not found."}, 404))
    return instance

