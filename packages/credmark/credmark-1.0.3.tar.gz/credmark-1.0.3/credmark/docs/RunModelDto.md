# RunModelDto


## Properties
Name | Type | Description
------------ | ------------- | -------------
slug | str | slug of the model to run
chain_id | int | chainId number, for example 1 for mainnet
block_number | Union[RunModelDtoBlockNumberType1, int] | blockNumber is a number or a string with a number, 'latest', 'earliest', or 'pending'
input | Dict[str, Any] | Model input data
version | Union[Unset, str] | Typically not required but you may specify version of the model to run

