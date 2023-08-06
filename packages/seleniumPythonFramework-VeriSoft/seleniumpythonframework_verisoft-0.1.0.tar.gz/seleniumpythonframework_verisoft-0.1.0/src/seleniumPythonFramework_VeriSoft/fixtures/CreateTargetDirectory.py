import os
from os.path import dirname
import pytest
"""
creates target directory with necessary folders for the files created out of the build.

@Author: Efrat Cohen
@Date: 12.2022
"""


def before_all(project_path):
    """
    check if target directory exist, if not - create this directory with screenshots folder in.
    """
    # Get project path
    infra_project_path = dirname(dirname(__file__))

    # Store the project user directory param in pytest global variables
    pytest.user_dir = project_path

    # Specify path
    path = project_path + "/target"

    # Check whether the specified path exists or not
    isExist = os.path.exists(path)

    if not isExist:
        # Create target directory
        os.makedirs(project_path + "/target", exist_ok=True)

        # Create screenshots folder in target directory
        os.makedirs(project_path + "/target/screenshots", exist_ok=True)

