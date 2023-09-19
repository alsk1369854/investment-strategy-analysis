from typing import Dict, Any, List
from inspect import isclass


class BasicUtil:
    @staticmethod
    def get_class_annotations(_class: object) -> Dict[str, Any]:
        if isclass(_class):
            return _class.__dict__["__annotations__"]

        raise TypeError(f"{_class} is not a class")

    @staticmethod
    def get_create_data_frame_data(data_mode: object) -> Dict[str, List[Any]]:
        result: Dict[str, List[Any]] = {}
        data_mode.__dict__
        for key in data_mode.__dict__:
            value: Any = data_mode.__dict__[key]
            result[key] = [value]
        return result
