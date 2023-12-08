import logging
from botocore.exceptions import ClientError
import os
import json
import boto3

logging.basicConfig()
logger = logging.getLogger(" Password_manager")
logger.setLevel(logging.INFO)


def retrieve_secret(secret_identifier=None):
    """
    this function retrieves a secret stored in SecretsManager

    Parameters
    ----------
        secret_identifier: user input of the secret they want to retrieve

    Returns
    ----------
        returns nothing, displays terminal message if secret retrieved, saves
        secret to local directory ../secrets/
    """
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

        with open(f"./secrets/{secret_identifier}.txt", "w") as f:
            f.write(
                f'User ID = {secret["user_id"]} \nPassword = {secret["password"]}'  # noqa E501
            )

        logger.info(f" Secrets stored in local file {secret_identifier}.txt")

    except ClientError as ce:
        logger.error(ce.response["Error"]["Message"])
