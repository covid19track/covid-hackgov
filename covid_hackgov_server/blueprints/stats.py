from quart import Blueprint, jsonify, request, jsonify
from ..auth import token_check
from io import StringIO
from datetime import datetime, timedelta
import pandas as pd
import aiohttp
import json
from ..errors import BadRequest

bp = Blueprint("stats", __name__)


async def get_stats_from_country(date, country):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv") as r:
            data = json.loads(pd.read_csv(StringIO(await r.text())).to_json())

            country_id = None

            if country.lower() != "us":
                country_id = list(filter(lambda a: a[1].lower(
                ) == country.lower(), data["Country_Region"].items()))

            if not country_id or len(country_id) < 1:
                raise BadRequest("Invalid country")

            country_id = country_id[0][0]

            country_stats = {
                "cases": data["Confirmed"][country_id],
                "deaths": data["Deaths"][country_id],
                "recovered": data["Recovered"][country_id]
            }

            return country_stats

@bp.route("")
async def stats():
    await token_check(request.headers.get("Authorization"))

    country = request.args.get("country")

    if not country:
        raise BadRequest("Empty 'country' query")

    d = datetime.utcnow()
    d -= timedelta(days=1)

    return await get_stats_from_country(f"{d:%m}-{d:%d}-{d.year}", country)

@bp.route("/daily")
async def todays_stat_increase():
    await token_check(request.headers.get("Authorization"))

    country = request.args.get("country")

    if not country:
        raise BadRequest("Empty 'country' query")

    d = datetime.utcnow()
    d -= timedelta(days=1)

    latest_data = await get_stats_from_country(f"{d:%m}-{d:%d}-{d.year}", country)
    d -= timedelta(days=1)
    yesterdays_data = await get_stats_from_country(f"{d:%m}-{d:%d}-{d.year}", country)
    latest_data["cases"] -= yesterdays_data["cases"]
    latest_data["deaths"] -= yesterdays_data["deaths"]
    latest_data["recovered"] -= yesterdays_data["recovered"]
    return latest_data