import json
import pkg_resources


def get_file_format(filename: str) -> str:
    parts = filename.split(".")
    if len(parts) == 2:
        return parts[1]
    else:
        raise ValueError(f"Unrecognised filename format '{filename}': Unable to split strings")


def read_config() -> dict:
    with pkg_resources.resource_stream('capsphere', 'config/schema.json') as f:
        return json.load(f)
