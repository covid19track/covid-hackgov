from quart import Blueprint, jsonify, request, current_app as app

bp = Blueprint("root", __name__)


@bp.route("/endpoints")
async def endpoints():
    return jsonify({
        "endpoints": {
            "GET": {
                "endpoints": "/v1/endpoints",
                "register": "/v1/register",
                "geolocate": "/v1/geolocate",
                "random": "/v1/random"
            }
        }
    })
