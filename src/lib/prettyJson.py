import json
import html

def printPretty(jsonDict):
    return json.dumps(jsonDict, sort_keys=True, indent= 4, separators=(',', ': ')).replace('\\n', '\\\\n')