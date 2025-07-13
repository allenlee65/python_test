Feature: Validate instruments API response

  Background:
    Given the instruments API endpoint is available

  Scenario: Validate response status, time, and structure
    When I request the instruments data
    Then the HTTP status code should be 200
    And the response time should be less than 500 ms
    And the response contains required fields: id, method, code, and result
    And the result.data array and its elements have the correct structure
    And each instrument's "tradable" property must be a boolean
