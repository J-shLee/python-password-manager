from src.password_manager import (
    insert_secret,
    get_client,
    list_secrets,
    delete_secret,
    retrieve_secret,
    handler,
)
import moto
from moto import mock_secretsmanager
import os
import pytest
import boto3
import json
import logging
from unittest import mock
from unittest.mock import patch

logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@mock_secretsmanager
class TestInsertSecretsTest:
    def test_secretsmanager_logs_correct_message_when_invoked_with_valid_inputs(
        self, caplog
    ):
        with caplog.at_level(logging.INFO):
            insert_secret("secretid", "userid", "password")

            assert "Secret Saved" in caplog.text

    def test_raises_resource_exists_exception_when_name_of_secret_is_already_used(
        self, caplog
    ):
        """captures as client error"""
        with caplog.at_level(logging.INFO):
            insert_secret("secretid", "userid", "password")
            insert_secret("secretid", "userid", "password")

            assert "A resource with the ID you requested already exists." in caplog.text

    def test_raises_parameter_validation_error_if_invalid_inputs_provided(self, caplog):
        """captures as client error"""
        with caplog.at_level(logging.INFO):
            insert_secret(["secretid"], "user_id", "password")

            assert "Parameter validation failed" in caplog.text


@mock_secretsmanager
class TestListSecrets:
    def test_returns_correct_message_when_no_secrets_stored(self, caplog):
        with caplog.at_level(logging.INFO):
            list_secrets()

            assert "There are no secrets" in caplog.text

    def test_returns_correct_message_when_secrets_stored(self, caplog):
        with caplog.at_level(logging.INFO):
            insert_secret("a", "a", "a")
            list_secrets()

            assert "1 secret(s) available: \n['a']" in caplog.text

    # def test_raises_client_error(self, caplog):
    #     with patch('../src.password_manager.get_client', return_value=None):

    #         with caplog.at_level(logging.INFO):

    #             list_secrets()


@mock_secretsmanager
class TestDeleteSecrets:
    def test_returns_correct_message_when_secret_successfully_deleted(self, caplog):
        with caplog.at_level(logging.INFO):
            insert_secret("a", "a", "a")
            delete_secret("a")

            assert "Secret Deleted: a" in caplog.text

    def test_captures_client_error_when_secret_does_not_exist(self, caplog):
        with caplog.at_level(logging.INFO):
            delete_secret("a")

            assert "Secrets Manager can't find the specified secret" in caplog.text

    # def test_raises_client_error(self, caplog):


@mock_secretsmanager
class TestRetrieveSecret:
    def test_returns_correct_message_when_secret_successfully_retreived(self, caplog):
        with caplog.at_level(logging.INFO):
            insert_secret("a", "a", "a")
            retrieve_secret("a")

            assert f"Secrets stored in local file a.txt" in caplog.text

    def test_creates_new_file_containing_correct_secret_info(self):
        insert_secret("a", "a", "a")
        retrieve_secret("a")
        directory = os.getcwd()
        assert os.path.exists(f"{directory}/secrets/a.txt") == True

    def test_correct_content_is_inside_the_file(self):
        insert_secret("a", "a", "a")
        retrieve_secret("a")
        directory = os.getcwd()

        secret_txt = open(f"{directory}/a.txt", "r")
        lines = secret_txt.readlines()
        assert lines[0] == "User ID = a \n"
        assert lines[1] == "Password = a"

    def test_returns_client_error_if_secret_doesnt_exist(self, caplog):
        with caplog.at_level(logging.INFO):
            retrieve_secret("a")

            assert "Secrets Manager can't find the specified secret" in caplog.text


class TestHandler:
    def test_handler_invokes_insert_secret_with_user_input_e(self):
        with patch("src.password_manager.insert_secret", return_value=True) as mock:
            assert handler("e") == True
            assert mock.call_count == 1

    def test_handler_invokes_list_secrets_with_user_input_l(self):
        with patch("src.password_manager.list_secrets", return_value=True) as mock:
            assert handler("l") == True
            assert mock.call_count == 1

    def test_handler_invokes_delete_secrets_with_user_input_d(self):
        with patch("src.password_manager.delete_secret", return_value=True) as mock:
            assert handler("d") == True
            assert mock.call_count == 1

    def test_handler_invokes_delete_secrets_with_user_input_r(self):
        with patch("src.password_manager.retrieve_secret", return_value=True) as mock:
            assert handler("r") == True
            assert mock.call_count == 1

    def test_handler_logs_correct_message_on_exit(self, caplog):
        with caplog.at_level(logging.INFO):
            handler("x")

            assert "Thank you. Goodbye" in caplog.text
