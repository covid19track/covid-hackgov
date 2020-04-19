from quart import Blueprint, jsonify, request, jsonify
from ..auth import token_check
import aiohttp
import inspect

bp = Blueprint("geolocate", __name__)


@bp.route("/geolocate")
async def geolocate():
    await token_check(request.headers.get("Authorization"))

    async with aiohttp.ClientSession() as cs:
        ip = request.remote_addr

        if ip in ("127.0.0.1", "0.0.0.0", "localhost"):
            async with cs.get("https://api.ipify.org") as r:
                ip = await r.text()

        async with cs.get(f"http://ip-api.com/json/{ip}") as r:
            return jsonify({"country": (await r.json())["country"]})
