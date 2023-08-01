# Primary testing file
from pytest import raises
from hhttpp.classes import *

def test_status_codes():
    # Correct cases
    StatusCode(101,"Switching Protocols")
    StatusCode(200, "Ok")
    StatusCode(301, "Moved Permenantly")
    StatusCode(404, "Not Found")
    StatusCode(500, "Internal Server Error")

    # Edge cases
    StatusCode(100, "Continue")
    StatusCode(599, "")

    # Error case
    with raises(ValueError):
        StatusCode(-1, "Broken")
    with raises(ValueError):
        StatusCode(99, "Switcheroonied")
    with raises(ValueError):
        StatusCode(600, "Uknown Browser")


def test_request():
    ...

def test_response():
    ...

def test_server():
    s = Server()
    # Test log limit
    ## Default (500)
    for _ in range(600): 
        s.generate_response(s.parse_request(""))
    assert len(s.logs) == 500

    ## Custom (700)
    s = Server(log_limit = 700)
    for _ in range(900): 
        s.generate_response(s.parse_request(""))
    assert len(s.logs) == 700
