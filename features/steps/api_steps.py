import json
import requests
import allure
from behave import given, when, then

@given('baseURL "{base_url}"')
def step_impl_base_url(context, base_url):
    context.base_url = base_url


@given('payload:')
def step_impl_payload(context):
    context.payload = json.loads(context.text)

    # Attach payload
    allure.attach(
        json.dumps(context.payload, indent=2),
        name="REQUEST PAYLOAD",
        attachment_type=allure.attachment_type.JSON
    )


@when('POST "{endpoint}"')
def step_impl_post(context, endpoint):
    url = context.base_url + endpoint

    headers = {"Content-Type": "application/json"}
    context.response = requests.post(url, json=context.payload, headers=headers)

    # Attach request details
    allure.attach(url, name="REQUEST URL", attachment_type=allure.attachment_type.TEXT)
    allure.attach(json.dumps(headers, indent=2), name="REQUEST HEADERS", attachment_type=allure.attachment_type.JSON)

    # Attach response details
    try:
        response_body = json.dumps(context.response.json(), indent=2)
    except ValueError:
        response_body = context.response.text

    allure.attach(str(context.response.status_code), name="STATUS CODE", attachment_type=allure.attachment_type.TEXT)
    allure.attach(json.dumps(dict(context.response.headers), indent=2),
                  name="RESPONSE HEADERS", attachment_type=allure.attachment_type.JSON)
    allure.attach(response_body, name="RESPONSE BODY", attachment_type=allure.attachment_type.JSON)


@then('status code = {status_code:d}')
def step_impl_status(context, status_code):
    assert context.response.status_code == status_code


@then('the response field "{field}" should be "{expected_value}"')
def step_impl_field_str(context, field, expected_value):
    body = context.response.json()
    assert body.get(field) == expected_value
