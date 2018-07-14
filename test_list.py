# -*- coding: utf-8 -*-

"""
    test_list.py

    AWS AppSync Portal Test List

    support version: Python 3.6.5
"""

def get_test_list(id):
    """ get_test_list

        @param id: Portal user id
    """
    print(id)
    return [
        {
            "name": "Reset",
            "queries": [
                {
                    "name": "getUser",
                    "query": """
                        query ($id: ID!) {
                            getUser(id: $id) {
                                id
                                email
                                displayName
                                career
                                avatarUri
                                message
                                works {
                                    id
                                }
                                __typename
                            }
                        }
                    """,
                    "variables": {
                        "id": id
                    },
                    "operation_name": None
                },
                {
                    "name": "listWorks",
                    "query": """
                        query ($id: ID!) {
                            getUser(id: $id) {
                                id
                                email
                                displayName
                                __typename
                            }
                        }
                    """,
                    "variables": {
                        "id": id
                    },
                    "operation_name": None
                },
            ],
        }
    ]
