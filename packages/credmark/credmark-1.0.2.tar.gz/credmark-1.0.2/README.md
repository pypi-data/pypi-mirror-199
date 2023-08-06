# Credmark
An SDK for accessing Credmark Gateway

## Installation
Install using pip:

```bash
pip install credmark
```

## Usage
First, create an authenticated client. In order to access the API, you will need a key. Information about getting a key is available in our [API setup guide](https://docs.credmark.com/api-how-to-guide/).

```python
from credmark import AuthenticatedClient

client = AuthenticatedClient(api_key="<Your API Key>")
```

Now call your endpoint and use your models:

```python
from credmark.models import TokenMetadataResponse
from credmark.token_api import get_token_metadata
from credmark.types import Response

metadata: TokenMetadataResponse = get_token_metadata.sync(1, "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9", client=client)
# or if you need more info (e.g. status_code)
response: Response[TokenMetadataResponse] = get_token_metadata.sync(1, "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9", client=client)
```

Or do the same thing with an async version:

```python
from credmark.models import TokenMetadataResponse
from credmark.token_api import get_token_metadata
from credmark.types import Response

metadata: TokenMetadataResponse = await get_token_metadata.asyncio(1, "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9", client=client)
response: Response[TokenMetadataResponse] = await get_token_metadata.asyncio_detailed(1, "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9", client=client)
```

## Run a model
You can run a model using DeFi API:

```python
from credmark.defi_api import run_model
from credmark.models import RunModelDto

async def run_model_example():
    price_data = await run_model.asyncio(
        client=client,
        json_body=RunModelDto(
            chain_id=1, 
            block_number="latest", 
            slug="price.quote", 
            input={"base": {"symbol": "AAVE"}}
        ),
    )

    if price_data.error:
        print(price_data.error)
        return

    price = price_data.output['price']
    print(price)
```

## Available APIs
 - [Token API](credmark/docs/TokenAPI.md)
 - [DeFi API](credmark/docs/DeFiAPI.md)
 - [Utilities API](credmark/docs/Utilities.md)


## Things to know:
1. Every path/method combo has four functions:
    1. `sync`: Blocking request that returns parsed data (if successful) or `None`
    2. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.
    3. `asyncio`: Like `sync` but async instead of blocking
    4. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking

2. All path/query params, and bodies become method arguments.


## Advanced Usage
By default, when you're calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    api_key="SuperSecretToken",
    verify_ssl="/path/to/certificate_bundle.pem",
)
```

You can also disable certificate validation altogether, but beware that **this is a security risk**.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    api_key="SuperSecretToken", 
    verify_ssl=False
)
```

There are more settings on the generated `Client` class which let you control more runtime behavior, check out the docstring on that class for more info.
