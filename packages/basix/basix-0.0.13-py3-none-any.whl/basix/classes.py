import inspect
from typing import Any, Type


def validate_constructor_args(cls: Type) -> Type:
    """
    A decorator that validates the arguments passed to a class's __init__ method using the
    _validate_{arg_name} methods defined on the class. It also sets the validated arguments as
    attributes of the instance.

    Parameters
    ----------
    cls : Type
        The class to validate.

    Returns
    -------
    Type
        The class with the __init__ method validated and attributes set.
    """

    original_init = cls.__init__

    fullargspec = inspect.getfullargspec(original_init)

    arg_names = fullargspec.args

    default_values = list(fullargspec.defaults or [])

    while len(default_values) < len(arg_names):
        default_values.insert(0, None)

    arg_defaults = [
        [name, default]
        for name, default in zip(arg_names, default_values)
        if name != "self"
    ]

    args_values = [[k, v] for k, v in arg_defaults if v is None]

    kwargs_values = {k: v for k, v in arg_defaults if v is not None}

    def new_init(self, *args: Any, **kwargs: Any) -> None:

        base_args = args_values.copy()

        base_kwargs = kwargs_values.copy()

        for i in range(len(args)):
            name = base_args[i][0]
            val = base_args[i][1] = args[i]
            validator = getattr(cls, f"_validate_{name}", None)
            if validator:
                base_args[i][1] = validator(cls, val)
            setattr(self, name, val)

        for name, val in base_kwargs.items():
            if name in kwargs:
                base_kwargs[name] = kwargs[name]
            validator = getattr(cls, f"_validate_{name}", None)
            if validator:
                base_kwargs[name] = validator(cls, val)
            setattr(self, name, val)

        new_args = tuple([x[1] for x in base_args])

        original_init(self, *new_args, **base_kwargs)

    cls.__init__ = new_init

    return cls
