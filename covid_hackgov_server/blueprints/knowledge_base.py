from quart import Blueprint, jsonify
import random

bp = Blueprint("knowledge_base", __name__)


@bp.route("/random")
async def knowledge():
    return jsonify({
        "knowledge": random.choice([
            "According to Chinese Government, COVID-19 spread began in December of 2019",
            "Wuhan's population is equal to Greece's entire population.",
            "There are 210 countries that have reported a total of 2.3 million cases!",
            "Every single continent except Africa has reported COVID-19 cases."
            "Stay home! COVID-19 is out there, seeking for people!"
        ])
    })
