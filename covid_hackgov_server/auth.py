import logbook
import itsdangerous
import base64
import binascii
from .errors import Unauthorized, Forbidden
from quart import current_app as app

log = logbook.Logger(__name__)


def token_check(token):
    try:
        if token.split(".")[0] != "hackgov":
            raise Unauthorized("Invalid token")
    except IndexError:
        raise Unauthorized("Invalid token")

    try:
        itsdangerous.TimestampSigner(app.config["SECRET_KEY"]).unsign(token)
    except itsdangerous.BadSignature:
        raise Forbidden("Invalid token")
