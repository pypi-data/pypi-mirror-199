import os


def check_workspace_exit(current_path):
    if current_path == os.path.dirname(current_path):
        return "", False
    for file_name in os.listdir(current_path):
        if ".ndtc" == file_name:
            return current_path, True
    return check_workspace_exit(os.path.dirname(current_path))


