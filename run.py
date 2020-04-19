from quart import Quart, request, jsonify
from covid_hackgov_server.blueprints import (
    root,
    knowledge_base,
    auth,
    science
)
import config
import logbook
import sys
from covid_hackgov_server.errors import CovidHackgovError

handler = logbook.StreamHandler(sys.stdout, level=logbook.INFO)
handler.push_application()

log = logbook.Logger("covid_hackgov_server.boot")

logbook.compat.redirect_logging()

app = Quart(__name__)
app.config.from_object(f"config.{config.MODE}")
app.debug = app.config.get("DEBUG", False)

if app.debug:
    log.info("Running in debug mode")
    handler.level = logbook.DEBUG
    app.logger.level = logbook.DEBUG

bps = {
    root: None,
    knowledge_base: None,
    auth: None,
    science: None
}

for bp, suffix in bps.items():
    app.register_blueprint(bp.bp, url_prefix=f"/v1/{suffix or ''}")


@app.after_request
async def app_after_request(resp):
    """Handle CORS headers"""
    origin = request.headers.get("Origin", "*")
    resp.headers["Access-Control-Allow-Origin"] = origin
    resp.headers["Access-Control-Allow-Headers"] = (
        "*, X-Super-Properties, "
        "X-Fingerprint, "
        "X-Context-Properties, "
        "X-Failed-Requests, "
        "X-Debug-Options, "
        "Content-Type, "
        "Authorization, "
        "Origin, "
        "If-None-Match"
    )
    resp.headers["Access-Control-Allow-Methods"] = resp.headers.get(
        "allow", "*")

    return resp


@app.errorhandler(CovidHackgovError)
async def handle_covid_hackgov_server_err(err):
    try:
        ejson = err.json
    except IndexError:
        ejson = {}

    try:
        ejson["code"] = err.error_code
    except AttributeError:
        pass

    log.warning("error: {} {!r}", err.status_code, err.message)

    return jsonify({
        "error": True,
        "status": err.status_code,
        "message": err.message, **ejson
    }), err.status_code


@app.errorhandler(500)
async def handle_500(err):
    return jsonify({"error": True, "message": repr(err), "internal_server_error": True}), 500
