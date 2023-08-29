"""
HHTTPP is a very simple HTTP server built for a tutorial series: https://schulichignite.com/blog/hhttpp/series-introduction/

Notes
-----
- This project is NOT production ready, and likely never will be
- The functionality is based on the Python standard lib HTTP server: https://docs.python.org/3/library/http.server.html

Examples
--------
Setting up a basic http server on port 3883
```
from hhttpp import Server

Server(port=3883).start_server()
"""

__version__ = "0.1.0"
from .classes import Server as Server
