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
from typing import Literal

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

@dataclass
class Response:
    # Used to represent a HTTP Response
    status:StatusCode
    headers:dict = field(default_factory=lambda: dict())
    content: str = ""

@dataclass
class Server:
    # Used to represent an overall HTTP server
    proxy_directory:str
    
    def parse_request(self, input_text:str) -> Request:
        # TODO: Parse input text to generate Request object
        return Request("schulichignite.com", "/", "GET")
        
    def generate_response(self, request: Request) -> Response:
        # TODO: Locate resource, setup status code etc.
        headers = {"hostname": request.hostname}
        content = "<html><head><title>Hello World</title></head><body><h1>Hello World</h1></body></html>"
        return Response(StatusCode(200, "Ok"), headers, content)
    
    def send_request(self, request:Request) -> Response:
        # TODO: Network send the request and get a reponse
        return self.generate_response(request)

if __name__ == "__main__": # Code inside this statement will only run if the file is explicitly called and not just imported.
    ok = StatusCode(200, "OK")
    print(Request("schulichignite.com", "/"))
    print(Response(ok))