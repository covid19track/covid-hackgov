from quart import Blueprint, jsonify
from logbook import Logger

bp = Blueprint("science", __name__)

log = Logger(__name__)


@bp.route("/science", methods=["POST"])
async def telemetry():
    log.info('Collecting telemetry metrics...')
    return jsonify({"message": "We're not Discord lol"})
