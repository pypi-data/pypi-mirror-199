"""
Jira REST API
"""
import os

from ..jira import jira_categories as JiraCategories
from ..rest.session import RESTSession


class JiraRESTClient(RESTSession):
    """Jira REST API Client"""

    def add_authorisation(self) -> None:
        self.set_basic_auth(
            username=os.environ["JAXA_JIRA_USERNAME"],
            password=os.environ["JAXA_JIRA_APITOKEN"],
        )

    @property
    def labels(self) -> JiraCategories.JiraLabels:
        """ """
        self.add_authorisation()
        return JiraCategories.JiraLabels(self)

    @property
    def customfieldlist(self) -> JiraCategories.JiraCustomFieldList:
        """ """
        self.add_authorisation()
        return JiraCategories.JiraCustomFieldList(self)

    @property
    def fields(self) -> JiraCategories.JiraFields:
        """ """
        self.add_authorisation()
        return JiraCategories.JiraFields(self)

    @property
    def issues(self) -> JiraCategories.JiraIssues:
        """ """
        self.add_authorisation()
        return JiraCategories.JiraIssues(self)

    @property
    def links(self) -> JiraCategories.JiraLinks:
        """ """
        self.add_authorisation()
        return JiraCategories.JiraLinks(self)

    @property
    def search(self) -> JiraCategories.JiraSearch:
        """ """
        self.add_authorisation()
        return JiraCategories.JiraSearch(self)
