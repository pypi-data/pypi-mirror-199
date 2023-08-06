from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ..models.token_error_response import TokenErrorResponse
from ..models.token_total_supply_response import TokenTotalSupplyResponse
from ..types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    scaled: Union[Unset, None, bool] = True,
) -> Dict[str, Any]:
    url = "{}/v1/tokens/{chainId}/{tokenAddress}/total-supply".format(
        client.base_url, chainId=chain_id, tokenAddress=token_address
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["blockNumber"] = block_number

    params["timestamp"] = timestamp

    params["scaled"] = scaled

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[TokenErrorResponse, TokenTotalSupplyResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TokenTotalSupplyResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = TokenErrorResponse.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[TokenErrorResponse, TokenTotalSupplyResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    scaled: Union[Unset, None, bool] = True,
) -> Response[Union[TokenErrorResponse, TokenTotalSupplyResponse]]:
    """Get token's total supply

     Returns total supply of a token.

    Args:
        chain_id (float):
        token_address (str):
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):
        scaled (Union[Unset, None, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenTotalSupplyResponse]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        block_number=block_number,
        timestamp=timestamp,
        scaled=scaled,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    scaled: Union[Unset, None, bool] = True,
) -> Optional[Union[TokenErrorResponse, TokenTotalSupplyResponse]]:
    """Get token's total supply

     Returns total supply of a token.

    Args:
        chain_id (float):
        token_address (str):
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):
        scaled (Union[Unset, None, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenTotalSupplyResponse]]
    """

    return sync_detailed(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        block_number=block_number,
        timestamp=timestamp,
        scaled=scaled,
    ).parsed


async def asyncio_detailed(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    scaled: Union[Unset, None, bool] = True,
) -> Response[Union[TokenErrorResponse, TokenTotalSupplyResponse]]:
    """Get token's total supply

     Returns total supply of a token.

    Args:
        chain_id (float):
        token_address (str):
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):
        scaled (Union[Unset, None, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenTotalSupplyResponse]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        block_number=block_number,
        timestamp=timestamp,
        scaled=scaled,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    scaled: Union[Unset, None, bool] = True,
) -> Optional[Union[TokenErrorResponse, TokenTotalSupplyResponse]]:
    """Get token's total supply

     Returns total supply of a token.

    Args:
        chain_id (float):
        token_address (str):
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):
        scaled (Union[Unset, None, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenTotalSupplyResponse]]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            token_address=token_address,
            client=client,
            block_number=block_number,
            timestamp=timestamp,
            scaled=scaled,
        )
    ).parsed
