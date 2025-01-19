from fastapi import HTTPException, Request
from grpc_client import validate_token

import re

ALLOWED_ROLES = {
    (re.compile(r"^/api/materials/$"), "GET"): ["STUDENT", "PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+$"), "GET"): ["STUDENT", "PROFESSOR"],
    (re.compile(r"^/api/materials/$"), "PUT"): ["PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+$"), "DELETE"): ["ADMIN", "PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+/course$"), "POST"): ["PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+/\d+/upload-course$"), "POST"): ["PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+/lab$"), "POST"): ["PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+/\d+/course$"), "DELETE"): ["PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+/\d+/lab$"), "DELETE"): ["PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+/evaluation$"), "GET"): ["STUDENT", "PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+/lab$"), "GET"): ["STUDENT", "PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+/course$"), "GET"): ["STUDENT", "PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+/evaluation$"), "POST"): ["PROFESSOR"],
    (re.compile(r"^/api/materials/[^/]+/courses/\d+$"), "GET"): ["STUDENT", "PROFESSOR"],
}

async def role_based_filter(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or malformed")

    token = auth_header.split(" ")[1]
    try:
        user_data = validate_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    method = request.method
    path = request.url.path

    print(f'\npath: {path}\nmethod: {method}\nuser role: {user_data["role"]}')

    for (path_pattern, allowed_method), allowed_roles in ALLOWED_ROLES.items():
        if path_pattern.match(path) and method == allowed_method:
            if user_data["role"] not in allowed_roles:
                raise HTTPException(status_code=403, detail="You do not have the required role to access this route")
            return user_data

    raise HTTPException(status_code=403, detail="Access to this route is restricted")