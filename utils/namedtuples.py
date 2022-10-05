from typing import NamedTuple
from typing import Optional


class Checking(NamedTuple):
    passed: bool = True
    message: Optional[str] = None
    params: dict = dict()
