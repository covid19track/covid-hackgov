from quart import Blueprint, jsonify, request, current_app as app

bp = Blueprint("root", __name__)


@bp.route("/endpoints")
async def endpoints():
    return jsonify({
        "endpoints": {
            "GET": {
                "Endpoints": "/v1/endpoints",
                "Register": "/v1/register",
                "Generate API Key": "/v1/genAPIKey",
                "Validate API Key": "/v1/validateKey",
                "Geolocate": "/v1/geolocate",
                "Random Fact": "/v1/randomFact"
            }
        }
    })
