from rest_framework_jwt.utils import jwt_payload_handler


# custom payload to include specified fields in token
def jwt_custom_payload_handler(user):
    payload = jwt_payload_handler(user)
    payload['firstname'] = user.first_name
    payload['lastname'] = user.last_name
    payload['telephone'] = user.telephone.raw_phone
    return payload
