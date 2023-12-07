import logging
from botocore.exceptions import ClientError
import json
import boto3

logging.basicConfig()
logger = logging.getLogger(" Password_manager")
logger.setLevel(logging.INFO)


def insert_secret(secret_identifier=None, user_id=None, password=None):
    try:
        client = boto3.client("secretsmanager", region_name="eu-west-2")

        if secret_identifier is None:
            secret_identifier = input(
                " What would you like to call this secret? "
            )  # noqa E501

        if user_id is None:
            user_id = input(" What is the username you'd like to save? ")

        if password is None:
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
