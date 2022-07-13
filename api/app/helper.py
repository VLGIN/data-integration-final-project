import json
from bson import json_util


def cursor_list_to_list(cursor_list):
    return json.loads(json_util.dumps(cursor_list))
