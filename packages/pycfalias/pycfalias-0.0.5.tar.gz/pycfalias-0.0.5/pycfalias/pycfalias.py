from datetime import datetime as dt
import sys
import argparse
import requests
from . import config
from . import formatting
#from config import get_config, validate_config
#from formatting import format_table


CF_URI = "https://api.cloudflare.com/client/v4/zones/{zone}/email/routing/rules"


def get_email_aliases():
    conf = config.get_config()
    headers = {
        "Authorization": "Bearer " + conf.get("CF_TOKEN")
    }

    try:
        resp = requests.get(CF_URI.format(
            zone=conf.get("CF_ZONE")), headers=headers, timeout=3)
    except ConnectionError as err:
        print(err)

    return resp.json()


def create_email_alias(dest):
    conf = config.get_config()

    headers = {
        "Authorization": "Bearer " + conf.get("CF_TOKEN")
    }

    time = dt.utcnow()
    timestamp = time.isoformat(timespec='milliseconds')
    default_name = f"Rule created at {timestamp}Z"

    payload = {
        "actions": [
            {
                "type": "forward",
                        "value": [conf.get("CF_FORWARD_EMAIL")]
            }
        ],
        "enabled": True,
        "matchers": [
            {
                "field": "to",
                "type": "literal",
                "value": dest
            }
        ],
        "name": default_name,
        "priority": 0
    }

    try:
        resp = requests.request("POST", CF_URI
                                .format(zone=conf.get("CF_ZONE")), json=payload,
                                        headers=headers, timeout=3)
    except ConnectionError as err:
        print(err)

    return resp


def remove_email_alias(alias):
    ruleid = ""
    conf = config.get_config()

    headers = {
        "Authorization": "Bearer " + conf.get("CF_TOKEN")
    }

    data = get_email_aliases()

    try:
        ruleid = [i["tag"] for i in data["result"] if i["matchers"][0]
                  ["type"] == "literal" and i["matchers"][0]["value"] == alias][0]
    except IndexError:
        sys.exit("Error: Unable to find alias")

    try:
        resp = requests.request("DELETE", CF_URI
                                .format(zone=conf.get("CF_ZONE")) + '/' + ruleid,
                                        headers=headers, timeout=3)
    except ConnectionError as err:
        print(err)

    return resp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", help="List email aliases",
                        required=False, action="store_true")
    parser.add_argument(
        "-c", "--create", help="Create new email alias", required=False)
    parser.add_argument(
        "-r", "--remove", help="Remove email alias", required=False)

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    if args.list:
        table = formatting.format_table(get_email_aliases())
        print(table)
    elif args.create:
        create_email_alias(args.create)
    elif args.remove:
        remove_email_alias(args.remove)


if __name__ == "__main__":
    config.validate_config(config.get_config())
    main()
