import subprocess
from nvos import login, file, utils
import os
import daemon
import time
import logging
import concurrent.futures
import platform
import json

# 导入全局日志记录器
logger = logging.getLogger()
all_workspace_path = {}


def command_init():
    status = login.check_login_status()
    if not status:
        print("Please login first. you could use login command to login this script")
        return
    workspace_path, success = utils.check_workspace_exit(os.getcwd())
    init_path = os.path.join(workspace_path, ".ndtc", "init")
    if os.path.exists(init_path):
        with open(init_path, 'r') as f:
            line = f.readlines()
        if line == workspace_path:
            print("Don't repeat execute init command or executor init command in a subdirectory")
            return
    file.init_work_space(workspace_path)


def command_async():
    workspace_path, success = common_verify()
    if not success:
        return
    all_workspace_path.update({workspace_path: workspace_path})
    if platform.system() == 'Windows':
        return
    with open(os.path.expanduser(os.path.join("~", "workspace")), "w") as f:
        f.write(json.dumps(all_workspace_path))

    proc1 = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'ndtc'], stdin=proc1.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc1.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.
    out, err = proc2.communicate()
    number = 0
    for line in out.splitlines():
        if 'ndtc' in str(line).lower() and 'python' in str(line).lower():
            number = number + 1
    if number > 1:
        return
    preserve_fds = [handler.stream for handler in logger.handlers]
    with daemon.DaemonContext(files_preserve = preserve_fds):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                for temp in all_workspace_path.keys():
                    logger.info("command_async current run workspace is " + temp)
                    executor.submit(file.pull_data_from_cloud, temp)
                time.sleep(10)


def command_pull():
    workspace_path, success = common_verify()
    if not success:
        return
    file.pull_data_from_cloud(workspace_path)


def common_verify():
    workspace_path, success = utils.check_workspace_exit(os.getcwd())
    if not success:
        print(
            "Please executor this command that your before executor init command of directory or subdirectory, or you can  executor init this directory")
        return workspace_path, False
    status = login.check_login_status()
    if not status:
        print("Please login first. you could use login command to login this script")
        return workspace_path, False
    return workspace_path, True
