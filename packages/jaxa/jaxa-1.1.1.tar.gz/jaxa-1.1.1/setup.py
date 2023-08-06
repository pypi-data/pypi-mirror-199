# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jaxa',
 'jaxa.api',
 'jaxa.api.common',
 'jaxa.api.jira',
 'jaxa.api.rest',
 'jaxa.api.xray']

package_data = \
{'': ['*'],
 'jaxa.api.xray': ['gql_templates/testexecutions/*',
                   'gql_templates/testplans/*',
                   'gql_templates/testruns/*',
                   'gql_templates/tests/*',
                   'gql_templates/testsets/*',
                   'gql_templates/teststatuses/*',
                   'gql_templates/teststeps/*']}

install_requires = \
['gql>=3.4.0,<4.0.0', 'requests-toolbelt>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['prep-dev-release = scripts.release_process:prep_dev',
                     'prep-major-release = scripts.release_process:prep_major',
                     'prep-minor-release = scripts.release_process:prep_minor',
                     'prep-patch-release = scripts.release_process:prep_patch',
                     'release = scripts.release_process:upload_release',
                     'run-tests = scripts.dev_process:run_tests']}

setup_kwargs = {
    'name': 'jaxa',
    'version': '1.1.1',
    'description': 'Jira and Xray API',
    'long_description': '# JAXA - Jira And Xray API\n\nThis is not intended to be a fully functioning complete API client module for Jira & Xray.\nOne day it may be.\nFor now it merely meets the criteria I need it to offer.\n\n## Configuration\n\n### Environment Variable Configuration\n\n| Environment Variable    | Description                                                    |\n|-------------------------|----------------------------------------------------------------|\n| JAXA_JIRA_BASEURL       | URL for Jira Cloud. E.g. https://example.atlassian.net         |\n| JAXA_JIRA_USERNAME      | Email address of user for connecting to Jira                   |\n| JAXA_JIRA_APITOKEN      | API Token of user for connecting to Jira                       |\n| JAXA_JIRA_CLIENT_ID     | Client ID for accessing Jira Xray                              |\n| JAXA_JIRA_CLIENT_SECRET | Client Secret for accessing Jira Xray                          |\n| JAXA_XRAY_BASEURL       | URL for XRay Cloud. E.g. https://xray.cloud.getxray.app/api/v1 |\n| JAXA_PROJECT_ID         | ID of Jira Project                                             |\n| JAXA_PROJECT_NAME       | Name of Jira Project                                           |\n\n## Usage\n\n\n## Tests\n\n**Warning: These tests will create tickets in Jira**\n\n```shell\n# Run all functional tests against supported python versions via nox\npoetry run run-tests\n\n#\npoetry run nox -s functional_tests-3.8\n\npoetry run nox -s jira_issues-3.8\n```\n',
    'author': 'Gleams API user',
    'author_email': 'Stephen.Swannell+ghapi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
