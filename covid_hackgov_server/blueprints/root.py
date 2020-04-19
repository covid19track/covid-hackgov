from quart import Blueprint, jsonify, request, current_app as app

bp = Blueprint("root", __name__)


@bp.route("/endpoints")
async def endpoints():
    return jsonify({"endpoints": {"endpoints": "/v1/endpoints", "register": "/v1/register", "random": "/v1/random"}})


@bp.route("/.well-known/nodeinfo")
async def nodeinfo_index():
    proto = "http" if not app.config.get("IS_SSL", False) else "https"
    main_url = app.config.get("MAIN_URL", request.host)

    return jsonify({
        "links": [
            {
                "href": f"{proto}://{main_url}/nodeinfo/2.0.json",
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0"
            },
            {
                "href": f"{proto}://{main_url}/nodeinfo/2.1.json",
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.1"
            }
        ]
    })


def fetch_nodeinfo():
    return {
        "metadata": {
            "features": ["covid_hackgov_server"],
            "nodeDescription": "An instance of covid_hackgov_server",
            "nodeName": app.config.get("node_name"),
            "private": app.config.get("node_private", False),
            "federation": {}
        },
        "openRegistrations": app.config.get("REGISTRATIONS", False),
        "protocols": [],
        "software": {
            "name": "covid_hackgov_server",
            "version": "vINFINITY"
        },
        "services": {
            "inbound": [],
            "outbound": []
        },
        "usage": {
            "localPosts": 0,
            "users": {
                "total": 0
            }
        },
        "version": "0"
    }


@bp.route("/nodeinfo/2.0.json")
async def nodeinfo_20():
    """Handler for nodeinfo 2.0"""
    return jsonify(fetch_nodeinfo())


@bp.route("/nodeinfo/2.1.json")
async def nodeinfo_21():
    """Handler for nodeinfo 2.1"""
    nodeinfo = fetch_nodeinfo()

    nodeinfo["software"]["repository"] = "https://github.com/covid19track/covid-hackgov-server"
    return jsonify(nodeinfo)
