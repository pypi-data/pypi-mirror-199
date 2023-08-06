"""@Author: Rayane AMROUCHE

Common classes.
"""
from __future__ import annotations

import json
import uuid
import inspect

try:
    from IPython.display import display  # type: ignore
except ImportError:
    pass

from typing import Any, Union, Optional, Tuple, Dict, List, Callable

from datachain.core.lazy import Lazy, LazyLoadingRequired
from datachain.core.sync import unwrap_async

session_uuid = uuid.uuid4()


class Pipe:
    """A class representing a transformation function."""

    def __init__(self, func: Callable, *args: Any, **kwds: Any) -> None:
        """Initialize a Pipe object.

        Args:
            func (Callable): The transformation function.
            *args (Any): Positional arguments to pass to the transformation function.
            **kwds (Any): Keyword arguments to pass to the transformation function.
        """
        self.func = func
        self.args = args
        self.kwds = kwds
        self.leaf = False
        self.name = "Default"

    def set_leaf(self) -> Any:
        """Set the Pipe object as a leaf node in a chain.

        Returns:
            Any: The current Pipe object.
        """
        self.leaf = True
        return self

    def rename(self, name: str) -> Any:
        """Rename the Pipe object.

        Args:
            name (str): The new name of the Pipe object.

        Returns:
            Any: The current Pipe object.
        """
        self.name = name
        return self


class DataCache:
    """A data storage class that can be accessed through attributes.

    Args:
        extractor (callable): Function to extract data.
        loader (callable): Function to load data.

    Attributes:
        __keys (list): List of keys.
    """

    def __init__(self, extractor, loader) -> None:
        self.extractor = extractor
        self.loader = loader
        self.__keys: List = []

    def keys(self):
        """Return a list of keys.

        Returns:
            list: List of keys.
        """
        return self.__keys

    def __getitem__(self, __name: str) -> Any:
        return self.extractor(__name)

    def __setitem__(self, __name: str, __value: Any) -> None:
        self.__keys.append(__name)
        self.loader(__name, __value)


class DataSource:
    """Data Source class."""

    def __init__(self, func: Any = None, **kwds) -> None:
        self.func = func
        self.params = kwds

    def preload(self, **kwds) -> Any:
        """Preload parameters for a given source.

        Args:
            **kwds: Arbitrary keyword arguments to feed parameters.

        Returns:
            Any: Returns the data source object.
        """
        self.params.update(kwds)
        return self

    def register(self, func: Callable) -> Any:
        """Register a function as the main source extractor.

        Args:
            func (Callable): The extractor function.

        Returns:
            Any: Returns the data source object.
        """
        self.func = func
        return self

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        params = self.params.copy()
        params.update(kwds)
        if self.func:
            return self.func(*args, **params)
        return None


def _transform(obj: Any, func: Callable, args: Tuple, kwds: Dict) -> Any:
    """Apply a given function to transform data using the given arguments.

    Args:
        obj (Any): Data to transform.
        func (Callable): Transforming function.
        args (Tuple): Arguments to pass to the transforming function.
        kwds (Dict): Keyword arguments to pass to the transforming function.

    Raises:
        ValueError: If the pipe target and a keyword argument have the same name.

    Returns:
        Any: Transformed data.
    """
    data = obj.data
    target = None

    # If the function is a string, get the method with that name from the data object
    if isinstance(func, str):
        # Put a value in target because data is in the method
        target = func
        func = getattr(data, func)
        # If the attribute is not callable then it is not a method so it is returned
        if not callable(func):
            # We actually should check if args and kwds are given and raise an error
            return func
    elif isinstance(func, tuple):
        func, target = func
        # If the pipe target name is the same as a keyword argument name, raise an error
        if target in kwds:
            msg = f"{target} is both the pipe target and a keyword argument"
            raise ValueError(msg)
        # Add the data to the keyword arguments
        kwds[target] = data

    # If the data is awaitable then await it
    if inspect.isawaitable(data):
        func = unwrap_async(func, target)

    # If no target is given then obj is the first argument
    if target is None:
        return func(data, *args, **kwds)
    # Otherwhise
    return func(*args, **kwds)


class Data(Lazy):
    """Data class."""

    def __init__(
        self,
        extractor: Optional[Callable] = None,
        params: Optional[Dict] = None,
        cached: bool = True,
    ) -> None:
        """Initializes a new Data instance.

        Args:
            extractor (Optional[Callable]): The data extraction function to use.
            params (Optional[Dict]): Parameters to pass to the extraction function.
            cached (bool): Whether the data should be cached or loaded on demand.
        """
        self.extractor = extractor
        self.params = {} if params is None else params
        self.cached = cached

    @Lazy.property
    def data(self) -> Any:
        """Returns the value of the `__data` attribute, loading it lazily if necessary.

        Raises:
            LazyLoadingRequired: If the `__data` attribute has not yet been loaded.

        Returns:
            Any: The value of the `__data` attribute.
        """
        if not self.cached:
            self.__load__("data")
        try:
            return self.__data  # type: ignore
        except AttributeError as err:
            raise LazyLoadingRequired from err

    def __load__(self, attr: Any) -> None:
        if attr == "data":
            if self.extractor is None:
                return None

            self.__data = (  # pylint: disable=attribute-defined-outside-init
                self.extractor(**self.params)
            )
            return self.__data
        return None

    def force_data(self, value: Any):
        """Force the data value of the instance.

        Args:
            value (Any): The new value to set for the data.
        """
        self.__data = value  # pylint: disable=attribute-defined-outside-init

    def __repr__(self) -> str:
        try:
            return repr(self.__data)
        except AttributeError:
            return "<Data not loaded>"

    def _ipython_display_(self):
        try:
            display(self.__data)
        except AttributeError:
            print("<Data not loaded>")

    def transform(self, func: Any, *args: Any, **kwds: Any) -> Data:
        """Transforms the current instance's data by applying a function to it and
        returns a new Data instance.

        Args:
            func (Any): The function to apply to the data.
            *args (Any): Additional positional arguments to pass to the function.
            **kwds (Any): Additional keyword arguments to pass to the function.

        Returns:
            Any: A new Data instance with the transformed data.
        """
        sign = inspect.signature(_transform).bind(self, func, args, kwds)
        sign.apply_defaults()
        params = sign.arguments
        return Data(_transform, params, self.cached)

    def chain(self, *pipes: Pipe) -> Union[Any, Tuple[Any, List[Any]]]:
        """Chains multiple transformation functions together and applies them
        sequentially to the data stored in the current instance of Data.

        Args:
            *pipes (Pipe): One or more Pipe objects representing transformation
            functions to be applied.

        Returns:
            Union[Any, Tuple[Any, List[Any]]]: A tuple containing the transformed data
            from the last pipe and a list of transformed data from any leaf pipes
            encountered in the chain. If no leaf pipes are present, only the transformed
            data from the last pipe is returned.
        """
        res = self
        leaves = []
        for pipe in pipes:
            transformed_data = res.transform(pipe.func, *pipe.args, **pipe.kwds)
            if pipe.leaf:
                leaves.append(transformed_data)
            else:
                res = transformed_data
        return (res, leaves) if leaves else res

    def decorate(
        self,
        decorator: Callable,
        func: Callable,
        *args: Any,
        **kwds: Any,
    ) -> Data:
        """Apply a decorator to a transforming function and call it on the current
        instance data.

        Args:
            decorator (Callable): The decorator function to apply.
            func (Callable): The transforming function.
            *args (Any): Positional arguments to pass to the transforming function.
            **kwds (Any): Keyword arguments to pass to the transforming function.

        Returns:
            Any: The original Data instance.
        """
        decorator(_transform(self, func, args, kwds))
        return self


class DataManager:
    """
    Data Manager class.

    Args:
        metadata (Dict): A dictionary of data metadata.
        cache (Optional): A data cache to store cached data. Defaults to None.

    """

    def __init__(self, metadata: Dict, cache: Any = None) -> None:
        """Initialize a Data Manager instance."""
        self.config = metadata
        if cache is None:
            cache = {}
        self.__cache: Any = cache
        self.__params: Dict = {}

    def __getitem__(self, key: str):
        self.__params = self.config[key]
        return self

    def __repr__(self) -> str:
        """Return the string representation of the Data Manager instance."""
        return json.dumps(self.config, indent=4)

    def __setup_extract(self, extractor: Callable, *args: Any, **kwds: Any) -> Any:
        """Set up the extraction process.

        Args:
            extractor (Callable): A function or class that extracts data from a source.
            *args (Any): Positional arguments for the extractor.
            **kwds (Any): Keyword arguments for the extractor.

        Returns:
            Any: The arguments to pass to the extractor function.
        """
        params = self.__params
        params.update(kwds)
        extractor_func = getattr(extractor, "func", extractor)
        sign = inspect.signature(extractor_func).bind(*args, **params)
        self.__params = {}
        sign.apply_defaults()
        return sign.arguments

    def extract(self, extractor: Callable, *args: Any, **kwds: Any) -> Any:
        """Extract data from a data source using the config and an appropriate
        extractor.

        Args:
            extractor (Callable): A function or class that extracts data from a source.
            *args (Any): Positional arguments for the extractor.
            **kwds (Any): Keyword arguments for the extractor.

        Returns:
            Any: The extracted data.
        """
        params = self.__setup_extract(extractor, *args, **kwds)
        cache_key = str(uuid.uuid5(session_uuid, str(params)))
        data = Data(extractor, params, True)
        if cache_key in self.__cache.keys():
            data.force_data(self.__cache[cache_key])
        else:
            self.__cache[cache_key] = data
        return data

    def uncached_extract(self, extractor: Callable, *args: Any, **kwds: Any) -> Data:
        """Extract data from a data source using the config and an appropriate
        extractor.

        Args:
            extractor (Callable): A function or class that extracts data from a source.
            *args (Any): Positional arguments for the extractor.
            **kwds (Any): Keyword arguments for the extractor.

        Returns:
            Any: The extracted data.
        """
        params = self.__setup_extract(extractor, *args, **kwds)
        data = Data(extractor, params, False)
        return data
