import json
import requests

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

        return json.loads(r.content)
    def projects(self):
        projects = self.query_grapql(
            """
                query Project {projects{nodes{id,name}}}
            """
        )

        return projects["data"]["projects"]

