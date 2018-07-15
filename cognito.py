# -*- coding: utf-8 -*-

"""
    cognito.py

    AWS Cognito client
    
    support version: Python 3.6.5
"""
import base64
import json

import boto3


def cognito_auth(username, password, region_name, client_id):
    """ cognito_auth

        @param username: aws cognito username
        @param password: aws cognito password
        @param region_name: aws cognito region_name
        @param client_id: aws cognito client_id
    """
    try:
        client = boto3.client(
            "cognito-idp",
            region_name=region_name,
        )
        result = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
            ClientId=client_id
        )
        return result

    except Exception as e:
        return e


def formatAuth(client):
    """ formatAuth

        @param client: boto3.client

        result struct
        {
            header: {
                "kid": string,
                "alg": string
            },
            payload: {
                "sub"                : string,
                "aud"                : string,
                "email_verified"     : boolean,
                "event_id"           : string,
                "token_use"          : string,
                "auth_time"          : number,
                "iss"                : string,
                "cognito:username"   : string,
                "custom:display_name": string,
                "exp"                : number,
                "iat"                : number,
                "email"              : string
            }
        }
    """
    jwt = client["AuthenticationResult"]["IdToken"].split('.')
    return {
        "header" : json.loads(base64.b64decode(jwt[0]).decode()),
        "payload": json.loads(base64.urlsafe_b64decode(jwt[1] + '=' * (-len(jwt[1]) % 4)).decode())
    }
