from quart import Blueprint, jsonify, request, current_app as app
from logbook import Logger
from datetime import datetime
from ..auth import token_check
from ..schemas import validate
import asyncio

bp = Blueprint("science", __name__)

log = Logger(__name__)

SCIENCE_SCHEMA = {
    "action": {"type": "string"}
}


@bp.route("/science", methods=["POST"])
async def telemetry():
    token = request.headers.get("Authorization")

    await token_check(token)

    action = (await validate(await request.get_json(), SCIENCE_SCHEMA)).get("action")

    if not action:
        raise BadRequest("Empty 'action' field")

    timestamp = int(datetime.utcnow().timestamp())

    async with app.db.acquire() as pool:
        await pool.execute("INSERT INTO science(action, timestamp, token) VALUES($1, $2, $3)", action, timestamp, token)

    log.info(f"{action}, {timestamp}, {token}")

    return "", 204
