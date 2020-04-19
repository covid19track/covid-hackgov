from quart import Blueprint, jsonify

bp = Blueprint('hello_api', __name__)


@bp.route('/')
def index():
    return jsonify({"status": 200, "message": "Hello! Use one of our endpoints."})
