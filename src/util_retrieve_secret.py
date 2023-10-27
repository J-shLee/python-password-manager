import logging
from botocore.exceptions import ClientError
from src.util_get_client import get_client
import os
import json

logging.basicConfig()
logger = logging.getLogger(" Password_manager")
logger.setLevel(logging.INFO)


def retrieve_secret(secret_identifier=None):
    try:
        client = get_client()

        if secret_identifier == None:
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
