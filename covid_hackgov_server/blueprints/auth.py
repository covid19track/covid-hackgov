from quart import Blueprint, jsonify, request, current_app as app
import itsdangerous
import base64
from datetime import datetime
import secrets

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=["POST"])
async def index():
    if not app.config.get("REGISTRATIONS", False):
        return jsonify({"message": "Registrations are disabled."}), 400

    return jsonify({"token": itsdangerous.TimestampSigner(app.config["SECRET_KEY"]).sign("hackgov").decode()})
