import boto3


def get_client():
    secrets_manager = boto3.client("secretsmanager")
    return secrets_manager
