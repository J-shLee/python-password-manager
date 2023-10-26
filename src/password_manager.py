import boto3
from botocore.exceptions import ClientError
import json
import logging

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)


def get_client():
    secrets_manager = boto3.client('secretsmanager')
    return secrets_manager

def insert_secret(secret_identifier=None, user_id=None, password=None):
    try:
        client = get_client()

        if secret_identifier == None:
            secret_identifier = input('What name would you like to give this secret?')

        if user_id == None:
            user_id = input('What is the username you\'d like to save?')
        
        if password == None:
            password = input('What is the password you\'d like to save?')
        
        json_upload = {
            'user_id': user_id, 
            'password': password
        }

        response = client.create_secret(
            Name=secret_identifier,
            SecretString=json.dumps(json_upload)
        )


        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            logger.info('Secret Saved')
    except ClientError as ce:
        logger.error(ce)
    except Exception as e:
        logger.error(e)
    # finally:
    #     return handler()


def list_secrets():
    try:
        client = get_client()
        response = client.list_secrets()

        if len(response['SecretList']) == 0:
            logger.info("There are no secrets")
            # return handler()
        else:
            secrets = [secret['Name'] for secret in response['SecretList']]
            logger.info(f'{len(secrets)} secret(s) available: \n{secrets}')
            # return handler()
    except ClientError as ce:
        logger.error(ce)
    # finally:
    #     return handler()