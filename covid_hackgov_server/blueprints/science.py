from quart import Blueprint, jsonify
import random

bp = Blueprint('science_api', __name__)


@bp.route('/science')
def telemetry():
    return jsonify({"endpoint": "Not suitable for work.", "message": "You are not authenticated, get the out."})
