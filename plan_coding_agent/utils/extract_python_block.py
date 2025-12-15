import re
from typing import Optional


def extract_python_block(text: str):
    match = re.search(
        r"```python[ \t]*\n(.*?)\n```",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    return match.group(1) if match else None
