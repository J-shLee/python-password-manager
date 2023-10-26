import boto3
from botocore.exceptions import ClientError
import json
import logging
import os

logging.basicConfig()
logger = logging.getLogger("Password_manager")
logger.setLevel(logging.INFO)


def handler(user_input=None):
    valid_inputs = {
        "e": insert_secret,
        "r": retrieve_secret,
        "d": delete_secret,
        "l": list_secrets,
    }

    if user_input == None:
        user_input = input(
            "Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it: "
        ).lower()

    if user_input == "x":
        logger.info("Thank you. Goodbye")
        return
    elif user_input in valid_inputs:
        function = valid_inputs[user_input]
        return function()
    else:
        logger.info("Invalid input")
        return handler()


def get_client():
    secrets_manager = boto3.client("secretsmanager")
    return secrets_manager


def insert_secret(secret_identifier=None, user_id=None, password=None):
    try:
        client = get_client()

        if secret_identifier == None:
            secret_identifier = input("What name would you like to give this secret? ")

        if user_id == None:
            user_id = input("What is the username you'd like to save? ")

        if password == None:
            password = input("What is the password you'd like to save? ")

        json_upload = {"user_id": user_id, "password": password}

        response = client.create_secret(
            Name=secret_identifier, SecretString=json.dumps(json_upload)
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info("Secret Saved")
            return handler()
    except ClientError as ce:
        logger.error(ce.response["Error"]["Message"])
    except Exception as e:
        logger.error(e)
    # finally:
    #     return handler()


def list_secrets():
    try:
        client = get_client()
        response = client.list_secrets()

        if len(response["SecretList"]) == 0:
            logger.info("There are no secrets")
            return handler()
        else:
            secrets = [secret["Name"] for secret in response["SecretList"]]
            logger.info(f"{len(secrets)} secret(s) available: \n{secrets}")
            return handler()
    except ClientError as ce:
        logger.error(ce.response["Error"]["Message"])
        return handler()
    # finally:
    #     return handler()


def delete_secret(secret_identifier=None):
    try:
        client = get_client()

        if secret_identifier == None:
            secret_identifier = input(
                "What's the name of the secret you would like to delete? "
            )

        response = client.delete_secret(SecretId=secret_identifier)

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info(f"Secret Deleted: {response['Name']}")
            # return handler()
    except ClientError as ce:
        logger.error(ce.response["Error"]["Message"])
    # finally:
    #     return handler()


def retrieve_secret(secret_identifier=None):
    try:
        client = get_client()

        if secret_identifier == None:
            secret_identifier = input(
                "What is the name of the secret you would like to retrieve? "
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

        logger.info(f"Secrets stored in local file {secret_identifier}.txt")
        return handler()
    except ClientError as ce:
        logger.error(ce.response["Error"]["Message"])


handler()
