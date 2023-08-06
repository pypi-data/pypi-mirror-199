import json
from prettytable import PrettyTable, from_json


def format_table(data):
    j = []

    j.append(["name", "alias", "type", "dest", "enabled"])
    for i in data['result']:
        if i['matchers'][0]['type'] == "literal":
            j.append({
                "name": i["name"],
                "alias": i["matchers"][0]["value"],
                "type": i["actions"][0]["type"],
                "dest": i["actions"][0]["value"][0],
                "enabled": i["enabled"]
            })

    table = PrettyTable()
    table = from_json(json.dumps(j))

    return table
