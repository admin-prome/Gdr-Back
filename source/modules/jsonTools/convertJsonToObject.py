from types import SimpleNamespace

def json_to_object(data):
    if isinstance(data, dict):
        return SimpleNamespace(**{key: json_to_object(value) for key, value in data.items()})
    elif isinstance(data, list):
        return [json_to_object(item) for item in data]
    else:
        return data