from __future__ import annotations

from itertools import chain
from typing import Any, Sequence

from fastapi import APIRouter, FastAPI

from anqa.core.abc.service import AbstractSideService
from anqa.core.utils.class_utils import get_kwargs

from .errors import add_error_handlers
from .openapi import simplify_operation_ids
from .prometheus import add_prometheus_middleware
from .settings import ApiSettings


def add_side_service(app: FastAPI, service: AbstractSideService):
    app.on_event("startup")(service.start)
    app.on_event("shutdown")(service.stop)

    if hasattr(service, "endpoint_definitions"):
        for e in service.endpoint_definitions:
            app.add_api_route(**e)


def create_fastapi_app(
    settings: ApiSettings | type[ApiSettings] | None = None,
    routers: Sequence[APIRouter] = (),
    **kwargs: Any,
) -> FastAPI:
    if settings is None:
        settings = ApiSettings()
    elif isinstance(settings, type):
        settings = settings()
    kw = {**settings.dict(), **kwargs}
    filtered_kw = get_kwargs(FastAPI, kw)
    app = FastAPI(**filtered_kw)
    add_error_handlers(app)
    add_prometheus_middleware(app)
    for side_service in settings.side_services:
        add_side_service(app, side_service)
    for router in chain(routers, settings.routers):
        app.include_router(router)

    simplify_operation_ids(app)
    return app
