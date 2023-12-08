import os


def get_username():
    """
    this function retrieves the user name of the user

    Parameters
    ----------
        none

    Returns
    ----------
        returns: name of user
    """
    directory = os.getcwd()
    name = directory.split("/")[2]
    return name
