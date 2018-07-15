# -*- coding: utf-8 -*-

"""
    main.py

    support version: Python 3.6.5
    dependencies:
        boto3
        python-dotenv
    used font: http://patorjk.com/software/taag/#p=display&f=Calvin%20S&t=Type%20Something%20
"""

import os
import sys
from getpass import getpass
from os.path import dirname, join
from test import Test

from dotenv import load_dotenv
from graphql import GraphQL

import cognito
from bcolors import bcolors

ERROR_LOGS_FILE = "portal-error.log"


def main():
    """ main
        entry point
    """

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    COGNIT_RREGION_NAME = os.environ.get("COGNIT_RREGION_NAME")
    COGNITO_CLIENT_KEY  = os.environ.get("COGNITO_CLIENT_KEY")
    APPSYNC_URL         = os.environ.get("APPSYNC_URL")
    USERNAME            = os.environ.get("USERNAME")
    PASSWORD            = os.environ.get("PASSWORD")

    print(f"""
=======================================================
╔═╗┌─┐┬─┐┌┬┐┌─┐┬    ╔═╗┌─┐┌─┐╔═╗┬ ┬┌┐┌┌─┐  ╔╦╗┌─┐┌─┐┌┬┐
╠═╝│ │├┬┘ │ ├─┤│    ╠═╣├─┘├─┘╚═╗└┬┘││││     ║ ├┤ └─┐ │
╩  └─┘┴└─ ┴ ┴ ┴┴─┘  ╩ ╩┴  ┴  ╚═╝ ┴ ┘└┘└─┘   ╩ └─┘└─┘ ┴
COGNIT_RREGION_NAME: {bcolors.OKGREEN}{COGNIT_RREGION_NAME}{bcolors.ENDC}
COGNIT_RREGION_NAME: {bcolors.OKGREEN}{COGNITO_CLIENT_KEY}{bcolors.ENDC}
APPSYNC_URL        : {bcolors.OKGREEN}{APPSYNC_URL}{bcolors.ENDC}
=======================================================
    """)

    if USERNAME is None:
        USERNAME = input("Input cognito Username > ")

    if PASSWORD is None:
        PASSWORD = getpass("Input cognito Password > ")

    print(f"{bcolors.OKBLUE}Try{bcolors.ENDC} SignIn")

    auth = cognito.cognito_auth(
        USERNAME,
        PASSWORD,
        COGNIT_RREGION_NAME,
        COGNITO_CLIENT_KEY
    )

    if isinstance(auth, Exception):
        print(f"""
{bcolors.FAIL}Failed{bcolors.ENDC} SignIn
{bcolors.FAIL}{auth}{bcolors.ENDC}
        """)
        sys.exit(1)
    else:
        user = cognito.formatAuth(auth)
        print(f"""
{bcolors.OKGREEN}Success{bcolors.ENDC} SignIn
{bcolors.OKBLUE}i {bcolors.ENDC}username           : {bcolors.OKGREEN}{USERNAME}{bcolors.ENDC}
{bcolors.OKBLUE}i {bcolors.ENDC}sub                : {bcolors.OKGREEN}{user["payload"]["sub"]}{bcolors.ENDC}
{bcolors.OKBLUE}i {bcolors.ENDC}email              : {bcolors.OKGREEN}{user["payload"]["email"]}{bcolors.ENDC}
{bcolors.OKBLUE}i {bcolors.ENDC}custom:display_name: {bcolors.OKGREEN}{user["payload"]["custom:display_name"]}{bcolors.ENDC}
        """)

    jwt = auth["AuthenticationResult"]["IdToken"]
    graphql_client = GraphQL(APPSYNC_URL, jwt)
    test = Test(user["payload"]["sub"], graphql_client)
    test_list = test.get_test_list()

    print(f"""
=======================================================
╔═╗─┐ ┬┌─┐┌─┐┬ ┬┌┬┐┌─┐  ╔╦╗╔═╗╔═╗╔╦╗
║╣ ┌┴┬┘├┤ │  │ │ │ ├┤    ║ ║╣ ╚═╗ ║
╚═╝┴ └─└─┘└─┘└─┘ ┴ └─┘   ╩ ╚═╝╚═╝ ╩
Number of test items: {bcolors.OKGREEN}{len(test_list)}{bcolors.ENDC}
=======================================================
    """)

    errors = test.execute_test()

    print(f"""
=======================================================
╔╦╗┌─┐┌─┐┌┬┐  ╦═╗┌─┐┌─┐┬ ┬┬ ┌┬┐
 ║ ├┤ └─┐ │   ╠╦╝├┤ └─┐│ ││  │
 ╩ └─┘└─┘ ┴   ╩╚═└─┘└─┘└─┘┴─┘┴

Number of test items: {bcolors.OKGREEN}{len(test_list)}{bcolors.ENDC}
Success count       : {bcolors.OKGREEN}{len(test_list) - len(errors)}{bcolors.ENDC}
Faild count         : {bcolors.OKGREEN}{len(errors)}{bcolors.ENDC}
=======================================================
    """)

    if (len(errors) != 0):
        with open(join(dirname(__file__), ERROR_LOGS_FILE), mode="w") as f:
            f.write(str(errors))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
