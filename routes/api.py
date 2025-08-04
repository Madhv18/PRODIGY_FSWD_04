# file: routes/api.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

api_bp = Blueprint("api", __name__)

@api_bp.route("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    return jsonify({"user": user_id})
