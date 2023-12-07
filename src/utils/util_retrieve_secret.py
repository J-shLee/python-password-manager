import logging
from botocore.exceptions import ClientError
import os
import json
import boto3

logging.basicConfig()
logger = logging.getLogger(" Password_manager")
logger.setLevel(logging.INFO)


def retrieve_secret(secret_identifier=None):
    try:
        client = boto3.client("secretsmanager", region_name="eu-west-2")

        if secret_identifier is None:
            secret_identifier = input(
                " What is the name of the secret you would like to retrieve? "
            )

        response = client.get_secret_value(SecretId=secret_identifier)

        secret = json.loads(response["SecretString"])

        directory = os.getcwd()

        if not os.path.isdir(f"{directory}/secrets"):
            os.mkdir(f"{directory}/secrets")

        secret_txt = open(f"./secrets/{secret_identifier}.txt", "w")
        secret_txt.write(
            f'User ID = {secret["user_id"]} \nPassword = {secret["password"]}'
        )
        secret_txt.close()

        logger.info(f" Secrets stored in local file {secret_identifier}.txt")

    except ClientError as ce:
        logger.error(ce.response["Error"]["Message"])
