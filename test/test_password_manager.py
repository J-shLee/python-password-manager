from src.password_manager import insert_secret, get_client, list_secrets, delete_secret
import moto 
from moto import mock_secretsmanager
import os
import pytest
import boto3
import json
import logging

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@mock_secretsmanager
class TestInsertSecretsTest():
    def test_secretsmanager_logs_correct_message_when_invoked_with_valid_inputs(self, caplog):
        with caplog.at_level(logging.INFO):
        
            insert_secret('secretid', 'userid', 'password')
            
            assert ('Secret Saved' in caplog.text)

    def test_raises_resource_exists_exception_when_name_of_secret_is_already_used(self, caplog):
        """captures as client error"""
        with caplog.at_level(logging.INFO):

            insert_secret('secretid', 'userid', 'password')
            insert_secret('secretid', 'userid', 'password')
        
            assert ('A resource with the ID you requested already exists.' in caplog.text)

    def test_raises_parameter_validation_error_if_invalid_inputs_provided(self, caplog):
        """captures as client error"""
        with caplog.at_level(logging.INFO):

            insert_secret(['secretid'], 'user_id', 'password')

            assert ('Parameter validation failed' in caplog.text)

@mock_secretsmanager
class TestListSecrets():
    def test_returns_correct_message_when_no_secrets_stored(self, caplog):
        with caplog.at_level(logging.INFO):
            list_secrets()

            assert ('There are no secrets' in caplog.text)

    def test_returns_correct_message_when_no_secrets_stored(self, caplog):
        with caplog.at_level(logging.INFO):
            insert_secret('a', 'a', 'a')
            list_secrets()

            assert ("1 secret(s) available: \n['a']" in caplog.text)

    def test_raises_client_error(self, caplog):
        pass
    # """captures as client error"""
    # with caplog.at_level(logging.INFO):

    #     insert_secret('secretid', 'userid', 'password')
    #     insert_secret('secretid', 'userid', 'password')
    
    #     assert ('A resource with the ID you requested already exists.' in caplog.text)


@mock_secretsmanager
class TestDeleteSecrets():
    def test_returns_correct_message_when_secret_successfully_deleted(self, caplog):
        with caplog.at_level(logging.INFO):
            insert_secret('a', 'a', 'a')
            delete_secret('a')

            assert ('Secret Deleted: a' in caplog.text)

    # def test_returns_correct_message_when_no_secrets_stored(self, caplog):
    #     with caplog.at_level(logging.INFO):
    #         insert_secret('a', 'a', 'a')
    #         list_secrets()

    #         assert ("1 secret(s) available: \n['a']" in caplog.text)

    # def test_raises_client_error(self, caplog):