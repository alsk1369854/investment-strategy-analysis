from typing import Dict, Callable, TypeVar, Any, List, Optional


T = TypeVar("T")

PubSubCallback = Callable[[str, Optional[T]], None]


class PubSub:
    callback_dict: Dict[str, List[PubSubCallback]] = {}

    @staticmethod
    def subscribe(name: str, callback: PubSubCallback) -> str:
        if not (name in PubSub.callback_dict):
            PubSub.callback_dict[name] = []

        PubSub.callback_dict[name].append(callback)

    @staticmethod
    def publish(name: str, data: Optional[T] = None):
        if not (name in PubSub.callback_dict):
            return

        callback_list = PubSub.callback_dict[name]
        for callback in callback_list:
            callback(name, data)

    @staticmethod
    def unsubscribe(name: str, callback: PubSubCallback):
        if not (name in PubSub.callback_dict):
            return

        PubSub.callback_dict[name].remove(callback)
