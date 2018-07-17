# -*- coding: utf-8 -*-

"""
    test.py

    AWS AppSync Portal Test

    support version: Python 3.6.5
"""

import copy
from datetime import datetime

from bcolors import bcolors


class Test:

    def get_test_list(self):
        return [
            {
                "name": "User test",
                "exec": lambda: self.test_user()
            },
            {
                "name": "Work test",
                "exec": lambda: self.test_work()
            },
            # {
            #     "name": "Work list test",
            #     "exec": lambda: self.test_work_list()
            # }
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
            print(f"\n[{test_index + 1}/{len(test_list)}] Execute Test: {test['name']}")
            error = test["exec"]()
            if (error is not None):
                errors.append(error)

        return errors

    def test_user(self):
        """ test_user

            Flow
            1. Reset
            2. createUser: Confirmation equal to createUser request data
            3. getUser   : Confirmation equal to createUser request data
            4. updateUser: Confirmation equal to updateUser request data
            5. getUser   : Confirmation equal to createUser request data
            6. deleteUser: Confirm whether it was deleted
            7. getUser   : Confirm whether it was deleted

            Use Queries
            - createUser
            - getUser
            - updateUser
            - deleteUser
        """

        process_count = 0
        errors = []

        # 1. Reset
        process_count += 1
        self._reset(errors, process_count)

        # 2. createUser: Confirmation equal to createUser request data
        process_count += 1
        self._print_process_forward("Mutation(createUser)", process_count)
        user_input = {
            "displayName": f"AppSync-test sample user {str(datetime.now())}",
            "email"      : "AppSync-test@sample.xyz",
            "career"     : "AppSync-test test_user test",
            "avatarUri"  : "https://s3-ap-northeast-1.amazonaws.com/is09-portal-image/system/broken-image.png",
            "message"    : "",
        }
        result = self.client.graphql_request(
            """
                mutation createUser(
                    $user: UserCreate!
                ) {
                    createUser(
                        user: $user
                    ) {
                        id
                        displayName
                        email
                        career
                        avatarUri
                        message
                    }
                }
            """,
            {
                "user": user_input
            },
        )
        if "errors" not in result["body"].keys():
            try:
                request_user_input = copy.copy(user_input)
                request_user_input["id"] = self.user_id
                request_user_input["message"] = " "
                if request_user_input == result['body']['data']['createUser']:
                    self._print_process_backward(f"Create user {result['body']['data']['createUser']['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 3. getUser: Confirmation equal to createUser request data
        process_count += 1
        self._print_process_forward("Query(getUser)", process_count)
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
        if "errors" not in result["body"].keys():
            try:
                request_user_input = copy.copy(user_input)
                request_user_input["id"] = self.user_id
                request_user_input["message"] = " "
                if request_user_input == result['body']['data']['getUser']:
                    self._print_process_backward(f"Get user {result['body']['data']['getUser']['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 4. updateUser: Confirmation equal to updateUser request data
        process_count += 1
        user_update = {
            "id"         : self.user_id,
            "displayName": f"AppSync-test sample user {str(datetime.now())} (updated)",
            "email"      : "AppSync-test@sample.xyz (updated)",
            "career"     : "AppSync-test test_user test (updated)",
            "avatarUri"  : "https://s3-ap-northeast-1.amazonaws.com/is09-portal-image/system/broken-image.png (updated)",
            "message"    : "AppSync-test test_user test message (updated)",
        }
        self._print_process_forward("Mutation(updateUser)", process_count)
        result = self.client.graphql_request(
            """
                mutation(
                    $user: UserUpdate!
                ) {
                    updateUser(
                        user: $user
                    ) {
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
                "user": user_update
            },
        )
        if "errors" not in result["body"].keys():
            try:
                request_user_update = copy.copy(user_update)
                if request_user_update == result['body']['data']['updateUser']:
                    self._print_process_backward(f"Update user {result['body']['data']['updateUser']['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 5. getUser: Confirmation equal to createUser request data
        process_count += 1
        self._print_process_forward("Query(getUser)", process_count)
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
        if "errors" not in result["body"].keys():
            try:
                request_user_update = copy.copy(user_update)
                if request_user_update == result['body']['data']['getUser']:
                    self._print_process_backward(f"Get user {result['body']['data']['getUser']['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 6. deleteUser: Confirm whether it was deleted
        process_count += 1
        self._print_process_forward("Reset(deleteUser)", process_count)
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
        if "errors" not in result["body"].keys():
            try:
                self._print_process_backward(f"Delete own user data {result['body']['data']['deleteUser']['id']}", True)
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 7. getUser: Confirm whether it was deleted
        process_count += 1
        self._print_process_forward("Query(getUser)", process_count)
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
        if "errors" not in result["body"].keys():
            try:
                if result['body']['data']['getUser'] is None:
                    self._print_process_backward(f"Delete own user data", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        if len(errors) == 0:
            return None
        else:
            return errors

    def test_work(self):
        """ test_work

            Flow
            1. Reset
            2. createUser     : No verification
            3. createWork     : Confirmation equal to createWork request data
            4. getUser(works) : Confirmation equal to createWork request data
            5. getWork        : Confirmation equal to createWork request data
            6. updateWork     : Confirmation equal to updateWork request data
            7. getUser(works) : Confirmation equal to updateWork request data
            8. getWork        : Confirmation equal to updateWork request data
            9. deleteUser     : Confirm whether it was work deleted
            10. getUser(works): Confirm whether it was work deleted
            11. getWork       : Confirm whether it was work deleted

            Use Queries
            - createUser
            - getUser
            - deleteUser
            - createWork
            - updateWork
            - getWork
            - deleteWork
        """

        process_count = 0
        errors = []

        # 1. Reset
        process_count += 1
        self._reset(errors, process_count)

        # 2. createUser: No verification
        process_count += 1
        self._print_process_forward("Mutation(createUser)", process_count)
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
                    "displayName": f"AppSync-test test user {str(datetime.now())}",
                    "email"      : "AppSync-test@sample.xyz",
                    "career"     : "AppSync-test test_user test",
                    "avatarUri"  : "https://s3-ap-northeast-1.amazonaws.com/is09-portal-image/system/broken-image.png",
                    "message"    : "",
                }
            },
        )

        if "errors" not in result["body"].keys():
            try:
                self._print_process_backward(f"Create user {result['body']['data']['createUser']['id']}", True)
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        created_work_id = ""
        created_work_createdAt = ""

        # 3. createWork: Confirmation equal to createWork request data
        process_count += 1
        work_input = {
            "userId"     : self.user_id,
            "title"      : "AppSync-test test user",
            "description": f"AppSync-test work {str(datetime.now())}",
            "tags"       : ["AppSync-test"],
            "imageUrl"   : "https://s3-ap-northeast-1.amazonaws.com/is09-portal-image/system/broken-image.png"
        }
        self._print_process_forward("Mutation(createWork)", process_count)
        result = self.client.graphql_request(
            """
                mutation createWork(
                    $work: WorkCreate!
                ) {
                    createWork(
                        work: $work
                    ) {
                        id
                        description
                        userId
                        title
                        tags
                        imageUrl
                        createdAt
                    }
                }
            """,
            {
                "work": work_input
            },
        )

        if "errors" not in result["body"].keys():
            try:
                request_work_input = copy.copy(work_input)
                created_work_id = result['body']['data']['createWork']['id']
                request_work_input["id"] = created_work_id
                created_work_createdAt = result['body']['data']['createWork']['createdAt']
                request_work_input["createdAt"] = created_work_createdAt
                if request_work_input == result['body']['data']['createWork']:
                    self._print_process_backward(f"Create work {result['body']['data']['createWork']['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 4. getUser(works): Confirmation equal to createWork request data
        process_count += 1
        self._print_process_forward("Query(getUser)", process_count)
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
                        works {
                            items {
                                id
                                description
                                userId
                                title
                                tags
                                imageUrl
                                createdAt
                            }
                            exclusiveStartKey
                        }
                    }
                }
            """,
            {
                "id": self.user_id
            },
        )
        if "errors" not in result["body"].keys():
            try:
                request_work_input = copy.copy(work_input)
                request_work_input["id"] = created_work_id
                request_work_input["createdAt"] = created_work_createdAt
                if request_work_input == result['body']['data']['getUser']['works']['items'][0]:
                    self._print_process_backward(f"Get work on getUser {result['body']['data']['getUser']['works']['items'][0]['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 5. getWork: Confirmation equal to createWork request data
        process_count += 1
        self._print_process_forward("Query(getWork)", process_count)
        result = self.client.graphql_request(
            """
                query($id: ID!) {
                    getWork(id: $id) {
                        id
                        description
                        userId
                        title
                        tags
                        imageUrl
                        createdAt
                    }
                }
            """,
            {
                "id": created_work_id
            },
        )
        if "errors" not in result["body"].keys():
            try:
                request_work_input = copy.copy(work_input)
                request_work_input["id"] = created_work_id
                request_work_input["createdAt"] = created_work_createdAt
                if request_work_input == result['body']['data']['getWork']:
                    self._print_process_backward(f"Get work {result['body']['data']['getWork']['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 6. updateWork: Confirmation equal to updateWork request data
        process_count += 1
        work_update = {
            "id"         : created_work_id,
            "userId"     : self.user_id,
            "title"      : "AppSync-test test user (updated)",
            "description": f"AppSync-test work {str(datetime.now())} (updated)",
            "tags"       : ["AppSync-test", "AppSync-test-updated"],
            "imageUrl"   : "https://s3-ap-northeast-1.amazonaws.com/is09-portal-image/system/broken-image.png"
        }
        self._print_process_forward("Mutation(updateWork)", process_count)
        result = self.client.graphql_request(
            """
                mutation(
                    $work: WorkUpdate!
                ) {
                    updateWork(
                        work: $work
                    ) {
                        id
                        description
                        userId
                        title
                        tags
                        imageUrl
                        createdAt
                    }
                }
            """,
            {
                "work": work_update
            },
        )
        if "errors" not in result["body"].keys():
            try:
                request_work_update = copy.copy(work_update)
                request_work_update["id"] = created_work_id
                request_work_update["createdAt"] = created_work_createdAt
                if request_work_update == result['body']['data']['updateWork']:
                    self._print_process_backward(f"Update work {result['body']['data']['updateWork']['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 7. getUser(works): Confirmation equal to updateWork request data
        process_count += 1
        self._print_process_forward("Query(getUser)", process_count)
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
                        works {
                            items {
                                id
                                description
                                userId
                                title
                                tags
                                imageUrl
                                createdAt
                            }
                            exclusiveStartKey
                        }
                    }
                }
            """,
            {
                "id": self.user_id
            },
        )
        if "errors" not in result["body"].keys():
            try:
                request_work_update = copy.copy(work_update)
                request_work_update["id"] = created_work_id
                request_work_update["createdAt"] = created_work_createdAt
                if request_work_update == result['body']['data']['getUser']['works']['items'][0]:
                    self._print_process_backward(f"Get work on getUser {result['body']['data']['getUser']['works']['items'][0]['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 8. getWork: Confirmation equal to updateWork request data
        process_count += 1
        self._print_process_forward("Query(getWork)", process_count)
        result = self.client.graphql_request(
            """
                query($id: ID!) {
                    getWork(id: $id) {
                        id
                        description
                        userId
                        title
                        tags
                        imageUrl
                        createdAt
                    }
                }
            """,
            {
                "id": created_work_id
            },
        )
        if "errors" not in result["body"].keys():
            try:
                request_work_update = copy.copy(work_update)
                request_work_update["id"] = created_work_id
                request_work_update["createdAt"] = created_work_createdAt
                if request_work_update == result['body']['data']['getWork']:
                    self._print_process_backward(f"Get work {result['body']['data']['getWork']['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 9. deleteUser: Confirm whether it was work deleted
        process_count += 1
        self._print_process_forward("Reset(deleteUser)", process_count)
        result = self.client.graphql_request(
            """
                mutation ($id: ID!) {
                    deleteUser(id: $id) {
                        id
                        works {
                            items {
                                id
                                description
                                userId
                                title
                                tags
                                imageUrl
                                createdAt
                            }
                        }
                    }
                }
            """,
            {
                "id": self.user_id
            },
        )
        if "errors" not in result["body"].keys():
            try:
                if result['body']['data']['deleteUser']["works"]["items"] == []:
                    self._print_process_backward(f"Delete own user data {result['body']['data']['deleteUser']['id']}", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 10. getUser(works): Confirm whether it was work deleted
        process_count += 1
        self._print_process_forward("Query(getUser)", process_count)
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
                        works {
                            items {
                                id
                                description
                                userId
                                title
                                tags
                                imageUrl
                                createdAt
                            }
                            exclusiveStartKey
                        }
                    }
                }
            """,
            {
                "id": self.user_id
            },
        )
        if "errors" not in result["body"].keys():
            try:
                if result['body']['data']['getUser'] is None:
                    self._print_process_backward(f"Get work on getUser, deleted works", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 11. getWork: Confirm whether it was work deleted
        process_count += 1
        self._print_process_forward("Query(getWork)", process_count)
        result = self.client.graphql_request(
            """
                query($id: ID!) {
                    getWork(id: $id) {
                        id
                        description
                        userId
                        title
                        tags
                        imageUrl
                        createdAt
                    }
                }
            """,
            {
                "id": created_work_id
            },
        )
        if "errors" not in result["body"].keys():
            try:
                if result['body']['data']['getWork'] is None:
                    self._print_process_backward(f"Get work, deleted works", True)
                else:
                    self._print_process_backward("Not assumed response value", False)
                    errors.append(Exception(result["body"]))
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        if len(errors) == 0:
            return None
        else:
            return errors

    # TODO: creating...
    def test_work_list(self):
        """ test_work

            Flow
            1. Reset
            2. createUser: No verification
            3. createWork: Confirmation equal to createWork request data

            Use Queries
            - createUser
            - createWork
        """

        process_count = 0
        errors = []

        # 1. Reset
        process_count += 1
        self._reset(errors, process_count)

        # 2. createUser: No verification
        process_count += 1
        self._print_process_forward("Mutation(createUser)", process_count)
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
                    "displayName": f"AppSync-test test user {str(datetime.now())}",
                    "email"      : "AppSync-test@sample.xyz",
                    "career"     : "AppSync-test test_user test",
                    "avatarUri"  : "https://s3-ap-northeast-1.amazonaws.com/is09-portal-image/system/broken-image.png",
                    "message"    : "",
                }
            },
        )

        if "errors" not in result["body"].keys():
            try:
                self._print_process_backward(f"Create user {result['body']['data']['createUser']['id']}", True)
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        # 3. createWork: Confirmation equal to createWork request data
        for i in range(25):
            process_count += 1
            work_input = {
                "userId"     : self.user_id,
                "title"      : f"AppSync-test Work {i + 1 % 2}",
                "description": f"AppSync-test work {str(datetime.now())}",
                "tags"       : ["test", "even" if (i + 1) % 2 == 0 else "odd"],
                "imageUrl"   : "https://s3-ap-northeast-1.amazonaws.com/is09-portal-image/system/broken-image.png"
            }
            self._print_process_forward("Mutation(createWork)", process_count)
            result = self.client.graphql_request(
                """
                    mutation createWork(
                        $work: WorkCreate!
                    ) {
                        createWork(
                            work: $work
                        ) {
                            id
                            description
                            userId
                            title
                            tags
                            imageUrl
                            createdAt
                        }
                    }
                """,
                {
                    "work": work_input
                },
            )

            if "errors" not in result["body"].keys():
                try:
                    request_work_input = copy.copy(work_input)
                    created_work_id = result['body']['data']['createWork']['id']
                    request_work_input["id"] = created_work_id
                    created_work_createdAt = result['body']['data']['createWork']['createdAt']
                    request_work_input["createdAt"] = created_work_createdAt
                    if request_work_input == result['body']['data']['createWork']:
                        self._print_process_backward(f"Create work {result['body']['data']['createWork']['id']}", True)
                    else:
                        self._print_process_backward("Not assumed response value", False)
                        errors.append(Exception(result["body"]))
                except Exception as e:
                    self._print_process_backward(e, False)
                    errors.append(Exception(result["body"]))
            else:
                self._print_process_backward(result["body"], False)
                errors.append(Exception(result["body"]))

        if len(errors) == 0:
            return None
        else:
            return errors

    def _reset(self, errors, process_count):
        self._print_process_forward("Reset(deleteUser)", process_count)
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
        if "errors" not in result["body"].keys():
            try:
                self._print_process_backward(f"Delete own user data {result['body']['data']['deleteUser']['id']}", True)
            except Exception as e:
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

    @staticmethod
    def _print_process_forward(title, count):
        print(f"{bcolors.OKBLUE}{count}.{(3 -len(str(count))) * ' '}{bcolors.ENDC}{bcolors.INFO}{title}{bcolors.ENDC}{(20 - len(title)) * ' '}: ", end="")

    @staticmethod
    def _print_process_backward(value, is_success):
        if is_success:
            print(f"{value} {bcolors.OKGREEN}{bcolors.BOLD}✓{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}{bcolors.BOLD}{value} ✗{bcolors.ENDC}")
