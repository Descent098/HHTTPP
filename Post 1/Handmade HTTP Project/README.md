# Handmade HTTP Project (HHTTPP)

*Free range artisnal HTTP*

HHTTPP is an educational tool that is part of a series of blog posts being made to help teach about HTTP servers, and how to build one from scratch in python. The goals of the project are to build a package that:

1. Can be installed from pip (uploaded to pypi)
2. Can do all basic types of requests and responses (not every response code supported)
3. Have a simple CLI to make it easy to use

## Quick-start (TODO)

*Include how people can get started using your project in the shortest time possible*

### Installation

#### From source

1. Clone this repo: (put github/source code link here)
2. Run ```pip install .``` or ```sudo pip3 install .```in the root directory

#### From PyPi

1. Run ```pip install hhttpp```

#### Examples (TODO)

*Include an example or two of usage, or common use cases*

## Usage

HHTTPP has a CLI that you can use, the usage string can be found below:

```bash
hhttpp

Free range artisnal HTTP server

Usage: 
    hhttpp [-h] [-v] [-p PORT] [-f PROXY_FOLDER]

Options:
    -h, --help            Show this help message and exit
    -v, --version         Show program's version number and exit
    -p PORT, --port PORT  The port to start the server on 
    -f PROXY_FOLDER, --folder PROXY_FOLDER 
                          Lets you specify a folder to proxy instead of cwd
```

By default just running `hhttpp` in a folder will proxy the current folder (unless otherwise specified) you're in and find an available port to bind to if one is not specified.
