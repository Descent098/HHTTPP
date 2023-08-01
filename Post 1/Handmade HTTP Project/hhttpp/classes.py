"""This module will house all of our classes used in other modules

This includes the classes for the basic HTTP protocol implementation

Classes (TODO)
---------
This is where you mention any classes.

Request:
    Used to represent a HTTP request

Response:
    Used to represent a HTTP response

StatusCode:
    Used to represent a HTTP response status code

Server:
    Used to represent an overall HTTP server

Notes (TODO)
-----
Any other useful information.

References (TODO)
----------
If you are implementing complicated functionality that has associated references (papers, videos, presentations etc.)
    leave links to them here.

Examples (TODO)
--------
Any useful examples of basic usage of this module, make sure to enclose code in 3 backtics, this is
    interpreted by most modern IDE's as needing syntax highlighting which is quite useful. Here is an
    example:
    ```
    import this
    ```
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, List, Union

@dataclass
class Request:
    # Used to represent a HTTP request
    hostname: str
    slug: str
    method: Literal["GET","POST","PUT","DELETE"] = "GET"
    headers: dict = field(default_factory=lambda: dict())
    content:str = ""
    
    def __post_init__(self):
        self.method = self.method.strip().upper()
        if not self.method in ["GET","POST","PUT","DELETE"]:
            raise ValueError(f"Provided method {self.method} is not valid")
        ...

@dataclass
class StatusCode:
    # Used to represent a HTTP response status code
    value: int
    description: str

    def __post_init__(self):
        if self.value >599:
            raise ValueError("Cannot have a status code larger than 599")
        elif self.value <= 99:
            raise ValueError("Cannot have a status code less than 99")
    
    def is_error(self) -> bool:
        if self.value >=400:
            return True
        return False

@dataclass
class Response:
    # Used to represent a HTTP Response
    status:StatusCode
    headers:dict = field(default_factory=lambda: dict())
    content: str = ""
    is_binary: bool = False # Whether or not response should be binary instead of string

    def __post_init__(self):
        self.headers["Server"] = "HHTTPP"

    def is_error(self) -> bool:
        if self.status.value >=400:
            return True
        return False
    

@dataclass
class Server:
    # Used to represent an overall HTTP server
    proxy_directory:str = "."
    error_on_4xx: bool = False # Should raise a python error on 4xx status codes
    error_on_5xx: bool = True # Should raise a python error on 5xx status codes
    log_limit: int = 500 # The number of logs to maintain
    logs: List[Union[Request, Response]] = field(default_factory=lambda:[])
    
    def parse_request(self, input_text:str) -> Request:
        # TODO: Parse input text to generate Request object
        result = Request("schulichignite.com", "/", "GET")
        if len(self.logs) >=self.log_limit:
            print("500 or more, popping value")
            self.logs.pop()
        self.logs.append(result)
        return result
        
    def generate_response(self, request: Request) -> Response:
        # TODO: Locate resource, setup status code etc.
        headers = {"hostname": request.hostname}
        content = "<html><head><title>Hello World</title></head><body><h1>Hello World</h1></body></html>"
        
        # TODO: Pick status code
        status_code = StatusCode(200, "Ok")
        # status_code = StatusCode(404, "Not Found")
        # status_code = StatusCode(500, "Internal Server Error")

        # TODO: Create response object
        result = Response(status_code, headers, content)
        if self.error_on_4xx and (399<status_code.value<500):
            raise ValueError(f"Recieved client error status code '{status_code}: {status_code.description}' on request: {request}")
            
        if self.error_on_5xx and (499<status_code.value<600):
            raise ValueError(f"Recieved server error status code {status_code} on request: {request}")

        if len(self.logs) >=500:
            self.logs.pop()
        self.logs.append(result)
        return result
    
    def send_request(self, request:Request) -> Response:
        # TODO: Network send the request and get a reponse
        return self.generate_response(request)

@dataclass
class MIMEType:
    type:str
    resource_path: str


    def generate_MIME_type_from_path(path:str) -> MIMEType:
        # Takes in a file path and returns a Valid MIMEType for it
        extension = path.lower().split(".")[-1]
        if extension.endswith("gz"): # Tarballs
            extension = ".".join(path.split(".")[-2::])
        extension_to_types = {
            "txt": "text/plain",
            "html": "text/html",
            "css": "text/css",
            "js": "text/javascript",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "svg": "image/svg+xml",
            "mp4": "video/mp4",
            "mp3": "audio/mpeg"
        }

        type_string = extension_to_types.get(extension, "application/octet-stream")
        return MIMEType(type_string, path)

    def __repr__(self) -> str:
        return str(self.type)
    
    def __str__(self) -> str:
        return str(self.type)

if __name__ == "__main__": # Code inside this statement will only run if the file is explicitly called and not just imported.
    
    s = Server()
    for _ in range(600):
        s.generate_response(s.parse_request(""))
    
    print(len(s.logs))
    ok = StatusCode(200, "OK")
    # print(Request("schulichignite.com", "/"))
    # print(Response(ok))
    print(s)