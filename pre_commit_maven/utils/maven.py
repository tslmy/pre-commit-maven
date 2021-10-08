from __future__ import print_function

import os.path

from pre_commit_maven.utils import shell
from pre_commit_maven.utils.shell import ExecutionResult

MAVEN_CLI_OPTS = ["--batch-mode"]
MAVEN_OPTS = [
    "-client",
    "-XX:+TieredCompilation",
    "-XX:TieredStopAtLevel=1",
    "-Xverify:none",
]


class Colours:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def get_maven_path(cwd: str, shell_runner=shell):
    path = ""
    mvn_wrapper_path = os.path.join(cwd, "mvnw")
    if shell_runner.exists_file(mvn_wrapper_path):
        path = mvn_wrapper_path
    else:
        path = "mvn"
    return path


def execute(args: list, cwd: str, shell_runner=shell, env=os.environ.copy()):
    assert args is not None and len(args) > 0, "args not specified"

    cmd = [get_maven_path(cwd, shell_runner)] + MAVEN_CLI_OPTS + args

    env["MAVEN_OPTS"] = " ".join(MAVEN_OPTS)
    return shell_runner.execute(cmd, cwd=cwd, env=env)


def print_error(execution_result: ExecutionResult, print_fn=print):
    print_fn(execution_result.stdout)
