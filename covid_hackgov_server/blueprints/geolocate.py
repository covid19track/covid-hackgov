from quart import Blueprint, jsonify, request, jsonify
from ..auth import token_check
from ..schemas import validate, TOKEN_SCHEMA
import aiohttp
import inspect

bp = Blueprint("geolocate", __name__)


@bp.route("/geolocate")
async def geolocate():
    data = await validate(await request.get_json(), TOKEN_SCHEMA)

    await token_check(data.get("token"))

    async with aiohttp.ClientSession() as cs:
        ip = request.remote_addr

        if ip in ("127.0.0.1", "0.0.0.0", "localhost"):
            async with cs.get("https://api.ipify.org") as r:
                ip = await r.text()

        async with cs.get(f"http://ip-api.com/json/{ip}") as r:
            return jsonify({"country": (await r.json())["country"]})
