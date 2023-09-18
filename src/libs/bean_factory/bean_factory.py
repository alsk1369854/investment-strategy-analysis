from typing import Dict, Any, Type, TypeVar, cast
from inspect import isclass


T = TypeVar("T")


class BeanFactory:
    _bean_count: int = 0
    _bean_dict: Dict[Type[object], object] = {}

    # @staticmethod
    # def init():
    #     BeanFactory._init_bean_instance_dependency_injection()

    # @staticmethod
    # def _init_bean_instance_dependency_injection():
    #     for bean_class in BeanFactory._bean_dict:
    #         bean_instance: object = BeanFactory._bean_dict[bean_class]
    #         BeanFactory._dependency_injection(bean_instance)

    @staticmethod
    def _dependency_injection(bean_instance: T):
        bean_class: Type[T] = bean_instance.__class__
        bean_class_dict: Dict[str, Any] = getattr(bean_class, "__dict__")
        if "__annotations__" not in bean_class_dict:
            return

        class_annotations_dict: Dict[str, Any] = bean_class_dict["__annotations__"]
        for attr_name in class_annotations_dict:
            attr_var: Any = class_annotations_dict[attr_name]
            if isclass(attr_var) and (attr_var in BeanFactory._bean_dict):
                dependency_bean_instance: object = BeanFactory._bean_dict[attr_var]
                setattr(bean_instance, attr_name, dependency_bean_instance)

    @staticmethod
    def _add_bean_class(bean_class: Type[T]):
        if isclass(bean_class):
            bean_instance: T = bean_class()
            BeanFactory._bean_count += 1
            setattr(bean_instance, "_bean_number", BeanFactory._bean_count)

            BeanFactory._dependency_injection(bean_instance)
            BeanFactory._bean_dict[bean_class] = bean_instance

    @staticmethod
    def get_bean(bean_class: Type[T]) -> T:
        if not isclass(bean_class):
            raise TypeError(f"{bean_class} is not a class type")

        if not (bean_class in BeanFactory._bean_dict):
            raise RuntimeError(f"{bean_class} not found")

        return cast(T, BeanFactory._bean_dict[bean_class])


def bean(bean_class: Type[T]) -> Type[T]:
    BeanFactory._add_bean_class(bean_class)
    return bean_class
