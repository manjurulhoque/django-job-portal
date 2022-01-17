from typing import NamedTuple, Optional


class Checking(NamedTuple):
    passed: bool = True
    message: Optional[str] = None
    params: dict = dict()
