# JAXA - Jira And Xray API

This is not intended to be a fully functioning complete API client module for Jira & Xray.
One day it may be.
For now it merely meets the criteria I need it to offer.

## Configuration

### Environment Variable Configuration

| Environment Variable    | Description                                                    |
|-------------------------|----------------------------------------------------------------|
| JAXA_JIRA_BASEURL       | URL for Jira Cloud. E.g. https://example.atlassian.net         |
| JAXA_JIRA_USERNAME      | Email address of user for connecting to Jira                   |
| JAXA_JIRA_APITOKEN      | API Token of user for connecting to Jira                       |
| JAXA_JIRA_CLIENT_ID     | Client ID for accessing Jira Xray                              |
| JAXA_JIRA_CLIENT_SECRET | Client Secret for accessing Jira Xray                          |
| JAXA_XRAY_BASEURL       | URL for XRay Cloud. E.g. https://xray.cloud.getxray.app/api/v1 |
| JAXA_PROJECT_ID         | ID of Jira Project                                             |
| JAXA_PROJECT_NAME       | Name of Jira Project                                           |

## Usage


## Tests

**Warning: These tests will create tickets in Jira**

```shell
# Run all functional tests against supported python versions via nox
poetry run run-tests

#
poetry run nox -s functional_tests-3.8

poetry run nox -s jira_issues-3.8
```
