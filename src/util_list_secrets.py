import logging
from botocore.exceptions import ClientError
from src.util_get_client import get_client

logging.basicConfig()
logger = logging.getLogger(" Password_manager")
logger.setLevel(logging.INFO)


def list_secrets():
    try:
        client = get_client()
        response = client.list_secrets()

        if len(response["SecretList"]) == 0:
            logger.info(" There are no secrets")
        else:
            secrets = [secret["Name"] for secret in response["SecretList"]]
            logger.info(f" {len(secrets)} secret(s) available: \n{secrets}")

    except ClientError as ce:
        logger.error(ce.response["Error"]["Message"])
