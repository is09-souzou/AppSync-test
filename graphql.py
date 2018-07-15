# -*- coding: utf-8 -*-

"""
    graphql.py

    GraphQL client Class
    support version: Python 3.6.5
"""

import json
import urllib


class GraphQL:
    def __init__(self, url, jwt_token):
        """ __init__

            @param url      : GraphQL Endpoint URL
            @param jwt_token: jwt token
        """
        self.url       = url
        self.jwt_token = jwt_token

    def graphql_request(self, query, variables, operation_name=None):
        """ graphql_request

            @param query         : GraphQL request query
            @param variables     : GraphQL request variables
            @param operation_name: GraphQL request operation_name
        """

        obj = {
            "operationName": operation_name,
            "query"        : query,
            "variables"    : variables
        }
        json_data = json.dumps(obj).encode("utf-8")
        headers = {
            "Content-Type" : "application/json",
            "Authorization": self.jwt_token
        }

        request = urllib.request.Request(
            self.url,
            data=json_data,
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            result = json.loads(response_body.split('\n')[0])
            return {
                "status": response.status,
                "body"  : result
            }
