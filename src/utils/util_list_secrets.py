import logging
from botocore.exceptions import ClientError
import boto3

logging.basicConfig()
logger = logging.getLogger(" Password_manager")
logger.setLevel(logging.INFO)


def list_secrets():
    try:
        client = boto3.client("secretsmanager")
        response = client.list_secrets()

        if len(response["SecretList"]) == 0:
            logger.info(" There are no secrets")
        else:
            secrets = [secret["Name"] for secret in response["SecretList"]]
            logger.info(f" {len(secrets)} secret(s) available: \n{secrets}")

    except ClientError as ce:
        logger.error(ce.response["Error"]["Message"])
