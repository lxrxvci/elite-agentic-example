"""RFC 9457 Problem Details and global exception handlers."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None


def problem_response(
    status: int,
    title: str,
    detail: str | None = None,
    instance: str | None = None,
    type_base: str = "https://api.example.com/errors",
) -> JSONResponse:
    slug = title.lower().replace(" ", "-")
    body = {
        "type": f"{type_base}/{slug}",
        "title": title,
        "status": status,
        "detail": detail,
        "instance": instance,
    }
    return JSONResponse(content=body, status_code=status, media_type="application/problem+json")


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class ValidationError(Exception):
    pass


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = [
            {"pointer": f"/{'.'.join(str(loc) for loc in err['loc'][1:])}", "message": err["msg"]}
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=400,
            content={
                "type": "https://api.example.com/errors/validation-error",
                "title": "Validation error",
                "status": 400,
                "detail": "One or more fields failed validation.",
                "instance": str(request.url.path),
                "errors": errors,
            },
            media_type="application/problem+json",
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return problem_response(
            status=404,
            title="Not found",
            detail=str(exc),
            instance=str(request.url.path),
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
        return problem_response(
            status=409,
            title="Conflict",
            detail=str(exc),
            instance=str(request.url.path),
        )

    @app.exception_handler(ValidationError)
    async def domain_validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
        return problem_response(
            status=422,
            title="Unprocessable entity",
            detail=str(exc),
            instance=str(request.url.path),
        )

    @app.exception_handler(Exception)
    async def catchall_handler(request: Request, exc: Exception) -> JSONResponse:
        return problem_response(
            status=500,
            title="Internal server error",
            detail="An unexpected error occurred. Please try again later.",
            instance=str(request.url.path),
        )
