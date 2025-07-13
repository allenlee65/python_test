import requests
from behave import given, when, then

API_URL = "https://uat-api.3ona.co/exchange/v1/public/get-risk-parameters"  # Replace {URL} with your actual endpoint

@given('the risk parameters API endpoint is available')
def step_given_api_endpoint(context):
    context.api_url = API_URL

@when('I request risk parameters')
def step_when_request_risk_parameters(context):
    response = requests.get(context.api_url)
    context.status_code = response.status_code
    context.response_json = response.json()

@then('the HTTP status code should be 200')
def step_then_status_code(context):
    assert context.status_code == 200, f"Expected 200, got {context.status_code}"

@then('the response has required fields: id, method, code, and result')
def step_then_required_fields(context):
    data = context.response_json
    assert isinstance(data, dict), "Response is not a JSON object"
    for key in ['id', 'method', 'code', 'result']:
        assert key in data, f"Missing required field: {key}"

@then('the result object contains the expected fields')
def step_then_result_fields(context):
    result = context.response_json.get('result')
    assert isinstance(result, dict), "'result' is not an object"
    expected_keys = [
        'default_max_product_leverage_for_spot',
        'default_max_product_leverage_for_perps',
        'default_max_product_leverage_for_futures',
        'default_unit_margin_rate',
        'default_collateral_cap',
        'update_timestamp_ms',
        'base_currency_config'
    ]
    assert set(result.keys()) == set(expected_keys), (
        f"'result' keys mismatch. Expected: {expected_keys}, Got: {list(result.keys())}"
    )

@then('the update timestamp must be a non-negative integer')
def step_then_update_timestamp(context):
    result = context.response_json.get('result')
    ts = result.get('update_timestamp_ms')
    assert isinstance(ts, int) and ts >= 0, f"update_timestamp_ms must be a non-negative integer, got {ts}"

@then('the base currency config is a non-empty array with required fields in each item')
def step_then_base_currency_config(context):
    result = context.response_json.get('result')
    config = result.get('base_currency_config')
    assert isinstance(config, list) and len(config) > 0, "base_currency_config is not a non-empty array"
    required_fields = [
        'instrument_name',
        #'minimum_haircut',
        #'unit_margin_rate',
        #'order_limit',
        #'max_order_notional_usd'
    ]
    for item in config:
        assert isinstance(item, dict), "Item in base_currency_config is not an object"
        for field in required_fields:
            assert field in item, f"Missing field '{field}' in base_currency_config item"
            assert isinstance(item[field], str), f"Field '{field}' must be a string in base_currency_config"
