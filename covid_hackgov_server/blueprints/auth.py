from quart import Blueprint, jsonify, request
import secrets

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=["POST"])
async def index():
    user_secret = secrets.token_hex(10)
    return jsonify({"endpoint": "Token Registration Endpoint", "message": "Use the token below to get access to the API for 24 hours.", "token": user_secret})
