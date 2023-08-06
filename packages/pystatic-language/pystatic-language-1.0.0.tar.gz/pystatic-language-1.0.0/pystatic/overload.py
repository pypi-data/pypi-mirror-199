# overload.py

import inspect
from functools import partial
from typing import Callable, Any, Union

from pystatic.types import (
    statictypes, RuntimeTypeError, RuntimeTypeWarning
)

__all__ = [
    "Overload",
    "OverloadProtocol",
    "overload"
]

def is_regular_method(method: Union[Callable, staticmethod, classmethod]) -> bool:
    """
    Checks if the method is not static or class method.

    :returns: The boolean value.
    """

    return not isinstance(method, (staticmethod, classmethod))
# end is_regular_method

def get_callable_method(method: Union[Callable, staticmethod, classmethod]) -> Callable:
    """
    Gets the callable method from the given method.

    :returns: The callable method.
    """

    return method if is_regular_method(method) else method.__func__
# end get_callable_method

class OverloadProtocol:
    """A class to enable the overload inside classes."""

    def __getattribute__(self, key: str) -> Any:
        """
        Gets the attribute value.

        :param key: The name of the attribute.

        :return: The attribute value.
        """

        val = super().__getattribute__(key)

        if isinstance(val, Overload):
            val.instance = self
        # end if

        return val
    # end __getattribute__
# end OverloadProtocol

class Overload:
    """A class to create an overload functionality."""

    def __init__(self, c: Callable) -> None:
        """
        Defines the class attributes.

        :param c: The decorated callable object.
        """

        self.instance = None

        self.c = c

        self.signature = inspect.signature(get_callable_method(c))

        self.signatures = {self.signature: self.c}
    # end __init__

    def overload(self, c: Callable) -> object:
        """
        sets the signature of the decorated overloading callable object in the class.

        :param c: The decorated callable object.

        :return: The current class object.
        """

        self.signatures[inspect.signature(get_callable_method(c))] = c

        return self
    # end overload

    # noinspection PyUnresolvedReferences
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Calls the decorated callable with the overloading match.

        :param args: The positional arguments.
        :param kwargs: The keyword arguments.

        :return: The returned value from the callable call.
        """

        for signature, c in self.signatures.items():
            try:
                if isinstance(c, staticmethod):
                    c = c.__func__

                elif self.instance is not None:
                    if isinstance(c, classmethod):
                        annotations = c.__func__.__annotations__
                        c = partial(c, type(self.instance))
                        c.__annotations__ = annotations

                    else:
                        annotations = c.__annotations__
                        c = partial(c, self.instance)
                        c.__annotations__ = annotations
                    # end if
                # end if

                return statictypes(c)(*args, **kwargs)

            except (RuntimeTypeError, RuntimeTypeWarning, TypeError):
                pass
            # end try

        else:
            c = self.c

            if isinstance(c, staticmethod):
                c = c.__func__

            elif self.instance is not None:
                if isinstance(c, classmethod):
                    annotations = c.__func__.__annotations__
                    c = partial(c, type(self.instance))
                    c.__annotations__ = annotations

                else:
                    annotations = c.__annotations__
                    c = partial(c, self.instance)
                    c.__annotations__ = annotations
                # end if
            # end if

            print(self.instance)

            return c(*args, **kwargs)
        # end for
    # end __call__
# end Overload

overload = Overload