from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ..models.token_balance_response import TokenBalanceResponse
from ..models.token_error_response import TokenErrorResponse
from ..types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    account_address: str,
    quote_address: Union[Unset, None, str] = UNSET,
    scaled: Union[Unset, None, bool] = True,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v1/tokens/{chainId}/{tokenAddress}/balance".format(
        client.base_url, chainId=chain_id, tokenAddress=token_address
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["accountAddress"] = account_address

    params["quoteAddress"] = quote_address

    params["scaled"] = scaled

    params["blockNumber"] = block_number

    params["timestamp"] = timestamp

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
) -> Optional[Union[TokenBalanceResponse, TokenErrorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TokenBalanceResponse.from_dict(response.json())

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
) -> Response[Union[TokenBalanceResponse, TokenErrorResponse]]:
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
    account_address: str,
    quote_address: Union[Unset, None, str] = UNSET,
    scaled: Union[Unset, None, bool] = True,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
) -> Response[Union[TokenBalanceResponse, TokenErrorResponse]]:
    """Get token balance

     Returns token balance for an account.

    Args:
        chain_id (float):
        token_address (str):
        account_address (str):
        quote_address (Union[Unset, None, str]):
        scaled (Union[Unset, None, bool]):  Default: True.
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenBalanceResponse, TokenErrorResponse]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        account_address=account_address,
        quote_address=quote_address,
        scaled=scaled,
        block_number=block_number,
        timestamp=timestamp,
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
    account_address: str,
    quote_address: Union[Unset, None, str] = UNSET,
    scaled: Union[Unset, None, bool] = True,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
) -> Optional[Union[TokenBalanceResponse, TokenErrorResponse]]:
    """Get token balance

     Returns token balance for an account.

    Args:
        chain_id (float):
        token_address (str):
        account_address (str):
        quote_address (Union[Unset, None, str]):
        scaled (Union[Unset, None, bool]):  Default: True.
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenBalanceResponse, TokenErrorResponse]]
    """

    return sync_detailed(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        account_address=account_address,
        quote_address=quote_address,
        scaled=scaled,
        block_number=block_number,
        timestamp=timestamp,
    ).parsed


async def asyncio_detailed(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    account_address: str,
    quote_address: Union[Unset, None, str] = UNSET,
    scaled: Union[Unset, None, bool] = True,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
) -> Response[Union[TokenBalanceResponse, TokenErrorResponse]]:
    """Get token balance

     Returns token balance for an account.

    Args:
        chain_id (float):
        token_address (str):
        account_address (str):
        quote_address (Union[Unset, None, str]):
        scaled (Union[Unset, None, bool]):  Default: True.
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenBalanceResponse, TokenErrorResponse]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        account_address=account_address,
        quote_address=quote_address,
        scaled=scaled,
        block_number=block_number,
        timestamp=timestamp,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    account_address: str,
    quote_address: Union[Unset, None, str] = UNSET,
    scaled: Union[Unset, None, bool] = True,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
) -> Optional[Union[TokenBalanceResponse, TokenErrorResponse]]:
    """Get token balance

     Returns token balance for an account.

    Args:
        chain_id (float):
        token_address (str):
        account_address (str):
        quote_address (Union[Unset, None, str]):
        scaled (Union[Unset, None, bool]):  Default: True.
        block_number (Union[Unset, None, float]):
        timestamp (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenBalanceResponse, TokenErrorResponse]]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            token_address=token_address,
            client=client,
            account_address=account_address,
            quote_address=quote_address,
            scaled=scaled,
            block_number=block_number,
            timestamp=timestamp,
        )
    ).parsed
