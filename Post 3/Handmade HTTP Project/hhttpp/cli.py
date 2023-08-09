# This file will house the code for the CLI (command line interface)
from hhttpp import __version__
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
    # args = docopt(usage, version=__version__) # Will be used in later post to do CLI parsing
    print("Not yet implemented")
