def get_request_param(request, param):
    return request.data.get(param, '').strip()


ALLOWED_ROLES = ['user', 'driver']
