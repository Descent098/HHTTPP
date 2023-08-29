"""This module will house all of our classes used in other modules

This includes the classes for the basic HTTP protocol implementation

Classes
-------
This is where you mention any classes.

Request:
    Used to represent a HTTP request

Response:
    Used to represent a HTTP response

StatusCode:
    Used to represent a HTTP response status code

Server:
    Used to represent an overall HTTP server

References
----------
- Status codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- HTTP 1.1 Standard: https://datatracker.ietf.org/doc/html/rfc2616
- Python standard lib HTTP server: https://docs.python.org/3/library/http.server.html

Examples
--------
Setting up a basic http server on port 3883
```
from hhttpp import Server

Server(port=3883).start_server()
```
"""
from __future__ import annotations
import re
import os
import glob
import socket
from dataclasses import dataclass, field
from typing import Literal, List, Union, Dict

def parse_headers(input_text:str) -> Dict[str, str]:
    """Used to parse headers from HTTP request/responses

    Parameters
    ----------
    input_text : str
        The http request/response to parse as plaintext

    Returns
    -------
    Dict[str, str]
        A dictionary with a schema of {header: header_value}
    """
    regex = r"^(.*?):\s*(.*?)$"
    headers_match = re.findall(regex, input_text, re.MULTILINE)
    if headers_match:
        return {header_label.strip(): header_value.strip() for (header_label, header_value) in headers_match }
    else:
        return dict()

def parse_content(input_text:str) -> str:
    """Parse the content from HTTP content

    Parameters
    ----------
    input_text : str
        The http request/response to parse as plaintext

    Returns
    -------
    str
        The content of the HTTP request/response
    """
    regex = r".*\n\n(.+)"
    content_match = re.match(regex, input_text, re.MULTILINE | re.DOTALL)
    if not content_match:
        return ""
    else:
        return content_match.group(1).strip()

@dataclass
class Request:
    # Used to represent a HTTP request
    hostname: str
    slug: str
    method: Literal["GET","POST","PUT","DELETE"] = "GET"
    headers: dict = field(default_factory=lambda: dict())
    content:str = ""
    
    def __post_init__(self):
        # Make sure hostname isn't URL
        self.hostname = self.hostname.replace("http://","").replace("https://","") # Strip accidental protocols
        if "/" in self.hostname:
            raise ValueError(f"/ found in hostname {self.hostname} please confirm this isn't a URL")
        
        # Make sure method is valid and uppercase
        self.method = self.method.strip().upper()
        if not self.method in ["GET","POST","PUT","DELETE"]:
            raise ValueError(f"Provided method {self.method} is not valid")
        
        # Setup default headers
        self.headers["host"] = self.hostname
        self.headers["accept"] = self.headers.get("accept", "*/*")

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
class MIMEType:
    type:str
    resource_path: Union[None, str] = None
    is_binary:bool = False

    def __post_init__(self):
        # Incorrect manual type
        if not len(self.type.split("/")) == 2:
            raise ValueError(f"Incorrect MIME Type provided {self.type}")
        elif not self.type.split("/")[1]:
            raise ValueError(f"Incorrect MIME Type provided {self.type}")

        # Validate resource path exists if specified
        if self.resource_path:
            if not os.path.exists(self.resource_path):
                raise ValueError(f"Resource {self.resource_path} does not exist")

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
        if extension not in ("txt","html","css","js","md"):
            binary = True
        else:
            binary = False

        type_string = extension_to_types.get(extension, "application/octet-stream")
        return MIMEType(type_string, path, binary)

    def __repr__(self) -> str:
        return str(self.type)
    
    def __str__(self) -> str:
        return str(self.type)

@dataclass
class Response:
    # Used to represent a HTTP Response
    status:StatusCode
    type: MIMEType = field(default_factory=lambda:MIMEType("application/octet-stream"))
    headers:dict = field(default_factory=lambda: {"server":"HHTTPP"})
    content: str = ""
    is_binary: bool = False # Whether or not response should be binary instead of string

    def __post_init__(self):
        
        # Make sure server header is set properly
        self.headers.update({"Server": "HHTTPP","server": "HHTTPP", "Content-Type":self.type.type})
        # Make sure lowercase version of headers are available
        keys = list(self.headers.keys())
        for key in keys:
            self.headers[key.lower()] = self.headers[key]

    def is_error(self) -> bool:
        if self.status.value >=400:
            return True
        return False
    
    def __str__(self) -> str:
        # Convert headers to plaintext
        header_text = ""
        for header in self.headers:

            header_text += f"{header}: {self.headers[header]}\r"

        return f"""HTTP/1.1 {self.status.value} {self.status.description}\n{header_text}\n\n{self.content}"""
        
    

@dataclass
class Server:
    # Used to represent an overall HTTP server
    proxy_directory:str = "."
    error_on_4xx: bool = False # Should raise a python error on 4xx status codes
    error_on_5xx: bool = True # Should raise a python error on 5xx status codes
    log_limit: int = 500 # The number of logs to maintain
    logs: List[Union[Request, Response]] = field(default_factory=lambda:[])
    file_list: List[str] = field(default_factory=lambda:[]) # all the files in the proxy_directory
    urls: Dict[str,str] = field(default_factory=lambda:dict()) # A mapping of files to URL's
    host:str = "127.0.0.1"
    port:int = 9338
    socket: Union[None, socket.socket] = None
    
    def __post_init__(self):
        proxy_dir = os.path.abspath(self.proxy_directory)

        if not self.file_list:
            self.file_list = [
                f"{os.path.join(proxy_dir, file)}" 
                for file in glob.iglob(os.path.join(proxy_dir, '**',"*.*"), recursive=True)
            ]
        
        # Create URL list from file_list
        urls = dict()
        for file in self.file_list:
            base_url = file.replace(proxy_dir, "")
            file = os.path.relpath(file)
            
            # Set homepage
            if "index.html" in file:
                urls["/"] = file
                urls["/index.html"] = file
                continue
            
            # Add alias if HTML file
            if file.endswith(".html"):
                url = base_url.replace("\\","/").replace(r"//","/").replace(".html","")
                if not url.startswith("/"):
                    url = "/" + url
                urls[url] = file
            
            # Add path to file
            url = base_url.replace("\\","/").replace(r"//","/")
            if not url.startswith("/"):
                url = "/" + url
            urls[url] = file
        # Set instance url list to generated URL list
        self.urls = urls
    
    def parse_request(self, input_text:str) -> Request:
        """Takes in the plaintext HTTP request and returns a Request object

        Parameters
        ----------
        input_text : str
            The plaintext request

        Returns
        -------
        Request
            The class-based representation of the input_text request
        """
        # Parse first line of request
        regex = r"([A-z]{3,6}) (\/.*) HTTP\/(\d\.\d)"
        first_line = re.match(regex, input_text, re.MULTILINE)
        
        if not first_line:
            raise ValueError(f"Incorrectly formatted HTTP request recieved:\n\t {input_text}")
        method = first_line.group(1)
        slug = first_line.group(2)
        version = first_line.group(3)
        
        if not (first_line and slug and version):
            raise ValueError(f"Incorrectly formatted HTTP request recieved:\n\t {input_text}")
        
        
        # Parse headers
        headers = parse_headers(input_text)

        # Find content
        content = parse_content(input_text)
        
        # Combine info to create request object
        result = Request("schulichignite.com", slug, method, content = content, headers=headers)

        if len(self.logs) >= self.log_limit:
            print(f"Log limit {self.log_limit} or more, popping value")
            self.logs.pop()
        self.logs.append(result)
        return result
        
    def generate_response(self, request: Request) -> Response:
        """Takes in a Request object and generates a correct Response object for the request

        Parameters
        ----------
        request : Request
            The object with details about the request

        Returns
        -------
        Response
            The object with details about the response
        """
        headers = {"hostname": request.hostname,"server": "HHTTPP","Server": "HHTTPP"}
        
        # Pick status code & MIME Type
        try:
            if request.method in ["PUT", "POST", "DELETE"]:
                status_code = StatusCode(403, "Forbidden")
                mime = MIMEType("application/octet-stream")
            elif request.slug in self.urls:
                status_code = StatusCode(200, "Ok")
                mime = MIMEType.generate_MIME_type_from_path(self.urls[request.slug])
            else:
                status_code = StatusCode(404, "Not Found")
                mime = MIMEType("application/octet-stream")
        except:
            status_code = StatusCode(500, "Internal Server Error")
            mime = MIMEType("application/octet-stream")

        # Get content
        if mime.resource_path:
            if mime.is_binary:
                with open(mime.resource_path, "rb") as byte_file:
                    content = byte_file.read()
            else:
                with open(mime.resource_path, "r", encoding="UTF-8") as text_file:
                    content = text_file.read()
        else:
            content = ""
        
        # Create response object
        result = Response(status_code,type=mime, headers=headers, content=content, is_binary=mime.is_binary)
        
        # Error if server is setup that way
        if self.error_on_4xx and (399<status_code.value<500):
            raise ValueError(f"Recieved client error status code '{status_code}: {status_code.description}' on request: {request}")
            
        if self.error_on_5xx and (499<status_code.value<600):
            raise ValueError(f"Recieved server error status code {status_code} on request: {request}")

        if len(self.logs) >=self.log_limit:
            self.logs.pop()
        self.logs.append(result)
        return result
    
    def start_server(self):
        """Starts a server on the specified port"""
        print("Starting")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            ## SOL_Socket details can be found here https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html#Socket_002dLevel-Options
            ## This basically sets the internal options of the socket itself to say that SO_REUSEADDR is set to 1 or true which permits reuse of local addresses for this socket 
            ## If you enable this option, you can actually have two sockets with the same Internet port number; but the system won't allow you to use the two identically-named sockets in a way that would confuse the Internet.
            ## The reason for this option is that some higher-level Internet protocols, including FTP, require you to keep reusing the same port number.
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Set internal socket to allow SO_REUSEADDR
            s.bind((self.host, self.port)) # Bind the configured socket to the server (assign ip address and port number to the socket instance)
            s.listen(1) # Listen for incoming connections

            print(f'Listening on port {self.port} ...')
            
            s.settimeout(None)            
            while True:
                try:
                    # Wait for client connections
                    print("Accepting")
                    client_connection, _ = s.accept()
                    print("Accepted")

                    # Get the client request
                    print("Decoding")
                    raw_data = client_connection.recv(4096)
                    if raw_data:
                        print("Raw data found")
                        request = raw_data.decode()
                    else: 
                        print("No raw data found")
                        continue
                    print("Decoded")
                    print(request)
                    
                    req = self.parse_request(request)
                    resp = self.generate_response(req)
                    
                    if resp.is_binary:
                        client_connection.send(str(f"HTTP/1.1 {resp.status.value} {resp.status.description}\n").encode())
                        header_text = ""
                        print(f"{resp.headers=}")
                        for header in resp.headers:
                            header_text += f"{header}: {resp.headers[header]}\n"
                        client_connection.send(header_text.encode())
                        client_connection.send("\n".encode())
                        client_connection.sendall(resp.content)
                    else:
                        client_connection.sendall(str(resp).encode())
                    print("waiting to close")
                    # client_connection.close()
                    client_connection.shutdown(socket.SHUT_RDWR)
                    print("Closed")
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    break

if __name__ == "__main__": # Code inside this statement will only run if the file is explicitly called and not just imported.
    s = Server(f"tests{os.sep}example_site")
    s.start_server()
