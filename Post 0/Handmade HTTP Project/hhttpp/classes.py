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
from dataclasses import dataclass

@dataclass
class Request:
    # Used to represent a HTTP request
    ...
    
@dataclass
class Response:
    # Used to represent a HTTP Response
    ...

@dataclass
class StatusCode:
    # Used to represent a HTTP response status code
    ...

@dataclass
class Server:
    # Used to represent an overall HTTP server
    ...

if __name__ == "__main__": # Code inside this statement will only run if the file is explicitly called and not just imported.
    ...