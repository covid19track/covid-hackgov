from quart import Quart, request, jsonify, redirect
from covid_hackgov_server.blueprints import (
    root,
    knowledge_base,
    auth,
    science,
    geolocate,
    stats
)
import config
import logbook
import sys
from covid_hackgov_server.errors import CovidHackgovError
import asyncpg
from quart_cors import cors

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
    science: None,
    geolocate: None,
    stats: "stats"
}

for bp, suffix in bps.items():
    app.register_blueprint(cors(bp.bp, allow_origin="*"), url_prefix=f"/v1/{suffix or ''}")

@app.before_serving
async def app_before_serving():
    log.info("Opening DB")
    app.db = await asyncpg.create_pool(**app.config["POSTGRES"])


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

@app.errorhandler(404) 
async def page_not_found(err): 
    return redirect("/not_found.html")

app = cors(app, allow_origin="*")