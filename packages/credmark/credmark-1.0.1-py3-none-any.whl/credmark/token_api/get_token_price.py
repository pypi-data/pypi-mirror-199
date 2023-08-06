from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ..models.get_token_price_align import GetTokenPriceAlign
from ..models.get_token_price_src import GetTokenPriceSrc
from ..models.token_error_response import TokenErrorResponse
from ..models.token_price_response import TokenPriceResponse
from ..types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    quote_address: Union[Unset, None, str] = UNSET,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    src: Union[Unset, None, GetTokenPriceSrc] = GetTokenPriceSrc.DEX,
    align: Union[Unset, None, GetTokenPriceAlign] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v1/tokens/{chainId}/{tokenAddress}/price".format(
        client.base_url, chainId=chain_id, tokenAddress=token_address
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["quoteAddress"] = quote_address

    params["blockNumber"] = block_number

    params["timestamp"] = timestamp

    json_src: Union[Unset, None, str] = UNSET
    if not isinstance(src, Unset):
        json_src = src.value if src else None

    params["src"] = json_src

    json_align: Union[Unset, None, str] = UNSET
    if not isinstance(align, Unset):
        json_align = align.value if align else None

    params["align"] = json_align

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
) -> Optional[Union[TokenErrorResponse, TokenPriceResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TokenPriceResponse.from_dict(response.json())

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
) -> Response[Union[TokenErrorResponse, TokenPriceResponse]]:
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
    quote_address: Union[Unset, None, str] = UNSET,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    src: Union[Unset, None, GetTokenPriceSrc] = GetTokenPriceSrc.DEX,
    align: Union[Unset, None, GetTokenPriceAlign] = UNSET,
) -> Response[Union[TokenErrorResponse, TokenPriceResponse]]:
    """Get token price data

     Returns price data for a token.

    Args:
        chain_id (float):
        token_address (str):
        quote_address (Union[Unset, None, str]):
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):
        src (Union[Unset, None, GetTokenPriceSrc]):  Default: GetTokenPriceSrc.DEX.
        align (Union[Unset, None, GetTokenPriceAlign]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenPriceResponse]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        quote_address=quote_address,
        block_number=block_number,
        timestamp=timestamp,
        src=src,
        align=align,
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
    quote_address: Union[Unset, None, str] = UNSET,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    src: Union[Unset, None, GetTokenPriceSrc] = GetTokenPriceSrc.DEX,
    align: Union[Unset, None, GetTokenPriceAlign] = UNSET,
) -> Optional[Union[TokenErrorResponse, TokenPriceResponse]]:
    """Get token price data

     Returns price data for a token.

    Args:
        chain_id (float):
        token_address (str):
        quote_address (Union[Unset, None, str]):
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):
        src (Union[Unset, None, GetTokenPriceSrc]):  Default: GetTokenPriceSrc.DEX.
        align (Union[Unset, None, GetTokenPriceAlign]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenPriceResponse]]
    """

    return sync_detailed(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        quote_address=quote_address,
        block_number=block_number,
        timestamp=timestamp,
        src=src,
        align=align,
    ).parsed


async def asyncio_detailed(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    quote_address: Union[Unset, None, str] = UNSET,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    src: Union[Unset, None, GetTokenPriceSrc] = GetTokenPriceSrc.DEX,
    align: Union[Unset, None, GetTokenPriceAlign] = UNSET,
) -> Response[Union[TokenErrorResponse, TokenPriceResponse]]:
    """Get token price data

     Returns price data for a token.

    Args:
        chain_id (float):
        token_address (str):
        quote_address (Union[Unset, None, str]):
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):
        src (Union[Unset, None, GetTokenPriceSrc]):  Default: GetTokenPriceSrc.DEX.
        align (Union[Unset, None, GetTokenPriceAlign]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenPriceResponse]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        quote_address=quote_address,
        block_number=block_number,
        timestamp=timestamp,
        src=src,
        align=align,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    quote_address: Union[Unset, None, str] = UNSET,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    src: Union[Unset, None, GetTokenPriceSrc] = GetTokenPriceSrc.DEX,
    align: Union[Unset, None, GetTokenPriceAlign] = UNSET,
) -> Optional[Union[TokenErrorResponse, TokenPriceResponse]]:
    """Get token price data

     Returns price data for a token.

    Args:
        chain_id (float):
        token_address (str):
        quote_address (Union[Unset, None, str]):
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):
        src (Union[Unset, None, GetTokenPriceSrc]):  Default: GetTokenPriceSrc.DEX.
        align (Union[Unset, None, GetTokenPriceAlign]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenPriceResponse]]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            token_address=token_address,
            client=client,
            quote_address=quote_address,
            block_number=block_number,
            timestamp=timestamp,
            src=src,
            align=align,
        )
    ).parsed
