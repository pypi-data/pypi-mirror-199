"""
Jira XRay REST API
"""

from ...api.rest.session import RESTSession
from ...api.xray import xray_categories as XRayCategories


class XRayRESTClient(RESTSession):
    """XRay REST Client"""

    @property
    def authenticate(self) -> XRayCategories.Authenticate:
        """
        https://xray.cloud.getxray.app/api/v1/authenticate
        Use the following API methods to authenticate.
        """
        return XRayCategories.Authenticate(self)
