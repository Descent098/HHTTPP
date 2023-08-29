# Handmade HTTP Project (HHTTPP)

*Free range artisnal HTTP*

HHTTPP is an educational tool that is part of [a series of blog posts]() being made to help teach about HTTP servers, and how to build one from scratch in python. The goals of the project are to build a package that:

1. Can be installed from pip (uploaded to pypi)
2. Can do all basic types of requests and responses (not every response code supported)
3. Have a simple CLI to make it easy to use

## Quick-start

### Installation

#### From source

1. Clone this repo: (put github/source code link here)
2. Run ```pip install .``` or ```sudo pip3 install .```in the root directory
3. Confirm it is working by running `hhttpp -h` which should show you the text you see in [usage](#usage)

#### From PyPi

1. Run ```pip install hhttpp```
2. Confirm it is working by running `hhttpp -h` which should show you the text you see in [usage](#usage)

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

By default just running `hhttpp` in a folder will proxy the current folder (unless otherwise specified) you're in and find an available port to bind to if one is not specified (starting with 8338).

#### API Examples

The simplest way to use `hhttpp` as an API is to import the `Server` object, and let it run:

```python
from hhttpp import Server

Server().start_server()
```

The server object in this case will have all the logs and server state, so if you want to change behaviours, modify it's initialization. For example initializing while only allowing certain files to be visible to the server:

```python
from hhttpp import Server

s = Server(file_list = ["index.html", "/css/main.css"])

s.start_server()
```
