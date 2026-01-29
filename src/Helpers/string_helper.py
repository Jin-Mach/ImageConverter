import os
from pathlib import Path

def validate_path(path: str, limit: int = 40) -> str:
    if not path:
        return ""

    path = Path(path)
    path_parts = list(path.parts)
    final_parts = []
    while path_parts:
        part = path_parts.pop()
        final_parts.insert(0, part)
        current_path = os.sep.join(final_parts)
        if len(current_path) > limit:
            final_parts.pop(0)
            break
    validated_path = os.sep.join(final_parts)
    return "..." + validated_path