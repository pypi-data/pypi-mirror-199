import pathlib
import os
import sys
import toml



def get_config():
    cf_auth = {
        "CF_FORWARD_EMAIL": os.getenv("CF_FORWARD_EMAIL"),
        "CF_TOKEN": os.getenv("CF_TOKEN"),
        "CF_ZONE": os.getenv("CF_ZONE")
    }

    path = pathlib.Path(pathlib.Path.home(), '.pycfalias.toml')
    if not path.is_file():
        # Environment variables take precendence
        return cf_auth
    # Return the configuration directly from the file
    return toml.load(path)


def validate_config(config):
    if None in config.values() or "" in config.values():
        msg = "Error: Missing values in the configuration,  \
               check environment variables or configuration file"
        sys.exit(msg)
