# This file will house the code for the CLI (command line interface)
import os
import socket
from random import randint

from hhttpp import __version__
from hhttpp.classes import Server
from docopt import docopt # Used for argument parsing

usage = """hhttpp

Free range artisnal HTTP server

Usage: 
    hhttpp [-h] [-v] [-p PORT] [-f PROXY_FOLDER]

Options:
    -h, --help            Show this help message and exit
    -v, --version         Show program's version number and exit
    -p PORT, --port PORT  The port to start the server on 
    -f PROXY_FOLDER, --folder PROXY_FOLDER 
                          Lets you specify a folder to proxy instead of cwd
"""

def main():
    # This will be the primary entrypoint for the CLI
    args = docopt(usage, version=__version__) # Will be used in later post to do CLI parsing
    port = 8338
    folder = "."
    if args["--port"]:
        port = int(args["--port"])
    if args["--folder"]:
        if not os.path.exists(args["--folder"]):
            raise ValueError(f"Folder path {args['--folder']} does not exist")
        folder = args["--folder"]
    # Assign port
    valid_port = False
    while not valid_port:
        port_testing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination = ("127.0.0.1", port)
        result = port_testing_socket.connect_ex(destination)
        if not result:
            new_port = randint(1_000,10_000)
            print(f"Could not connect to port {port} trying other port {new_port}")
            port = new_port
            port_testing_socket.close()
        else:
            print(f"Valid port found: {port}")
            valid_port = True
            port_testing_socket.close()
    Server(folder, port=port).start_server()
