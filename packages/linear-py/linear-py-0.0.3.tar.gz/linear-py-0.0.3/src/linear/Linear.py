import json
import requests

from .Exceptions import LinearQueryException

class Linear:
    def __init__(self, LINEAR_API_KEY=''):
        self.set_url('https://api.linear.app/graphql')
        self.set_api_key(LINEAR_API_KEY)
        self.headers = {
            "Authorization" : self.LINEAR_API_KEY
        }
        pass

    def set_url(self, url):
        self.graphql_url = url

    def set_api_key(self, LINEAR_API_KEY):
        self.LINEAR_API_KEY = LINEAR_API_KEY

    def query_grapql(self, query):
        r = requests.post(self.graphql_url, json={
            "query": query
        }, headers=self.headers)

        response = json.loads(r.content)

        if 'errors' in response:
            raise LinearQueryException(response["errors"])

        return response

    def query_basic_resource(self, resource=''):
        resource_response = self.query_grapql(
            """
                query Resource {"""+resource+"""{nodes{id,name}}}
            """
        )

        return resource_response["data"][resource]["nodes"]

    def create_issue(self, project=''):
        pass

    def teams(self):
        return self.query_basic_resource('teams')

    def states(self):
        return self.query_basic_resource('workflowStates')

    def projects(self):
        return self.query_basic_resource('projects')

