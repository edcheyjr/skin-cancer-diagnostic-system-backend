from functools import wraps
from flask import request, make_response, jsonify


from app.main.service.auth_helper import Auth

# auth decorator/wrapper for protected endpoints (i.e. endpoints that require a valid user token)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        print("=======================================")
        print("data:", data)
        print("=======================================")
        if status == 200:
            return f(*args, **kwargs)
        return data, status
    return decorated

# auth decorator/wrapper for protected endpoints (i.e. endpoints that require a valid admin token)


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        print("+=================== decorator input ================+")
        print("status", status)
        print("user object", data)
        print("+====================================================+")

        # if isinstance(data, dict):
        #     # return error message before calling the actual `f` function
        #     response = make_response(jsonify(data), status)
        #     response.headers["Content-Type"] = "application/json"
        #     print("+=================== decorator input ================+")
        #     print("response", response.data)
        #     print("+====================================================+")
        #     return response
        # else:
        if status == 200:
            if data.role == 'admin':
                # return None
                return f(*args, **kwargs)  # call the actual function
            else:
                return make_response(jsonify({
                    "status": "fail",
                    "message": "unauthorized request"
                }), 401)
        else:
            return make_response(jsonify(data), status)
    return decorated
