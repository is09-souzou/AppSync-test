# AppSync-test
https://github.com/is09-souzou/AppSync-Resolver-Mapping-Lambda
Test took

## Setup

1. Create file the `.env`

```sh
COGNIT_RREGION_NAME=
COGNITO_CLIENT_KEY=
APPSYNC_URL=

# option
USERNAME=
PASSWORD=
```

check the `.env.sample`

2. Create virtualenv

- Not installed virtualenv

```bash
$ pip install virtualenv
$ virtualenv -p python3 virtualenv
```

- Installed virtualenv
```bash
$ virtualenv -p python3 virtualenv
```

3. Start virtualenv

```bash
$ source virtualenv/bin/activate
```

4. Install dependencies

```bash
$ pip install -U pylint
$ pip install boto3
$ pip install python-dotenv
$ pip install flake8
```

- Exit virtualenv
```bash
$ deactivate
```

## Run AppSync-test Apprication

Run main.py
```
$ python3 main.py
```

## Check source lint
```bash
$ flake8 *.py
```

## Add test
1. open `test_list.py`
2. Add method to Test class
- Method name starts with `test_`
- return Error of None

sample
```python
    def test_sample(self):
        """ test_sample

            Flow
            1. Reset
            2. createUser: Confirmation equal to createUser request data

            Use Queries
            - createUser
        """
    
        progress_count = 0
        errors = []

        # 1. Reset
        progress_count += 1
        self._reset(errors, progress_count)

        # 2. createUser: Confirmation equal to createUser request data
        self._print_process_forward("Mutation(createUser)", progress_count)
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
                print(e)
                self._print_process_backward(e, False)
                errors.append(Exception(result["body"]))
        else:
            self._print_process_backward(result["body"], False)
            errors.append(Exception(result["body"]))

        if len(errors) == 0:
            return None
        else:
            return errors
```

3. Add created method to get_test_list method

sample
```python

    def get_test_list(self):
        return [
            ...
            # Add
            {
                "name": "Sample Test",
                "exec": lambda: self.test_sample()
            },
        ]
```
