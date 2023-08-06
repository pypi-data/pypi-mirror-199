# backend.py

import datetime as dt
from functools import wraps
from pathlib import Path
from typing import (
    List, Any, Union, Dict, Optional, Tuple, Callable
)

import dill
import codecs

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import (
    RedirectResponse, Response, FileResponse,
    JSONResponse, HTMLResponse, StreamingResponse,
    PlainTextResponse, UJSONResponse, ORJSONResponse
)

from represent import Modifiers, BaseModel

__all__ = [
    "Responses",
    "BaseEndpoint",
    "DocsEndpoint",
    "GET",
    "POST",
    "DELETE",
    "UPLOAD",
    "HEAD",
    "PATCH",
    "PUT",
    "DOCS",
    "FAVICON",
    "METHODS",
    "EndpointRedirectResponse",
    "EndpointResponse",
    "EndpointFileResponse",
    "EndpointJSONResponse",
    "EndpointHTMLResponse",
    "EndpointStreamingResponse",
    "EndpointPlainTextResponse",
    "EndpointUJSONResponse",
    "EndpointORJSONResponse",
    "RESPONSES",
    "loads",
    "dumps",
    "decode",
    "encode",
    "Record",
    "DataContainer",
    "UnSerializableObjectError",
    "UnDeserializableObjectError"
]

DOCS = '/docs'
FAVICON = '/favicon.ico'

class Methods(BaseModel):
    """A class to contain the methods of the service."""

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    UPLOAD = "UPLOAD"
    HEAD = "HEAD"
    PATCH = "PATCH"
    PUT = "PUT"

    METHODS = (
        GET, POST, DELETE, UPLOAD,
        HEAD, PATCH, PUT
    )
# end Methods

GET = Methods.GET
POST = Methods.POST
DELETE = Methods.DELETE
UPLOAD = Methods.UPLOAD
HEAD = Methods.HEAD
PATCH = Methods.PATCH
PUT = Methods.PUT

METHODS = Methods.METHODS

class Responses(BaseModel):
    """A class to contain the response types."""

    EndpointRedirectResponse = RedirectResponse
    EndpointResponse = Response
    EndpointFileResponse = FileResponse
    EndpointJSONResponse = JSONResponse
    EndpointHTMLResponse = HTMLResponse
    EndpointStreamingResponse = StreamingResponse
    EndpointPlainTextResponse = PlainTextResponse
    EndpointUJSONResponse = UJSONResponse
    EndpointORJSONResponse = ORJSONResponse

    RESPONSES = (
        EndpointRedirectResponse, EndpointResponse,
        EndpointFileResponse, EndpointJSONResponse,
        EndpointHTMLResponse, EndpointStreamingResponse,
        EndpointPlainTextResponse, EndpointUJSONResponse,
        EndpointORJSONResponse
    )
# end Responses

EndpointRedirectResponse = Responses.EndpointRedirectResponse
EndpointResponse = Responses.EndpointResponse
EndpointFileResponse = Responses.EndpointFileResponse
EndpointJSONResponse = Responses.EndpointJSONResponse
EndpointHTMLResponse = Responses.EndpointHTMLResponse
EndpointStreamingResponse = Responses.EndpointStreamingResponse
EndpointPlainTextResponse = Responses.EndpointPlainTextResponse
EndpointUJSONResponse = Responses.EndpointUJSONResponse
EndpointORJSONResponse = Responses.EndpointORJSONResponse

RESPONSES = Responses.RESPONSES

Method = str
Methods = List[Method]

SerializationExceptions = (
    TypeError, ValueError, AttributeError,
    dill.PicklingError, dill.PickleError
)

class UnSerializableObjectError(ValueError):
    """A class to represent an exception."""

    def __init__(self, data: Optional[Any] = None) -> None:
        """
        Defines the class attributes.

        :param data: The commands to collect for the exception.
        """

        message = f" {repr(data)} of type {type(data)}" if data is not None else ""

        super().__init__(
            f"Couldn't serialize the object{message}. "
            f"Probably due to the object having weak "
            f"references or C-type pointers."
        )
    # end __init__
# end UnSerializableObjectError

class UnDeserializableObjectError(ValueError):
    """A class to represent an exception."""

    def __init__(self, data: Optional[Any] = None) -> None:
        """
        Defines the class attributes.

        :param data: The commands to collect for the exception.
        """

        message = f" {repr(data)} of type {type(data)}" if data is not None else ""

        super().__init__(
            f"Couldn't deserialize the object{message}. "
            f"Probably due to the object having weak "
            f"references or C-type pointers."
        )
    # end __init__
# end UnDeserializableObjectError

def dumps(data) -> bytes:
    """
    Encodes the object commands to a bytes string.

    :param data: The data to dump.

    :return: The bytes string commands.
    """

    try:
        return dill.dumps(data)

    except SerializationExceptions:
        raise UnSerializableObjectError(data)
    # end try
# end dumps

def loads(data: bytes) -> Any:
    """
    Decodes the object commands from a bytes string, to the object.

    :param data: The commands to load into a string.

    :return: The bytes string commands as object.
    """

    return dill.loads(data)
# end loads

def decode(data: str) -> bytes:
    """
    Decodes the object from a string.

    :param data: The commands to load into a string.

    :return: The object's commands.
    """

    return loads(codecs.decode(data.encode(), "base64"))
# end decode

def copy(data: Any) -> Any:
    """
    Copies the object.

    :param data: The data to load into a copy.

    :return: The object's copy.
    """

    return loads(dumps(data))
# end copy

def encode(data: Any) -> str:
    """
    Encodes the object into a string.

    :param data: The data to load into a copy.

    :return: An encoded string for the commands.
    """

    return codecs.encode(dumps(data), "base64").decode()
# end encode

class Record(BaseModel):
    """A class to represent a result object for commands and conditions calls."""

    def __init__(
            self, *,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict[str, Any]] = None,
            returns: Optional[Any] = None
    ) -> None:
        """
        Defines the class attributes.

        :param args: The positional arguments.
        :param kwargs: The keyword arguments.
        :param returns: The returned values.
        """

        if args is None:
            args = ()
        # end if

        if kwargs is None:
            kwargs = {}
        # end if

        self.args = args
        self.kwargs = kwargs
        self.returns = returns
    # end __init__

    def collect(
            self, *,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict[str, Any]] = None,
            returns: Optional[Any] = None
    ) -> None:
        """
        Defines the class attributes.

        :param args: The positional arguments.
        :param kwargs: The keyword arguments.
        :param returns: The returned values.
        """

        self.args = args
        self.kwargs.update(kwargs)
        self.returns = returns
    # end collect
# end Record

Requests = List[Record]

class DataContainer(BaseModel, dict):
    """A class to represent a data container."""

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Sets the attribute.

        :param key: The key to the attribute.
        :param value: The value of the attribute.
        """

        self[key] = value

        super().__setattr__(key, value)
    # end __setattr__

    def copy(self):
        """
        Copies the data of the model.

        :return: The copy of the model.
        """

        data: DataContainer = copy(self)

        return data
    # end copy

    def update(self, config: Dict[str, Any], **kwargs: Any) -> None:
        """
        Updates the object's data with the config.

        :param config: The config object.
        :param kwargs: Any keyword arguments.
        """

        if isinstance(config, type(self)):
            config = config.__dict__
        # end if

        if isinstance(config, dict):
            for key in self.__dict__.keys():
                if key in config:
                    setattr(self, key, config[key])
                # end if
            # end for
        # end if

        super().update(config, **kwargs)
    # end update
# end DataContainer

class BaseEndpoint(BaseModel):
    """
    A class to represent an endpoint.

    The BaseEndpoint is a command class that is the base of custom
    endpoint classes. Custom endpoint classes inherit from BaseEndpoint
    to add the command to execute when the endpoint is requested
    by a client, through the API of a service object.

    The endpoint method is implemented in child classes.

    All the returned values and parameters end endpoint collects through
    its lifetime are stored as AssistantResponse and Request objects at the internal
    record of the object.

    data attributes:

    - io:
        The configuration for saving and loading data and attributes
        that are none-mandatory to load and save. When given to False,
        The io object will have no keys inside it.

    - methods:
        A list of API endpoint methods that the endpoint should be
        able to operate with.

    - path:
        The path to the endpoint through the api.

    - root:
        The root of the path to the endpoint, when not ''.

    >>> from live_api.endpoint import BaseEndpoint, GET
    >>>
    >>> class MyEndpoint(BaseEndpoint):
    >>>     ...
    >>>
    >>>     def endpoint(self, *args: Any, **kwargs: Any) -> Any:
    >>>         ...
    >>>
    >>> endpoint = MyEndpoint(path="/<ENDPOINT PATH IN URL>", methods=[GET])
    # end AnswerEndpoint
    """

    modifiers = Modifiers(
        excluded=["service", "options", "record", "modifiers"]
    )

    def __init__(
            self,
            path: Union[str, Path],
            methods: Methods,
            service: Optional[object] = None,
            description: Optional[str] = None,
            root: Optional[str] = None,
            options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param path: The path to the endpoint.
        :param methods: The endpoint methods.
        :param description: The description of the object.
        :param root: The root to the path.
        :param options: Any keyword arguments.
        :param service: The service object.
        """

        if options is None:
            options = {}
        # end if

        if root is None:
            root = ""
        # end if

        self.record: Requests = []

        self.options = options

        self.path = str(path)
        self.root = root
        self.description = description

        self.methods = methods

        self.service = service
    # end __init__

    def __call__(self, *args: Any, **kwargs: Any) -> Dict[str, Union[int, Any]]:
        """
        Returns the function to command the command.

        :param name: The intent that activated the command.
        :param message: The message for the intent.

        :return: The function to command the command.
        """

        try:
            start = dt.datetime.now()

            result = self.process(self.wrap(self.endpoint)(*args, **kwargs))

            end = dt.datetime.now()

            return DataContainer(
                dict(response=result, time=(end - start).total_seconds())
            )

        except FileNotFoundError as e:
            raise RuntimeError(
                f"Could not complete the "
                f"execution of the request. {str(e)}"
            )
        # end try
    # end __call__

    def process(self, response: Any) -> Any:
        """
        Processes the response of the endpoint.

        :param response: The endpoint response to process.

        :return: The processed response.
        """

        dir(self)

        return response
    # end process

    def wrap(self, endpoint: Callable[..., Any]) -> Any:
        """
        Processes the response of the endpoint.

        :param endpoint: The endpoint to process.

        :return: The processed response.
        """

        dir(self)

        @wraps(endpoint)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
        Returns the response for the API endpoint.

        :param args: The positional arguments.
        :param kwargs: Any keyword argument.

        :return: The response from the function call.
        """

            return endpoint(*args, **kwargs)
        # end wrapper

        return wrapper
    # end process

    def set_root(self, root: str, /) -> None:
        """
        Sets the root path of the endpoint.

        :param root: The root path.
        """

        self.root = root
    # end set_root

    def get_root(self) -> str:
        """
        Gets the root path of the endpoint.

        :returns: The root path.
        """

        return self.root
    # end get_root

    def endpoint(self, *args: Any, **kwargs: Any) -> Any:
        """
        Returns the response for the API endpoint.

        :param args: The positional arguments.
        :param kwargs: Any keyword argument.

        :return: The response from the function call.
        """
    # end endpoint
# end BaseEndpoint

class DocsEndpoint(BaseEndpoint):
    """A class to represent an endpoint."""

    def __init__(
            self,
            methods: List[str],
            service: Optional[object] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            icon: Optional[str] = None,
            options: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param methods: The endpoint methods.
        :param description: The description of the object.
        :param icon: The icon file path.
        :param title: The endpoint title.
        :param options: Any keyword arguments.
        :param service: The service object.
        """

        self.title = title
        self.icon = icon

        BaseEndpoint.__init__(
            self, path=DOCS, methods=methods, service=service,
            description=description, options=options
        )
    # end __init__

    def endpoint(self) -> Any:
        """
        Returns the response for the API endpoint.

        :return: The response from the function call.
        """

        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=(
                self.title + " - Service Docs"
                if self.title is not None else "Service Docs"
            ),
            swagger_favicon_url=(
                self.icon if self.icon is not None else
                "https://fastapi.tiangolo.com/img/favicon.png"
            )
        )
    # end answer
# end DocsEndpoint