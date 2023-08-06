from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ..models.token_error_response import TokenErrorResponse
from ..models.token_total_supply_historical_response import TokenTotalSupplyHistoricalResponse
from ..types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    scaled: Union[Unset, None, bool] = True,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v1/tokens/{chainId}/{tokenAddress}/total-supply/historical".format(
        client.base_url, chainId=chain_id, tokenAddress=token_address
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["scaled"] = scaled

    params["startBlockNumber"] = start_block_number

    params["endBlockNumber"] = end_block_number

    params["blockInterval"] = block_interval

    params["startTimestamp"] = start_timestamp

    params["endTimestamp"] = end_timestamp

    params["timeInterval"] = time_interval

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
) -> Optional[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TokenTotalSupplyHistoricalResponse.from_dict(response.json())

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
) -> Response[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]:
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
    scaled: Union[Unset, None, bool] = True,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
) -> Response[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]:
    """Get historical total supply

     Returns historical total supply for a token.

    Args:
        chain_id (float):
        token_address (str):
        scaled (Union[Unset, None, bool]):  Default: True.
        start_block_number (Union[Unset, None, float]):
        end_block_number (Union[Unset, None, float]):
        block_interval (Union[Unset, None, float]):
        start_timestamp (Union[Unset, None, float]):
        end_timestamp (Union[Unset, None, float]):
        time_interval (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        scaled=scaled,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        block_interval=block_interval,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        time_interval=time_interval,
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
    scaled: Union[Unset, None, bool] = True,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
) -> Optional[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]:
    """Get historical total supply

     Returns historical total supply for a token.

    Args:
        chain_id (float):
        token_address (str):
        scaled (Union[Unset, None, bool]):  Default: True.
        start_block_number (Union[Unset, None, float]):
        end_block_number (Union[Unset, None, float]):
        block_interval (Union[Unset, None, float]):
        start_timestamp (Union[Unset, None, float]):
        end_timestamp (Union[Unset, None, float]):
        time_interval (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]
    """

    return sync_detailed(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        scaled=scaled,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        block_interval=block_interval,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        time_interval=time_interval,
    ).parsed


async def asyncio_detailed(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    scaled: Union[Unset, None, bool] = True,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
) -> Response[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]:
    """Get historical total supply

     Returns historical total supply for a token.

    Args:
        chain_id (float):
        token_address (str):
        scaled (Union[Unset, None, bool]):  Default: True.
        start_block_number (Union[Unset, None, float]):
        end_block_number (Union[Unset, None, float]):
        block_interval (Union[Unset, None, float]):
        start_timestamp (Union[Unset, None, float]):
        end_timestamp (Union[Unset, None, float]):
        time_interval (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        scaled=scaled,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        block_interval=block_interval,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        time_interval=time_interval,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: float,
    token_address: str,
    *,
    client: AuthenticatedClient,
    scaled: Union[Unset, None, bool] = True,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
) -> Optional[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]:
    """Get historical total supply

     Returns historical total supply for a token.

    Args:
        chain_id (float):
        token_address (str):
        scaled (Union[Unset, None, bool]):  Default: True.
        start_block_number (Union[Unset, None, float]):
        end_block_number (Union[Unset, None, float]):
        block_interval (Union[Unset, None, float]):
        start_timestamp (Union[Unset, None, float]):
        end_timestamp (Union[Unset, None, float]):
        time_interval (Union[Unset, None, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            token_address=token_address,
            client=client,
            scaled=scaled,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
        )
    ).parsed
