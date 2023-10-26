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


def delete_secret(secret_identifier=None):
    try:
        client = get_client()

        if secret_identifier == None:
            secret_identifier = input('What\'s the name of the secret you would like to delete?')

        response = client.delete_secret(
            SecretId=secret_identifier
        )

        # print(response)
        # result of print(response) after deleting the only item in the bucket
        # {'ARN': 'arn:aws:secretsmanager:eu-west-2:039843163800:secret:zzzz-CpzmUZ',
        # 'Name': 'zzzz', 
        # 'DeletionDate': datetime.datetime(2023, 11, 24, 19, 0, 43, 426000, tzinfo=tzlocal()), 
        # 'ResponseMetadata': {'RequestId': 'be695dc5-f092-4f09-9027-321de30cb92b', 
        # 'HTTPStatusCode': 200, 
        # 'HTTPHeaders': {'x-amzn-requestid': 'be695dc5-f092-4f09-9027-321de30cb92b', 
        # 'content-type': 'application/x-amz-json-1.1', 
        # 'content-length': '120', 
        # 'date': 'Wed, 25 Oct 2023 19:00:43 GMT'}, 
        # 'RetryAttempts': 0}}
        # logger.info(response)

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            logger.info(f"Secret Deleted: {response['Name']}")
            # return handler()
        else:
            # raise error
            pass
    except:
        # print error message and return handler function to return to main menu
        pass