from quart import Blueprint, jsonify, request
from logbook import Logger
from ..auth import token_check

bp = Blueprint("science", __name__)

log = Logger(__name__)


@bp.route("/science", methods=["POST"])
async def telemetry():
    await token_check(request.headers.get("Authorization"))
    return "", 204
