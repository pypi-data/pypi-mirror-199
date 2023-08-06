import re
from typing import Iterator, Callable

from hypersquirrel.literalinterpreter.instagram import interpret as interpret_instagram

interpreters = {
    "^.*instagram.com\/(p|reel)\/[a-zA-z0-9-_]*.$": interpret_instagram
}


def get_interpreter(url: str) -> Callable[[str], Iterator[dict]]:
    for regex, interpreter in interpreters.items():
        if re.match(regex, url):
            return interpreter
