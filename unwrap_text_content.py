import json


def unwrap_text_content(result):
    if isinstance(result, list) and len(result) == 1 and hasattr(result[0], "text"):
        return json.loads(result[0].text)
    return result
