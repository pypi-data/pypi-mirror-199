from typing import Dict, Union

__all__ = ["Pause"]


Pause = Dict[str, Union[bool, int]]
AutoPause = Dict[str, Pause]
