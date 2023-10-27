import os 

def get_username():
    directory = os.getcwd()
    name = directory.split("/")[2]
    return name