import inspect
from dataclasses import dataclass
from typing import Optional, List, Callable, Any
from basix import functions
from loguru import logger
from functools import reduce


@dataclass
class ArgumentProperties:
    """
    A data class representing the properties of a function argument.

    Attributes
    ----------
    name : str
        The name of the argument.
    annotation : Optional[str], optional
        The type annotation of the argument, if specified.
    has_default : Optional[str], optional
        Flag that points if the argument has default value.
    default_value : Optional[str], optional
        The default value of the argument, if specified.
    """

    name: str
    annotation: Optional[str]
    has_default: bool
    default_value: Optional[Any]


@dataclass
class FunctionProperties:
    """
    A data class representing the properties of a function.

    Attributes
    ----------
    name : str
        The name of the function.
    module : str
        The name of the module containing the function.
    result_annotation : str
        The return type annotation of the function.
    args_properties : List[ArgumentProperties]
        A list of ArgumentProperties representing the function's arguments.
    n_not_defaults : int
        The number of non-default arguments in the function.
    n_defaults : int
        The number of arguments with default values in the function.
    non_default_args : List[ArgumentProperties]
        List of non-default arguments.
    default_args : List[ArgumentProperties]
        List of default arguments.
    """

    name: str
    module: str
    result_annotation: str
    args_properties: List[ArgumentProperties]
    n_not_defaults: int
    n_defaults: int
    non_default_args: List[ArgumentProperties]
    default_args: List[ArgumentProperties]


def get_function_properties(function: Callable) -> FunctionProperties:
    """
    Returns the properties of a function.

    Parameters
    ----------
    function : Callable
        The function to get properties for.

    Returns
    -------
    FunctionProperties
        A FunctionProperties object representing the properties of the function.
    """
    sig = inspect.signature(function)

    args_prop = []

    for name, param in sig.parameters.items():
        args_prop.append(
            ArgumentProperties(
                **{
                    "name": param._name,
                    "annotation": param.annotation
                    if not (param.annotation == inspect._empty)
                    else None,
                    "has_default": (param.default != inspect._empty),
                    "default_value": param.default if (param.default != inspect._empty) else None,
                }
            )
        )

    return FunctionProperties(
        **{
            "name": function.__name__,
            "module": function.__module__,
            "result_annotation": sig.return_annotation,
            "args_properties": args_prop,
            "n_not_defaults": sum(1 - int(arg.has_default) for arg in args_prop),
            "n_defaults": sum(int(arg.has_default) for arg in args_prop),
            "non_default_args": list(filter(lambda arg: not arg.has_default, args_prop)),
            "default_args": list(filter(lambda arg: arg.has_default, args_prop)),
        }
    )


class Pipe:
    def __init__(self, *stages: List[Callable]) -> None:
        """
        Initialize the Pipe object.

        Parameters
        ----------
        stages : list of callable objects
            List of stages to include in the pipeline.

        Returns
        -------
        None
        """
        self.stages = self.__validate_stages_input(stages)
        self.functions_properties = self.__get_functions_properties(self.stages)
        self.__validate_functions(self.functions_properties)

    def __call__(self, x) -> Any:
        """
        Call the pipeline with the given input value.

        Parameters
        ----------
        x : any
            Input value to pass through the pipeline.

        Returns
        -------
        any
            Result of the pipeline.
        """
        return self.pipeline(x)

    def pipeline(self, value=None) -> Callable:
        """
        Run the pipeline with the given input value.

        Parameters
        ----------
        value : any, optional
            Input value to pass through the pipeline. If not specified, the
            pipeline will start with None as input.

        Returns
        -------
        any
            Result of the pipeline.
        """
        return reduce(lambda acc, curr: curr(acc), self.stages, value)

    def __get_functions_properties(
        self, stages: List[Callable]
    ) -> List[functions.FunctionProperties]:
        """
        Get the function properties for the given list of stages.

        Parameters
        ----------
        stages : list of callable objects
            List of stages to get properties for.

        Returns
        -------
        list of FunctionProperties objects
            List of function properties for each stage.
        """
        return [functions.get_function_properties(stage) for stage in stages]

    def __validate_stages_input(self, stages: List[Callable]) -> List[Callable]:
        """
        Validate the list of stages passed to the pipeline.

        Parameters
        ----------
        stages : list of callable objects
            List of stages to include in the pipeline.

        Returns
        -------
        list of callable objects
            List of validated stages.
        """
        if len(stages) == 0:
            logger.warning("Any function was passed. Using identity")
            return [lambda x: x]

        return stages

    def __validate_functions(self, stage_properties: List[Callable]) -> None:
        """
        Validate the functions passed to the pipeline.

        Parameters
        ----------
        stage_properties : list of FunctionProperties objects
            List of function properties for each stage.

        Returns
        -------
        None
        """
        for i, stage_prop in enumerate(stage_properties):
            self.__validate_single_function(stage_prop, i)

    def __validate_single_function(
        self, stage_properties: functions.FunctionProperties, order: int
    ) -> None:
        """
        Validate a single function passed to the pipeline.

        Parameters
        ----------
        stage_properties : FunctionProperties object
            Function properties for the stage.

        order : int
            Order of the stage in the pipeline.

        Returns
        -------
        None
        """
        if stage_properties.n_not_defaults > 1:
            message = (
                f"The stage {1+order} named {stage_properties.module}.{stage_properties.name} "
                "has more than one non-default argument."
            )
            logger.error(message)
            raise Exception(message)

        if (stage_properties.n_not_defaults == 0) and (stage_properties.n_defaults == 0):
            message = (
                f"The stage {1+order} named {stage_properties.module}.{stage_properties.name} "
                "has no arguments at all."
            )
            logger.error(message)
            raise Exception(message)

        if (stage_properties.n_not_defaults == 0) and (stage_properties.n_defaults > 1):
            message = (
                f"The stage {1+order} named {stage_properties.module}.{stage_properties.name} "
                f"has only default arguments. The {self.__class__} are using the "
                f"first argument named '{stage_properties.default_args[0].name}'."
            )
            logger.warning(message)
