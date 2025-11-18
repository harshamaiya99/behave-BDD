Feature: Create User API

  Scenario Outline: Verify POST/users creates user successfully
    Given baseURL "https://jsonplaceholder.typicode.com"
    And payload:
      """
      {
        "name": "<name>",
        "username": "<username>",
        "email": "<email>"
      }
      """
    When POST "/users"
    Then status code = <status_code>
    And the response field "name" should be "<name>"
    And the response field "username" should be "<username>"
    And the response field "email" should be "<email>"

    Examples:
      | name     | username | email            | status_code |
      | Harsha   | maiya    | harsha@test.com  | 201         |
      | John Doe | johnd    | john@example.com | 201         |
