# -*- coding: utf-8 -*-

"""
    main.py
    
    support version: Python 3.6.5
    dependencies: 
        boto3
        python-dotenv
    
    used font: http://patorjk.com/software/taag/#p=display&f=Calvin%20S&t=Type%20Something%20
"""

import sys, os
import cognito
from os.path import join, dirname
from dotenv import load_dotenv
from getpass import getpass
from graphql import GraphQL
from test_list import get_test_list

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

    if USERNAME == None:
        USERNAME = input("Input cognito Username > ")

    if PASSWORD == None:
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
    
    test_list = get_test_list(user["payload"]["sub"])

    print(f"""
=======================================================
╔═╗─┐ ┬┌─┐┌─┐┬ ┬┌┬┐┌─┐  ╔╦╗╔═╗╔═╗╔╦╗
║╣ ┌┴┬┘├┤ │  │ │ │ ├┤    ║ ║╣ ╚═╗ ║ 
╚═╝┴ └─└─┘└─┘└─┘ ┴ └─┘   ╩ ╚═╝╚═╝ ╩ 
Number of test items: {bcolors.OKGREEN}{len(test_list)}{bcolors.ENDC}
=======================================================
    """)

    jwt = auth["AuthenticationResult"]["IdToken"]
    graphql = GraphQL(APPSYNC_URL, jwt)

    errors = []
    for test_index, test in enumerate(test_list):
        print(f"[{test_index + 1}/{len(test_list)}] {bcolors.UNDERLINE}{test['name']}{bcolors.ENDC}")
        queryErrors = []
        for query in test["queries"]:
            print(f"{bcolors.OKBLUE}i {bcolors.ENDC}{bcolors.INFO}{query['name']}{bcolors.ENDC}: ", end="")
            result = graphql.graphql_request(query["query"], query["variables"], operation_name=query["operation_name"])
            if not 'errors' in result["body"].keys() or result['status'] != 200:
                print(f"{bcolors.OKGREEN}{result['status']} {result['body']}{bcolors.ENDC}")
            else:
                print(f"{bcolors.FAIL}{result['status']} {result['body']}{bcolors.ENDC}")
                queryErrors.append(result['body'])
        
        if len(queryErrors) != 0:
            errors.append(queryErrors)

    
    print(f"""
=======================================================
╔╦╗┌─┐┌─┐┌┬┐  ╦═╗┌─┐┌─┐┬ ┬┬ ┌┬┐
 ║ ├┤ └─┐ │   ╠╦╝├┤ └─┐│ ││  │ 
 ╩ └─┘└─┘ ┴   ╩╚═└─┘└─┘└─┘┴─┘┴ 
 
Number of test items: {bcolors.OKGREEN}{len(test_list)}{bcolors.ENDC}
Success count       : {bcolors.OKGREEN}{len(errors) - len(test_list)}{bcolors.ENDC}
Faild count         : {bcolors.OKGREEN}{len(errors)}{bcolors.ENDC}
=======================================================
    """)

    if (len(test_list) == 0):
        sys.exit(0)
    else:
        sys.exit(1)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    OKGREEN = '\033[92m'
    INFO = '\033[90m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__":
    main()
