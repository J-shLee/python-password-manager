import boto3
import moto
import json

# put in a function??
client = boto3.client("secretsmanager")


def handler():
    valid_inputs = {
        "e": insert_secret,
        "r": retrieve_secret,
        "d": delete_secret,
        "l": list_secrets,
    }

    user_input = input(
        "Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:"
    ).lower()

    if user_input == "x":
        print("Thank you. Goodbye")
        return
    elif user_input in valid_inputs:
        function = valid_inputs[user_input]
        return function()
    else:
        print("Invalid input")
        return handler()


def insert_secret():
    try:
        secret_identifier = input("What name would you like to give this secret?")
        user_id = input("What is the username you'd like to save?")
        password = input("What is the password you'd like to save?")
        json_upload = {"user_id": user_id, "password": password}

        response = client.create_secret(
            Name=secret_identifier, SecretString=json.dumps(json_upload)
        )

        # result of print(response) -- successful upload >>>>>> {
        # 'ARN': 'arn:aws:secretsmanager:eu-west-2:039843163800:secret:zzzz-CpzmUZ', 'Name': 'zzzz',
        # 'VersionId': '05f71c9e-20c0-415a-9d67-943d9649673e', 'ResponseMetadata': {'RequestId': 'd4070677-281d-4b86-8089-bf6aca6b4546',
        # 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'd4070677-281d-4b86-8089-bf6aca6b4546', 'content-type': 'application/x-amz-json-1.1', 'content-length': '139', 'date': 'Wed, 25 Oct 2023 18:37:28 GMT'}, 'RetryAttempts': 0}}

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("Secret Saved")
            return handler()
        #     # return handler function to go back to main menu
        # else:
        #     print(response, "ENTERING ELSE")
        #     raise error
    except:
        pass
        # print error message and return handler function


# insert_secret()


def list_secrets():
    response = client.list_secrets()

    # print(response)

    # print(response) result while there was 1 item in the bucket >>>
    # {'SecretList': [{
    # 'ARN': 'arn:aws:secretsmanager:eu-west-2:039843163800:secret:zzzz-CpzmUZ',
    # 'Name': 'zzzz',
    # 'LastChangedDate': datetime.datetime(2023, 10, 25, 19, 37, 29, 592000, tzinfo=tzlocal()),
    # 'SecretVersionsToStages': {'05f71c9e-20c0-415a-9d67-943d9649673e': ['AWSCURRENT']},
    # 'CreatedDate': datetime.datetime(2023, 10, 25, 19, 37, 29, 389000, tzinfo=tzlocal())}],
    # 'ResponseMetadata': {'RequestId': 'a257fe28-f671-48a1-9a1d-e94a85274c6b',
    # 'HTTPStatusCode': 200,
    # 'HTTPHeaders': {'x-amzn-requestid': 'a257fe28-f671-48a1-9a1d-e94a85274c6b',
    # 'content-type': 'application/x-amz-json-1.1',
    # 'content-length': '252',
    # 'date': 'Wed, 25 Oct 2023 18:48:14 GMT'},
    # 'RetryAttempts': 0}}

    # print(response) when there was no items in the bucket >>>>>>
    # {'SecretList': [],
    # 'ResponseMetadata': {'RequestId': '1a19d297-65eb-4775-a643-c98a4d9ee36b',
    # 'HTTPStatusCode': 200,
    # 'HTTPHeaders': {'x-amzn-requestid': '1a19d297-65eb-4775-a643-c98a4d9ee36b',
    # 'content-type': 'application/x-amz-json-1.1',
    # 'content-length': '17',
    # 'date': 'Wed, 25 Oct 2023 19:04:27 GMT'},
    # 'RetryAttempts': 0}}

    if len(response["SecretList"]) == 0:
        print("There are no secrets")
        return handler()
    else:
        secrets = [secret["Name"] for secret in response["SecretList"]]
        print(f"{len(secrets)} secret(s) available: \n{secrets}")
        return handler()


def delete_secret():
    try:
        secret_identifier = input(
            "What's the name of the secret you would like to delete?"
        )

        response = client.delete_secret(SecretId=secret_identifier)

        print(response)
        # result of print(response) after deleting the only item in the bucket
        # {'ARN': 'arn:aws:secretsmanager:eu-west-2:039843163800:secret:zzzz-CpzmUZ',
        # 'Name': 'zzzz',
        # 'DeletionDate': datetime.datetime(2023, 11, 24, 19, 0, 43, 426000, tzinfo=tzlocal()),
        # 'ResponseMetadata': {'RequestId': 'be695dc5-f092-4f09-9027-321de30cb92b',
        # 'HTTPStatusCode': 200,
        # 'HTTPHeaders': {'x-amzn-requestid': 'be695dc5-f092-4f09-9027-321de30cb92b',
        # 'content-type': 'application/x-amz-json-1.1',
        # 'content-length': '120',
        # 'date': 'Wed, 25 Oct 2023 19:00:43 GMT'},
        # 'RetryAttempts': 0}}

        if response.HTTPStatusCode == 200:
            print("Deleted")
            return handler()
        else:
            # raise error
            pass
    except:
        # print error message and return handler function to return to main menu
        pass


def retrieve_secret(secret_identifier=None):
    try:
        secret_identifier = input(
            "What is the name of the secret you would like to retrieve?"
        )

        response = client.get_secret_value(SecretId=secret_identifier)

        secret = json.loads(response["SecretString"])

        secret_txt = open(f"{secret_identifier}.txt", "w")
        secret_txt.write(
            f'User ID = {secret["user_id"]} \nPassword = {secret["password"]}'
        )
        secret_txt.close()

        return handler()
    except:
        pass
        # error message when given an id which doesn't exist
        # raise error_class(parsed_response, operation_name)
        # botocore.errorfactory.ResourceNotFoundException: An error occurred (ResourceNotFoundException) when calling the GetSecretValue operation: Secrets Manager can't find the specified secret.

        # error message when retrieving a secret which has or is going to be deleted
        # raise error_class(parsed_response, operation_name)
        # botocore.errorfactory.InvalidRequestException: An error occurred (InvalidRequestException) when calling the GetSecretValue operation:


handler()
