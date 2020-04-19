from .errors import BadRequest
import cerberus
import logbook

log = logbook.Logger(__name__)

TOKEN_SCHEMA = {
    'token': {'type': 'string'}
}


async def validate(req, schema):
    validator = cerberus.Validator(schema)

    if req is None:
        raise BadRequest("No JSON provided")

    valid = False

    try:
        valid = validator.validate(req)
    except Exception:
        log.exception("Error while validating")
        raise Exception(f"Error while validating: {req}")

    if not valid:
        log.warning(f"Error validating doc {req}: {validator.errors}")
        raise BadRequest("Bad payload", validator.errors)

    return validator.document
