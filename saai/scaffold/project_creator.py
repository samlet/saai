from typing import Text, Optional
from rasa.cli.utils import create_output_path, print_success
import os
import rasa
from rasa.constants import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_DATA_PATH,
    DEFAULT_DOMAIN_PATH,
    DOCS_BASE_URL,
)

def scaffold_path(proto) -> Text:
    import pkg_resources

    return pkg_resources.resource_filename(__name__, f"initial_{proto}")

def create_initial_project(path: Text, proto:Text) -> None:
    from distutils.dir_util import copy_tree

    copy_tree(scaffold_path(proto), path)
    print("Created project directory at '{}'.".format(os.path.abspath(path)))

def train_project(path: Text) -> Optional[Text]:
    print_success("Training an initial model...")
    config = os.path.join(path, DEFAULT_CONFIG_PATH)
    training_files = os.path.join(path, DEFAULT_DATA_PATH)
    domain = os.path.join(path, DEFAULT_DOMAIN_PATH)
    output = os.path.join(path, create_output_path())

    model = rasa.train(domain, config, training_files, output)
    return model

def rasa_shell(model: Text):
    from rasa.core import constants
    from rasa.cli.shell import shell
    import argparse
    args=argparse.Namespace(model=model)
    # provide defaults for command line arguments
    attributes = [
        "endpoints",
        "credentials",
        "cors",
        "auth_token",
        "jwt_secret",
        "jwt_method",
        "enable_api",
        "remote_storage",
    ]
    for a in attributes:
        setattr(args, a, None)

    args.port = constants.DEFAULT_SERVER_PORT

    shell(args)

