from quart import Blueprint, jsonify
import random

bp = Blueprint("science", __name__)


@bp.route("/science")
def telemetry():
    return jsonify({"message": "We're not Discord lol"})
