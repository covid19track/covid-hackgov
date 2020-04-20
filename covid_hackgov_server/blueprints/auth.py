from quart import Blueprint, jsonify, request, current_app as app
import itsdangerous
import base64
from datetime import datetime
import secrets
from ..auth import token_check

bp = Blueprint('auth', __name__)

@bp.route("/validateAPIKey")
async def validate_token():
    await token_check(request.headers.get("Authorization"))
    return "", 204

@bp.route('/genAPIKey')
async def index():
    if not app.config.get("REGISTRATIONS", False):
        return jsonify({"message": "Registrations are disabled."}), 400

    return jsonify({"token": itsdangerous.TimestampSigner(app.config["SECRET_KEY"]).sign("hackgov").decode()})
