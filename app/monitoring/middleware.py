import time
import uuid

from fastapi import Request


async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    started = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Request-Duration-Ms"] = f"{(time.perf_counter() - started) * 1000:.2f}"
    return response
