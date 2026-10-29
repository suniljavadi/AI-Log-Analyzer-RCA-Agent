import logging
import time
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("app.request")


async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))[:128]
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("unhandled error: %s %s", request.method, request.url.path, extra={"request_id": request_id})
        response = JSONResponse({"detail": "Internal server error", "request_id": request_id}, status_code=500)
    duration_ms = (time.perf_counter() - started) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Request-Duration-Ms"] = f"{duration_ms:.2f}"
    logger.info(
        "%s %s -> %s (%.2f ms)", request.method, request.url.path, response.status_code, duration_ms,
        extra={"request_id": request_id},
    )
    return response