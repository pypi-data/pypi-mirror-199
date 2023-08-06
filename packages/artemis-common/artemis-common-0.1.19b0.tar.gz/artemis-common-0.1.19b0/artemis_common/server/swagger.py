from __future__ import annotations

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.docs import get_swagger_ui_html


def add_swagger(app: FastAPI):
    @app.get('/redoc', include_in_schema=False)
    async def redoc():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=f'{app.title} - Redoc',
            redoc_js_url='/static/redoc.standalone.js',
            redoc_favicon_url='/static/favicon-32x32.png',
        )

    @app.get('/docs', include_in_schema=False)
    async def docs():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f'{app.title} - Swagger',
            swagger_js_url='/static/swagger-ui-bundle.js',
            swagger_css_url='/static/swagger-ui.css',
            swagger_favicon_url='/static/favicon-32x32.png',
        )
