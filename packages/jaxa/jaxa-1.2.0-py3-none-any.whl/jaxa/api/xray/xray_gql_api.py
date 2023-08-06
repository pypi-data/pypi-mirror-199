"""
Jira XRay GQL API
"""
from pathlib import Path
from typing import Optional, Union

from gql import Client, gql
from gql.transport import Transport

from ...api.xray.xray_categories import (
    GQLTestExecution,
    GQLTestPlan,
    GQLTestRun,
    GQLTests,
    GQLTestSets,
    GQLTestStatus,
)


class XRayGQLClient:
    """XRay GraphQL Client"""

    def __init__(
        self,
        *,
        transport_layer: Optional[Transport] = None,
        fetch_schema_from_transport: bool = False,
    ) -> None:
        # Create a GraphQL client using the defined transport
        self.gql_cli = Client(
            transport=transport_layer,
            fetch_schema_from_transport=fetch_schema_from_transport,
        )

    def execute_query(self, query: str, variables: Optional[dict] = None) -> dict:
        return self.gql_cli.execute(gql(query), variable_values=variables)

    @staticmethod
    def load_query_from_file(path: Union[Path, str]) -> str:
        with open(path) as f:
            return f.read()

    @property
    def tests(self):
        """
        Perform the actual call and return response
        """
        return GQLTests(self)

    @property
    def test_plan(self):
        """
        Perform the actual call and return response
        """
        return GQLTestPlan(self)

    @property
    def test_executions(self):
        """
        Perform the actual call and return response
        """
        return GQLTestExecution(self)

    @property
    def test_runs(self):
        """
        Perform the actual call and return response
        """
        return GQLTestRun(self)

    @property
    def test_sets(self):
        """
        Perform the actual call and return response
        """
        return GQLTestSets(self)

    @property
    def test_statuses(self):
        """ """
        return GQLTestStatus(self)
