from typing import Dict, Any
from uuid import uuid4
from inspect import isclass


class UuidUtil:
    @staticmethod
    def get_general_uuid() -> str:
        return str(uuid4())
