import logging
from botocore.exceptions import ClientError
from src.util_get_client import get_client

logging.basicConfig()
logger = logging.getLogger(" Password_manager")
logger.setLevel(logging.INFO)


def delete_secret(secret_identifier=None):
    try:
        client = get_client()

        if secret_identifier == None:
            secret_identifier = input(
                " What's the name of the secret you would like to delete? "
            )

        response = client.delete_secret(SecretId=secret_identifier)

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info(f"Secret Deleted: {response['Name']}")

    except ClientError as ce:
        logger.error(ce.response["Error"]["Message"])
