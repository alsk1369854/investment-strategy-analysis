from typing import Dict, Any
from inspect import isclass


class BasicUtil:
    @staticmethod
    def get_class_annotations(_class: object) -> Dict[str, Any]:
        if isclass(_class):
            return _class.__dict__["__annotations__"]

        raise TypeError(f"{_class} is not a class")
