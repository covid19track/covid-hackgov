from quart import Blueprint, jsonify

bp = Blueprint('hello_api', __name__)


@bp.route('/')
def index():
    return jsonify({"message": "Hello API"})
