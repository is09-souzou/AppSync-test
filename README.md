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
```

## Run Apprication

Run main.py
```
$ python3 main.py
```

- Exit virtualenv
```bash
$ deactivate
```

## Add test
edit `test_list.py`

