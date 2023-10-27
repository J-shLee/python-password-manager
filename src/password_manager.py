from src.util_list_secrets import list_secrets
from src.util_delete_secret import delete_secret
from src.util_retrieve_secret import retrieve_secret
from src.util_insert_secret import insert_secret
from src.util_get_username import get_username

import logging
import os

logging.basicConfig()
logger = logging.getLogger(" Password_manager")
logger.setLevel(logging.INFO)


def handler(user_input=None):
    name = get_username()
    try:
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
            # logger.info(f" Thank you, {name}. Goodbye")
            return
        elif user_input in valid_inputs:
            function = valid_inputs[user_input]
            return function()
        else:
            logger.info("Invalid input")
            return handler()
    finally:
        if user_input == "x":
            logger.info(f" Thank you, {name}. Goodbye")
            return

        final_input = input(" Would you like to do something else? y/n: ")

        if final_input.lower() == "y":
            return handler()
        else:
            logger.info(f" Thank you, {name}. Goodbye")
            return


handler()
