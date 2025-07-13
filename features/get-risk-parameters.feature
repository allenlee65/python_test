Feature: Validate risk parameters API response

  Background:
    Given the risk parameters API endpoint is available

  Scenario: Validate response status and structure
    When I request risk parameters
    Then the HTTP status code should be 200
    And the response has required fields: id, method, code, and result
    And the result object contains the expected fields
    And the update timestamp must be a non-negative integer
    And the base currency config is a non-empty array with required fields in each item
