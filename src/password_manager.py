from src.utils.util_list_secrets import list_secrets
from src.utils.util_delete_secret import delete_secret
from src.utils.util_retrieve_secret import retrieve_secret
from src.utils.util_insert_secret import insert_secret
from src.utils.util_get_username import get_username

import logging

logging.basicConfig()
logger = logging.getLogger(" Password_manager")
logger.setLevel(logging.INFO)


def handler(user_input=None):
    name = get_username()

    g = "\033[0;33m"
    r = "\033[0;31m"
    n = "\033[0m"

    try:
        valid_inputs = {
            "e": insert_secret,
            "r": retrieve_secret,
            "d": delete_secret,
            "l": list_secrets,
        }

        if user_input is None:
            user_input = input(
                f"Please specify {g}[e]{n}ntry, {g}[r]{n}etrieval, {r}[d]{n}eletion, {g}[l]{n}isting or e{r}[x]{n}it: "  # noqa E501
            ).lower()

        if user_input == "x":
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


if __name__ == "__main__":
    handler()
