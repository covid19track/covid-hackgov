from quart import Blueprint, jsonify, request
import random
from ..auth import token_check
from ..schemas import validate
from ..errors import Unauthorized

bp = Blueprint("knowledge_base", __name__)

KNOWLEDGE_SCHEMA = {
    'token': {'type': 'string'}
}


@bp.route("/random", methods=["GET"])
async def knowledge():
    data = validate(await request.get_json(), KNOWLEDGE_SCHEMA)

    token_check(data["token"])

    return jsonify({
        "knowledge": random.choice([
            "Σύμφωνα με το Κινέζικο κράτος, η διασπορά του COVID-19 ξεκίνησε τον Δεκέμβριο του 2019",
            "Ο πληθυσμός της Ουχάν είναι ίσος με αυτόν της Ελλάδας!",
            "Υπάρχουν 210 χώρες που έχουν δηλώσει για ασθενείς, με σύνολο 2.5 εκατομμυρίων κρουσμάτων",
            "Κάθε ήπειρος εκτός απο την Ανταρκτική έχει δηλώσει για κρούσματα COVID-19",
            "Μένουμε σπίτι! Ο COVID-19 είναι αληθινός και η ανθρωπότητα κινδυνεύει!",
            "Ο όρος COVID-19 σημαίνει Corona Virus Disease 2019",
            "Το SARS-COV-2 σημαίνει κορονοϊός σοβαρού οξέος αναπνευστικού συνδρόμου τύπου 2 (Severe Acute Respiratory Syndrome COronaVirus 2)",
            "Ένας ιός είναι ένα προκαρυοτικό κύτταρο, δεν είναι ζωντανά, το μόνο που κάνει είναι να εισάγουν το δικό τους DNA σε άλλα κύτταρα",
            "Τα προκαρυοτικά κύτταρα είναι 10x μικρότερα από τα ευκαρυοτικά",
            "Ο κορονοϊός πρωτοεμφανίστηκε στην πόλη Ουχάν, της κινέζικης επαρχίας Χουμπεί.",
            "O SARS-COV-2 είναι κατά 96% πιθανόν να προήλθε απο τις νυχτερίδες.",
            "Δέν υπάρχει κάνενα εμβόλιο απο τον κορονοϊό, μείνετε σπίτι για ένα καλύτερο μέλλον!",
            "Δείτε τον πηγαίο κώδικα του project στο https://github.com/covid19track",
        ])
    })
