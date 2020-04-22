from quart import Blueprint, jsonify, request, jsonify
from ..auth import token_check
import aiohttp
import inspect
from ..schemas import validate
from ..errors import BadRequest

bp = Blueprint("geolocate", __name__)

GEOLOCATE_SCHEMA = {
    "ip": { "type": "string" }
}

@bp.route("/geolocate")
async def geolocate():
    await token_check(request.headers.get("Authorization"))

    ip = (await validate(await request.get_json(), GEOLOCATE_SCHEMA)).get("ip")

    if not ip:
        raise BadRequest("Empty 'ip' field")

    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"http://ip-api.com/json/{ip}") as r:
            data = await r.json()
            country = data.get("country")

            if country is None:
                raise BadRequest(data.get("message"))

            return jsonify({"country": country})