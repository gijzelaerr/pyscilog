from typing import Dict, Any


class State(dict):
    """
    Borg pattern to store global state
    """
    _shared_state: Dict[Any, Any] = {}

    def __init__(self):
        super().__init__()
        self.__dict__ = self._shared_state

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        print(key)