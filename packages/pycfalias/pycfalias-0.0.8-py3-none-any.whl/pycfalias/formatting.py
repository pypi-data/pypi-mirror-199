import json
from prettytable import PrettyTable, from_json


def format_table(data):
    j = []

    j.append(["name", "alias", "type", "dest", "enabled"])
    for i in data['result']:
        if i['matchers'][0]['type'] == "literal":
            j.append({
                "name": i.get("name", " "),
                "alias": i.get("matchers")[0].get("value", " "),
                "type": i.get("actions")[0].get("type", " "),
                "dest": i.get("actions")[0].get("value", " ")[0],
                "enabled": i.get("enabled", " ")
            })
    
    table = PrettyTable()
    table = from_json(json.dumps(j))

    return table
