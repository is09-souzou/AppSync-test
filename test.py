# -*- coding: utf-8 -*-

"""
    test.py

    AWS AppSync Portal Test

    support version: Python 3.6.5
"""

from inspect import signature

from bcolors import bcolors


class Test:

    def get_test_list(self):
        return [
            {
                "name": "test",
                "exec": lambda: self.test_user()
            },
        ]

    def __init__(self, user_id, client):
        """ __init__

            @param user_id: Portal user id
            @param client : GraphQL client
        """
        self.user_id = user_id
        self.client = client

    def execute_test(self):
        """ execute_test

        """

        test_list = self.get_test_list()
        errors = []

        for test_index, test in enumerate(test_list):
            print(f"[{test_index + 1}/{len(test_list)}] {bcolors.UNDERLINE}{test['name']}{bcolors.ENDC}")
            error = test["exec"]()
            if (error != None):
                errors.append(error)

        return errors

    def test_user(self):
        """ test_user

            1. deleteUser
            2. createUser
            3. getUser
            4. deleteUser
        """

        errors = []

        # 1. deleteUser
        self._print_process_forward("Reset(deleteUser)")
        result = self.client.graphql_request(
            """
                mutation ($id: ID!) {
                    deleteUser(id: $id) {
                        id
                    }
                }
            """,
            {
                "id": self.user_id
            },
        )
        if not 'errors' in result["body"].keys() or result['status'] != 200:
            try:
                self._print_process_backward(f"Delete own user data {result['body']['data']['deleteUser']['id']}", True)
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(e)
        else:
            self._print_process_backward(result['body'], False)
            errors.append(result['body'])
        
        # 2. createUser
        self._print_process_forward("Mutation(createUser)")
        result = self.client.graphql_request(
            """
                mutation createUser(
                    $user: UserCreate!
                ) {
                    createUser(
                        user: $user
                    ) {
                        id
                    }
                }
            """,
            {
                "user": {
                    "displayName": "AppSync-test sample user",
                    "email"      : "AppSync-test@sample.xyz",
                    "career"     : "AppSync-test test_user test",
                    "avatarUri"  : "https://s3-ap-northeast-1.amazonaws.com/is09-portal-image/system/broken-image.png",
                    "message"    : "",
                }
            },
        )
        if not 'errors' in result["body"].keys() or result['status'] != 200:
            try:
                self._print_process_backward(f"Create user {result['body']['data']['createUser']['id']}", True)
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(e)
        else:
            self._print_process_backward(result['body'], False)
            errors.append(result['body'])

        # 3. getUser
        self._print_process_forward("Query(getUser)")
        result = self.client.graphql_request(
            """
                query($id: ID!) {
                    getUser(id: $id) {
                        id
                        email
                        displayName
                        career
                        avatarUri
                        message
                    }
                }
            """,
            {
                "id": self.user_id
            },
        )
        if not 'errors' in result["body"].keys() or result['status'] != 200:
            try:
                self._print_process_backward(f"Create user {result['body']['data']['getUser']['id']}", True)
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(e)
        else:
            self._print_process_backward(result['body'], False)
            errors.append(result['body'])


        #4 deleteUser
        self._print_process_forward("Reset(deleteUser)")
        result = self.client.graphql_request(
            """
                mutation ($id: ID!) {
                    deleteUser(id: $id) {
                        id
                    }
                }
            """,
            {
                "id": self.user_id
            },
        )
        if not 'errors' in result["body"].keys() or result['status'] != 200:
            try:
                self._print_process_backward(f"Delete own user data {result['body']['data']['deleteUser']['id']}", True)
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(e)
        else:
            self._print_process_backward(result['body'], False)
            errors.append(result['body'])

        # Finaly
        if len(errors) == 0:
            return None
        else:
            return errors

    @staticmethod
    def _print_process_forward(title):
        print(f"{bcolors.OKBLUE}i {bcolors.ENDC}{bcolors.INFO}{title}{bcolors.ENDC}{(20 - len(title)) * ' '}: ", end="")

    @staticmethod
    def _print_process_backward(value, is_success):
        color = bcolors.FAIL
        mark = "✗"
        if is_success:
            color = bcolors.OKGREEN
            mark = "✓"

        print(f"{color}{bcolors.BOLD}{mark}{bcolors.ENDC} {value}")
