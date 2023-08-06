import json
import os
import sys

import pytest

# path relative to project root or module root
#   In IntelliJ the app is a module within project, so file must be relative to module
#   In PyCharm the app itself is a project, so file must be relative to project
#
SRC_DIR_JSON = "dk_site_packages.json"


def get_virtual_env():
    try:
        return os.environ["VIRTUAL_ENV"]
    except KeyError as er:
        print(f'environment variable VIRTUAL_ENV is not set. make sure you run this in a venv')
        exit(1)


@pytest.fixture(scope="session")
def project_root():
    if is_test_executing_in_lambda_runtime():
        return "/tmp/source_clone/python-samples/crudster"
    # return os.path.dirname(get_virtual_env()) + "/crudster"
    return os.path.dirname(get_virtual_env())


def is_test_executing_in_lambda_runtime():
    if os.environ.get("TEST_INVOKED_FROM_LAMBDA") == "True":
        if os.environ.get("AWS_EXECUTION_ENV") == "AWS_Lambda_python3.8":
            print('this implies we are now executing in the cloud inside lambda runtime, '
                  'so there is no need to set sys.path')
            return True
        else:
            print('this implies we are now executing lambda like env but not in cloud, '
                  'so we still need set sys.path')
            # temporary hack
            # FIXME i forget in what condition this applies
            # in docker env running local AWS_EXECUTION_ENV is not set, so for now
            # pretend as if this is cloud env
            return True
    else:
        print('this implies we are not executing in lambda like env, '
              'so we need set sys.path to make it look like lambda')
    return False


@pytest.fixture(scope="module")
def prepend_to_sys_path(project_root):
    """
    this fixture returns a function that takes a directory as input, appends it to the project root directory
    and this resulting directory is inserted into sys path
    :return:
    """

    print(f'prepend_to_sys_path: BEFORE ')
    saved_dir_name = None

    def twice(dir_name):
        sys.path.insert(0, project_root + dir_name)
        nonlocal saved_dir_name
        saved_dir_name = project_root + dir_name
        print(f'prepend_to_sys_path: SET {sys.path=}, just added to path {saved_dir_name}')

    yield twice

    sys.path.remove(saved_dir_name)
    print(f'prepend_to_sys_path: AFTER {sys.path=}, just removed from path {saved_dir_name}')


@pytest.fixture(scope="session", autouse=True)
def setup_sys_path(project_root):
    print(f'setup_sys_path {sys.path=}')
    print(f'setup_sys_path {os.getcwd()=}')
    insert_index = 0
    if not is_test_executing_in_lambda_runtime():
        # get VIRTUAL_ENV. if this is not set, throw fits;
        venv_dir = get_virtual_env()
        #   example: VIRTUAL_ENV=/Users/dmkamath/develop/concepts/gh/aprepos/python-samples/venv-py-samples

        # verify python version is 3.9;
        print(f'found python version {sys.version}')
        if not (sys.version_info.major == 3 and sys.version_info.minor == 9):
            print(f'you do not have version 3.8.x')
            exit(1)

        # verify there is valid site-packages directory in the venv
        venv_site_package = f'{venv_dir}/lib/python3.9/site-packages'
        if not os.path.isdir(venv_site_package):
            print(f'{venv_site_package} is not a valid directory')
            exit(1)

        # if you run pytest as pytest (from terminal) you need this.
        # if you run pytest as `python -m pytest` (from terminal) you don't need this (as python adds CWD to sys.path)
        # if you run pytest from IDE run menu you don't need this, PyCharm adds CWD, project root, source root to sys.path
        sys.path.insert(insert_index, project_root)
        insert_index += 1

        # add venv site-packages directory to sys.path
        sys.path.insert(insert_index, venv_site_package)
        insert_index += 1

    # get list of layer directories (site-packages).
    #   get this from dk_src_layout.json
    #   expect this file to be at the same level as venv (in dataknox)
    #   expect this file to be at predefined level "crudster/dk_site_packages.json"
    try:
        with open(f'{project_root}/{SRC_DIR_JSON}', 'r') as f:
            src_layout = json.load(f)
    except FileNotFoundError as e:
        raise e

    for idx, layer_dir in enumerate(src_layout):
        sys.path.insert(insert_index + idx, project_root + "/" + layer_dir)

    # this is a hack. pytest's conftest.py does have this setup but when aws_clients
    # get initialized
    os.environ["AWS_REGION"] = "us-east-2"

    print(f'end_some_info {sys.path=}')


print(f'i am here')
