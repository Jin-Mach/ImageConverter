import os
import pathlib


def validate_path(path: str) -> str:
    validate_list = []
    validated_path = ""
    if path is None:
        return validated_path
    path = pathlib.Path(path)
    for item in reversed(path.parts):
        validate_list.append(item)
        text_path = os.sep.join(validate_list)
        if len(text_path) > 20:
            validate_list.reverse()
            validated_path = os.sep.join(validate_list)
            break
    return f"...{validated_path}"
