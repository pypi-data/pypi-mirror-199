# Utilities


Method | HTTP Request | Description
------------- | ------------- | -------------
[**check_health**](#check_health) | GET /health | 
[**get_daily_model_usage**](#get_daily_model_usage) | GET /v1/usage/requests | Returns a list of daily model request statistics, either for a specific requester or for everyone.
[**get_top_models**](#get_top_models) | GET /v1/usage/top | Returns a list of the top used models.
[**get_total_model_usage**](#get_total_model_usage) | GET /v1/usage/total | Returns a count of model runs.


# **check_health**

Healthcheck status



### Response Type
Union[CheckHealthResponse200, CheckHealthResponse503]

# **get_daily_model_usage**

Model Request statistics

 Returns a list of daily model request statistics, either for a specific requester or for everyone.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
days | float | None
group_by | str | None
requester | str | None


### Response Type
List[Dict[str, Any]]

# **get_top_models**

Top Used Models

 Returns a list of the top used models.



### Response Type
List[Dict[str, Any]]

# **get_total_model_usage**

Total Model Usage

 Returns a count of model runs.



### Response Type
List[Dict[str, Any]]

