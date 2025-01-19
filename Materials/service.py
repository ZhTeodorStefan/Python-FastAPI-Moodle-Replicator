from typing import List, Dict, Any
from fastapi import Request
from fastapi.responses import JSONResponse
from models import Evaluation
from datetime import datetime

def check_formula(evaluation: List[Evaluation]) -> bool:

    summ = 100

    for eva in evaluation:
        summ -= eva.weight

    return True if summ == 0 else False

def enhanced_body_build(
    status: int,
    message: str,
    request: Request,
    additional_links: Dict[str, Dict[str, str]] = None,
    response_code: str = "ok",
    returned_value: Any = None,
) -> JSONResponse:

    base_links = {
        "api-docs": {
            "href": "/openapi.json",
            "rel": "openapi.json",
            "title": "API Documentation",
        },
    }

    if additional_links:
        base_links.update(additional_links)

    return JSONResponse(
        status_code=status,
        content={
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,
            "response_code": response_code,
            "message": message,
            "path": str(request.url),
            "returned_value": returned_value,
            "_links": base_links,
        },
    )


def build_links(endpoint: str, rel: str, title: str, method: str) -> dict:
    return {"href": f"http://localhost:8001/api/materials{endpoint}",
            "rel": rel,
            "title": title,
            "method": method.upper()}