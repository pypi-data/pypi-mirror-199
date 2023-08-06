from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ..models.get_cached_model_results_order import GetCachedModelResultsOrder
from ..models.model_runtime_stats_response import ModelRuntimeStatsResponse
from ..types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    slug: str,
    sort: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    offset: Union[Unset, None, float] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v1/model/results".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["slug"] = slug

    params["sort"] = sort

    json_order: Union[Unset, None, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value if order else None

    params["order"] = json_order

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[ModelRuntimeStatsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ModelRuntimeStatsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ModelRuntimeStatsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    slug: str,
    sort: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    offset: Union[Unset, None, float] = UNSET,
) -> Response[ModelRuntimeStatsResponse]:
    """Cached model results

     Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
    and get results, use `POST /v1/model/run`.

    Args:
        slug (str):
        sort (Union[Unset, None, str]):
        order (Union[Unset, None, GetCachedModelResultsOrder]):
        limit (Union[Unset, None, float]):
        offset (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        slug=slug,
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    slug: str,
    sort: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    offset: Union[Unset, None, float] = UNSET,
) -> Optional[ModelRuntimeStatsResponse]:
    """Cached model results

     Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
    and get results, use `POST /v1/model/run`.

    Args:
        slug (str):
        sort (Union[Unset, None, str]):
        order (Union[Unset, None, GetCachedModelResultsOrder]):
        limit (Union[Unset, None, float]):
        offset (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    return sync_detailed(
        client=client,
        slug=slug,
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    slug: str,
    sort: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    offset: Union[Unset, None, float] = UNSET,
) -> Response[ModelRuntimeStatsResponse]:
    """Cached model results

     Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
    and get results, use `POST /v1/model/run`.

    Args:
        slug (str):
        sort (Union[Unset, None, str]):
        order (Union[Unset, None, GetCachedModelResultsOrder]):
        limit (Union[Unset, None, float]):
        offset (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        slug=slug,
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    slug: str,
    sort: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    offset: Union[Unset, None, float] = UNSET,
) -> Optional[ModelRuntimeStatsResponse]:
    """Cached model results

     Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
    and get results, use `POST /v1/model/run`.

    Args:
        slug (str):
        sort (Union[Unset, None, str]):
        order (Union[Unset, None, GetCachedModelResultsOrder]):
        limit (Union[Unset, None, float]):
        offset (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            slug=slug,
            sort=sort,
            order=order,
            limit=limit,
            offset=offset,
        )
    ).parsed
