# Token API


Method | HTTP Request | Description
------------- | ------------- | -------------
[**get_token_metadata**](#get_token_metadata) | GET /v1/tokens/{chainId}/{tokenAddress} | Returns metadata for a token.
[**get_token_name**](#get_token_name) | GET /v1/tokens/{chainId}/{tokenAddress}/name | Returns name of a token.
[**get_token_symbol**](#get_token_symbol) | GET /v1/tokens/{chainId}/{tokenAddress}/symbol | Returns symbol of a token.
[**get_token_decimals**](#get_token_decimals) | GET /v1/tokens/{chainId}/{tokenAddress}/decimals | Returns decimals of a token.
[**get_token_total_supply**](#get_token_total_supply) | GET /v1/tokens/{chainId}/{tokenAddress}/total-supply | Returns total supply of a token.
[**get_token_total_supply_historical**](#get_token_total_supply_historical) | GET /v1/tokens/{chainId}/{tokenAddress}/total-supply/historical | Returns historical total supply for a token.
[**get_token_logo**](#get_token_logo) | GET /v1/tokens/{chainId}/{tokenAddress}/logo | Returns logo of a token.
[**get_token_creation_block**](#get_token_creation_block) | GET /v1/tokens/{chainId}/{tokenAddress}/creation-block | Returns creation block number of a token.
[**get_token_abi**](#get_token_abi) | GET /v1/tokens/{chainId}/{tokenAddress}/abi | Returns ABI of a token.
[**get_token_price**](#get_token_price) | GET /v1/tokens/{chainId}/{tokenAddress}/price | Returns price data for a token.
[**get_token_price_historical**](#get_token_price_historical) | GET /v1/tokens/{chainId}/{tokenAddress}/price/historical | Returns historical price data for a token.
[**get_token_balance**](#get_token_balance) | GET /v1/tokens/{chainId}/{tokenAddress}/balance | Returns token balance for an account.
[**get_token_balance_historical**](#get_token_balance_historical) | GET /v1/tokens/{chainId}/{tokenAddress}/balance/historical | Returns historical token balance for an account.
[**get_token_volume**](#get_token_volume) | GET /v1/tokens/{chainId}/{tokenAddress}/volume | Returns traded volume for a token over a period of blocks or time.
[**get_token_volume_historical**](#get_token_volume_historical) | GET /v1/tokens/{chainId}/{tokenAddress}/volume/historical | Returns traded volume for a token over a period of blocks or time divided by intervals.
[**get_token_holders**](#get_token_holders) | GET /v1/tokens/{chainId}/{tokenAddress}/holders | Returns holders of a token at a block or time.
[**get_token_holders_count**](#get_token_holders_count) | GET /v1/tokens/{chainId}/{tokenAddress}/holders/count | Returns total number of holders of a token at a block or time.


# **get_token_metadata**

Get token metadata

 Returns metadata for a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
block_number | float | None
timestamp | float | None


### Response Type
Union[TokenErrorResponse, TokenMetadataResponse]

# **get_token_name**

Get token name

 Returns name of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
block_number | float | None
timestamp | float | None


### Response Type
Union[TokenErrorResponse, TokenNameResponse]

# **get_token_symbol**

Get token symbol

 Returns symbol of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
block_number | float | None
timestamp | float | None


### Response Type
Union[TokenErrorResponse, TokenSymbolResponse]

# **get_token_decimals**

Get token decimals

 Returns decimals of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
block_number | float | None
timestamp | float | None


### Response Type
Union[TokenDecimalsResponse, TokenErrorResponse]

# **get_token_total_supply**

Get token's total supply

 Returns total supply of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
block_number | float | None
timestamp | float | None
scaled | bool | None


### Response Type
Union[TokenErrorResponse, TokenTotalSupplyResponse]

# **get_token_total_supply_historical**

Get historical total supply

 Returns historical total supply for a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
scaled | bool | None
start_block_number | float | None
end_block_number | float | None
block_interval | float | None
start_timestamp | float | None
end_timestamp | float | None
time_interval | float | None


### Response Type
Union[TokenErrorResponse, TokenTotalSupplyHistoricalResponse]

# **get_token_logo**

Get token logo

 Returns logo of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
block_number | float | None
timestamp | float | None


### Response Type
Union[TokenErrorResponse, TokenLogoResponse]

# **get_token_creation_block**

Get token creation block

 Returns creation block number of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
block_number | float | None
timestamp | float | None


### Response Type
Union[TokenCreationBlockResponse, TokenErrorResponse]

# **get_token_abi**

Get token ABI

 Returns ABI of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
block_number | float | None
timestamp | float | None


### Response Type
Union[TokenAbiResponse, TokenErrorResponse]

# **get_token_price**

Get token price data

 Returns price data for a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
quote_address | str | None
block_number | float | None
timestamp | float | None
src | GetTokenPriceSrc | None
align | GetTokenPriceAlign | None


### Response Type
Union[TokenErrorResponse, TokenPriceResponse]

# **get_token_price_historical**

Get historical price

 Returns historical price data for a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
quote_address | str | None
src | GetTokenPriceHistoricalSrc | None
start_block_number | float | None
end_block_number | float | None
block_interval | float | None
start_timestamp | float | None
end_timestamp | float | None
time_interval | float | None


### Response Type
Union[TokenErrorResponse, TokenPriceHistoricalResponse]

# **get_token_balance**

Get token balance

 Returns token balance for an account.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
account_address | str | None
quote_address | str | None
scaled | bool | None
block_number | float | None
timestamp | float | None


### Response Type
Union[TokenBalanceResponse, TokenErrorResponse]

# **get_token_balance_historical**

Get historical balance

 Returns historical token balance for an account.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
account_address | str | None
quote_address | str | None
scaled | bool | None
start_block_number | float | None
end_block_number | float | None
block_interval | float | None
start_timestamp | float | None
end_timestamp | float | None
time_interval | float | None


### Response Type
Union[TokenBalanceHistoricalResponse, TokenErrorResponse]

# **get_token_volume**

Get token volume

 Returns traded volume for a token over a period of blocks or time.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
scaled | bool | None
start_block_number | float | None
end_block_number | float | None
start_timestamp | float | None
end_timestamp | float | None


### Response Type
Union[TokenErrorResponse, TokenVolumeResponse]

# **get_token_volume_historical**

Get historical volume

 Returns traded volume for a token over a period of blocks or time divided by intervals.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
scaled | bool | None
start_block_number | float | None
end_block_number | float | None
start_timestamp | float | None
end_timestamp | float | None
block_interval | float | None
time_interval | float | None


### Response Type
Union[TokenErrorResponse, TokenVolumeHistoricalResponse]

# **get_token_holders**

Get token holders

 Returns holders of a token at a block or time.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
page_size | float | None
cursor | str | None
quote_address | str | None
scaled | bool | None
block_number | float | None
timestamp | float | None


### Response Type
Union[TokenErrorResponse, TokenHoldersResponse]

# **get_token_holders_count**

Get total number of token holders

 Returns total number of holders of a token at a block or time.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | None
token_address | str | None
block_number | float | None
timestamp | float | None


### Response Type
Union[TokenErrorResponse, TokenHoldersCountResponse]

