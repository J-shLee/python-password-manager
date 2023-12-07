import logging
from botocore.exceptions import ClientError
from util_get_client import get_client
import json

logging.basicConfig()
logger = logging.getLogger(" Password_manager")
logger.setLevel(logging.INFO)


def insert_secret(secret_identifier=None, user_id=None, password=None):
    try:
        client = get_client()

        if secret_identifier == None:
            secret_identifier = input(" What name would you like to give this secret? ")

        if user_id == None:
            user_id = input(" What is the username you'd like to save? ")

        if password == None:
            password = input(" What is the password you'd like to save? ")

        json_upload = {"user_id": user_id, "password": password}

        response = client.create_secret(
            Name=secret_identifier, SecretString=json.dumps(json_upload)
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info("Secret Saved")

    except ClientError as ce:
        logger.error(f' {ce.response["Error"]["Message"]}')
    except Exception as e:
        logger.error(e)
