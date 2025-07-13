import requests
from behave import given, when, then

API_URL = "https://uat-api.3ona.co/exchange/v1/public/get-instruments"  # Replace {URL} with your actual endpoint

@given('the instruments API endpoint is available')
def step_given_api_endpoint(context):
    context.api_url = API_URL

@when('I request the instruments data')
def step_when_request_instruments(context):
    response = requests.get(context.api_url)
    context.status_code = response.status_code
    context.response_time = response.elapsed.total_seconds() * 1000  # ms
    context.response_json = response.json()


@then('the response time should be less than 500 ms')
def step_then_response_time(context):
    assert context.response_time < 500, f"Response time {context.response_time:.2f}ms exceeds 200ms"

@then('the response contains required fields: id, method, code, and result')
def step_then_required_fields(context):
    data = context.response_json
    assert isinstance(data, dict), "Response is not a JSON object"
    for key in ['id', 'method', 'code', 'result']:
        assert key in data, f"Missing required field: {key}"

@then('the result.data array and its elements have the correct structure')
def step_then_result_data_structure(context):
    data = context.response_json
    result = data.get('result')
    assert isinstance(result, dict), "result is not an object"
    assert 'data' in result, "result does not contain 'data'"
    assert isinstance(result['data'], list), "'data' is not an array"

    required_keys = [
        'symbol', 'inst_type', 'display_name', 'base_ccy', 'quote_ccy', 'quote_decimals',
        'quantity_decimals', 'price_tick_size', 'qty_tick_size', 'max_leverage', 'tradable',
        'expiry_timestamp_ms', 'beta_product', 'margin_buy_enabled', 'margin_sell_enabled'
    ]

    for item in result['data']:
        assert isinstance(item, dict), "Element in data is not an object"
        for key in required_keys:
            assert key in item, f"Missing key '{key}' in item"
        assert isinstance(item['symbol'], str)
        assert isinstance(item['inst_type'], str)
        assert isinstance(item['display_name'], str)
        assert isinstance(item['base_ccy'], str)
        assert isinstance(item['quote_ccy'], str)
        assert isinstance(item['quote_decimals'], (int, float))
        assert isinstance(item['quantity_decimals'], (int, float))
        assert isinstance(item['price_tick_size'], str)
        assert isinstance(item['qty_tick_size'], str)
        # max_leverage can be string or empty
        assert isinstance(item['max_leverage'], str) or item['max_leverage'] == ""
        assert isinstance(item['tradable'], bool)
        assert isinstance(item['expiry_timestamp_ms'], (int, float))
        assert isinstance(item['beta_product'], bool)
        # underlying_symbol and contract_size can be string or empty
        # assert isinstance(item['underlying_symbol'], str) or item['underlying_symbol'] == ""
        # assert isinstance(item['contract_size'], str) or item['contract_size'] == ""
        assert isinstance(item['margin_buy_enabled'], bool)
        assert isinstance(item['margin_sell_enabled'], bool)

@then('each instrument\'s "tradable" property must be a boolean')
def step_then_tradable_boolean(context):
    data = context.response_json
    instruments = data.get('result', {}).get('data', [])
    assert isinstance(instruments, list) and len(instruments) > 0, "No instruments found"
    for instrument in instruments:
        assert 'tradable' in instrument, "Missing 'tradable' field"
        assert isinstance(instrument['tradable'], bool), "'tradable' is not a boolean"
