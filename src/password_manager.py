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
    client = get_client()
    response = client.list_secrets()

    # print(response)

    # print(response) result while there was 1 item in the bucket >>> 
    # {'SecretList': [{
    # 'ARN': 'arn:aws:secretsmanager:eu-west-2:039843163800:secret:zzzz-CpzmUZ', 
    # 'Name': 'zzzz', 
    # 'LastChangedDate': datetime.datetime(2023, 10, 25, 19, 37, 29, 592000, tzinfo=tzlocal()), 
    # 'SecretVersionsToStages': {'05f71c9e-20c0-415a-9d67-943d9649673e': ['AWSCURRENT']}, 
    # 'CreatedDate': datetime.datetime(2023, 10, 25, 19, 37, 29, 389000, tzinfo=tzlocal())}], 
    # 'ResponseMetadata': {'RequestId': 'a257fe28-f671-48a1-9a1d-e94a85274c6b', 
    # 'HTTPStatusCode': 200, 
    # 'HTTPHeaders': {'x-amzn-requestid': 'a257fe28-f671-48a1-9a1d-e94a85274c6b', 
    # 'content-type': 'application/x-amz-json-1.1', 
    # 'content-length': '252', 
    # 'date': 'Wed, 25 Oct 2023 18:48:14 GMT'}, 
    # 'RetryAttempts': 0}}


    # print(response) when there was no items in the bucket >>>>>>
    # {'SecretList': [], 
    # 'ResponseMetadata': {'RequestId': '1a19d297-65eb-4775-a643-c98a4d9ee36b', 
    # 'HTTPStatusCode': 200, 
    # 'HTTPHeaders': {'x-amzn-requestid': '1a19d297-65eb-4775-a643-c98a4d9ee36b', 
    # 'content-type': 'application/x-amz-json-1.1', 
    # 'content-length': '17', 
    # 'date': 'Wed, 25 Oct 2023 19:04:27 GMT'}, 
    # 'RetryAttempts': 0}}

    if len(response['SecretList']) == 0:
        logger.info("There are no secrets")
        # return handler()
    else:
        secrets = [secret['Name'] for secret in response['SecretList']]
        logger.info(f'{len(secrets)} secret(s) available: \n{secrets}')
        # return handler()