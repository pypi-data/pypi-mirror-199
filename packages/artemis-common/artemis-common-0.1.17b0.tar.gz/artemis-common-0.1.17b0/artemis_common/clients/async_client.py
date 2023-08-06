from __future__ import annotations

from typing import Iterable
from typing import Mapping
from typing import Optional
from typing import Type

import aiohttp
from httpx import Headers
from pydantic import BaseSettings

from .params_model import ParamsModel
from artemis_common import consts
from artemis_common.models.bases import AdvancedBaseModel
from artemis_common.models.server import ServerSuccessResponseModel


env_vars = consts._EnvironmentVariables()


def _get_dal_headers():
    return Headers(
        headers={
            consts.ARTEMIS_DAL_API_KEY_NAME: env_vars.artemis_dal_api_key.get_secret_value(),
            'Content-Type': 'application/json',
        },
    )


async def async_get(
    base_url: str,
    headers: Headers,
    route: str,
    params: Type[ParamsModel],
    output_model: Type[AdvancedBaseModel],
) -> Type[AdvancedBaseModel] | list[Type[AdvancedBaseModel]]:
    async with aiohttp.ClientSession(
        base_url=base_url,
        headers=headers,
    ) as client:
        raw_response = await client.get(
            url=route,
            params=params.get_params(),
            raise_for_status=True,
        )

    response = await raw_response.json()

    if isinstance(response, Iterable) and not isinstance(response, Mapping):
        return [output_model(**item) for item in response]
    return output_model(**response)


async def async_post(
    base_url: str,
    headers: Headers,
    route: str,
    data: Type[AdvancedBaseModel],
    params: Optional[Type[ParamsModel]] = None,
) -> ServerSuccessResponseModel:
    async with aiohttp.ClientSession(
        base_url=base_url,
        headers=headers,
    ) as client:
        raw_response = await client.post(
            url=route,
            params=params,
            json=data.dict(),
            raise_for_status=True,
        )

    response = await raw_response.json()
    return ServerSuccessResponseModel(**response)


async def dal_get(
    base_url: str,
    route: str,
    params: Type[ParamsModel],
    output_model: Type[AdvancedBaseModel],
) -> Type[AdvancedBaseModel] | list[Type[AdvancedBaseModel]]:
    return await async_get(
        base_url=base_url,
        headers=_get_dal_headers(),
        route=route,
        params=params,
        output_model=output_model,
    )


async def dal_post(
    base_url: str,
    route: str,
    data: Type[AdvancedBaseModel],
    params: Optional[Type[ParamsModel]] = None,
) -> ServerSuccessResponseModel:
    return await async_post(
        base_url=base_url,
        headers=_get_dal_headers(),
        route=route,
        data=data,
        params=params,
    )


__all__ = [
    dal_get.__name__,
    dal_post.__name__,
]
