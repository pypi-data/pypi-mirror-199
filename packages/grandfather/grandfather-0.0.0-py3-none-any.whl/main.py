import inspect
from typing import Callable, Protocol, Any

PreHook = Callable
PostHook = Callable


class Hook:
    def __init__(self, wrapped_func):
        self.wrapped_func = wrapped_func

    def __call__(self, *args, **kwargs) -> Any:
        raise NotImplementedError


class UnitCore(type):
    hooks: tuple[Hook]

    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)
        print(klass, type(klass))
        method_list = inspect.getmembers(klass, predicate=inspect.isfunction)

        key, func = method_list[1]

        hook_class = self.hooks[0]
        wrapped = hook_class(func)
        setattr(klass, key, wrapped)

def trace(hook_class):

    def _decorator(klass):
        method_list = inspect.getmembers(klass, predicate=inspect.isfunction)

        for key, func in method_list:
            wrapped = hook_class(func)
            setattr(klass, key, wrapped)

        return klass

    return _decorator
