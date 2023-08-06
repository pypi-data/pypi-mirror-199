"""
Jira And Xray API Client
"""
import logging
import os
from typing import Optional

from gql.transport.requests import RequestsHTTPTransport

from jaxa.api.jira import JiraRESTClient
from jaxa.api.xray import XRayGQLClient, XRayRESTClient

log = logging.getLogger("jaxa")
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("gql.transport.requests").setLevel(logging.CRITICAL)


class JAXAClient:
    """JAXA Client uses both XRay REST and XRay GraphQL apis"""

    def __init__(self, **kwargs):
        self.auth_token = None

        # Initialise JIra REST API
        self._init_jira_rest_api_client()

        # Initialise Xray REST API
        self._init_xray_rest_api_client()

        # Initialise Xray GraphQL API
        self._init_xray_graphql_api_client()

        # The issue is if token times out how to refresh and set it again
        # I think i need to check it but for now work on assumption it does not expire!

    def _init_jira_rest_api_client(self):
        log.debug("Initialising internal Jira REST api client")
        self._jira = JiraRESTClient(url=os.environ["JAXA_JIRA_BASEURL"])

    def _init_xray_rest_api_client(self):
        log.debug("Initialising internal XRay REST api client")
        self._rest = XRayRESTClient(url=os.environ["JAXA_XRAY_BASEURL"])

    def _init_xray_graphql_api_client(
        self,
    ):
        log.debug("Initialising internal XRay GQL api client")
        self._gql_headers = self.gql_auth_header(
            client_id=os.environ["JAXA_JIRA_CLIENT_ID"],
            client_secret=os.environ["JAXA_JIRA_CLIENT_SECRET"],
        )

        self._transport = RequestsHTTPTransport(
            url=os.environ["JAXA_XRAY_BASEURL"] + "/graphql", headers=self._gql_headers
        )
        self._xray_qgl = XRayGQLClient(transport_layer=self._transport)

    @property
    def jira(self):
        return self._jira

    @property
    def xray_rest(self):
        return self._rest

    @property
    def xray_gql(self):
        return self._xray_qgl

    def gql_auth_header(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ):
        self.auth_token = self._rest.authenticate.get_auth_token(
            client_id=client_id, client_secret=client_secret
        )
        return {"Authorization": f"Bearer {self.auth_token}"}
