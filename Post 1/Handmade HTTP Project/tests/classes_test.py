# Primary testing file
from pytest import raises
from hhttpp.classes import *

def test_MIME_type():
    MIMEType("text/html")
    MIMEType("image/png")
    
    # Error
    with raises(ValueError):
        MIMEType("text/html/css")
    with raises(ValueError):
        MIMEType("text html")
    with raises(ValueError):
        MIMEType("text/")
    with raises(ValueError):
        MIMEType("text/html/")
    
    # Test resource_path # TODO
    
    # Test generate_MIME_type_from_path() # TODO

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
    # Basic request
    r = Request("schulichignite.com", "/")
    assert r.hostname == "schulichignite.com"
    assert r.slug == "/"
    assert r.method == "GET"
    assert r.headers["accept"] == "*/*"
    
    # Basic request with lowercase method
    r = Request("schulichignite.com", "/", "get")
    assert r.hostname == "schulichignite.com"
    assert r.slug == "/"
    assert r.method == "GET"
    assert r.headers["accept"] == "*/*"
    
    # "Valid" request with URL
    r = Request("http://schulichignite.com", "/")
    assert r.hostname == "schulichignite.com"
    assert r.slug == "/"
    assert r.method == "GET"
    assert r.headers["accept"] == "*/*"

    r = Request("https://schulichignite.com", "/")
    assert r.hostname == "schulichignite.com"
    assert r.slug == "/"
    assert r.method == "GET"
    assert r.headers["accept"] == "*/*"
    
    # Error cases
    ## Full URL as hostname
    with raises(ValueError):
        Request("http://schulichignite.com/", "/")
    with raises(ValueError):
        Request("https://schulichignite.com/", "/")
    with raises(ValueError):
        Request("http://schulichignite.com/about", "/")
    with raises(ValueError):
        Request("https://schulichignite.com/about", "/")

    ## Methods
    with raises(ValueError):
        Request("schulichignite.com", "/", "gwet")
    with raises(ValueError):
        Request("schulichignite.com", "/", "xd")
    with raises(ValueError):
        Request("schulichignite.com", "/", "156574sdf")

def test_response():
    # Setup Status codes
    info = StatusCode(101,"Switching Protocols")
    valid = StatusCode(200, "Ok")
    redirect = StatusCode(301, "Moved Permenantly")
    client_error = StatusCode(404, "Not Found")
    server_error = StatusCode(500, "Internal Server Error")
    
    # Test basic usage and status codes
    r = Response(info)
    r1 = Response(valid)
    r2 = Response(redirect)
    r3 = Response(client_error)
    r4 = Response(server_error)
    
    assert type(r.headers) == dict
    assert type(r1.headers) == dict
    assert type(r2.headers) == dict
    assert type(r3.headers) == dict
    assert type(r4.headers) == dict
    
    assert r.headers["server"] == "HHTTPP"
    assert r1.headers["server"] == "HHTTPP"
    assert r2.headers["server"] == "HHTTPP"
    assert r3.headers["server"] == "HHTTPP"
    assert r4.headers["server"] == "HHTTPP"
    
    assert not r.is_error()
    assert not r1.is_error()
    assert not r2.is_error()
    assert r3.is_error()
    assert r4.is_error()
    
    # Test headers
    ## Make sure server is always set properly
    r = Response(info, headers={})
    r1 = Response(info, headers={"server":"Hue"})
    r2 = Response(info)
    with raises(AttributeError):
        Response(info, headers=[])
    with raises(AttributeError):
        Response(info, headers="server: hue")
    
    assert r.headers["server"] == "HHTTPP"
    assert r1.headers["server"] == "HHTTPP"
    assert r2.headers["server"] == "HHTTPP"
    
    # Test is_binary # TODO
    # Test content # TODO

def test_server():
    s = Server()
    
    # Test parse_request() # TODO
    
    ## Basic GET
    raw_request = "GET / HTTP/1.1\nHost: schulichignite.com"
    req = s.parse_request(raw_request)
    assert type(req) == Request # Will fail until a request object is returned
    assert req.method == "GET"
    assert req.headers["host"] == "schulichignite.com"
    assert req.headers["accept"] == "*/*" # TODO: Uncomment when feature is added
    
    ## GET with JSON content and headers
    raw_request = "GET / HTTP/1.1\nHost: schulichignite.com\nAccept: */*\n\n{{'name':'kieran','age':24}}"
    req = s.parse_request(raw_request)
    assert type(req) == Request # Will fail until a request object is returned
    assert req.method == "GET"
    assert req.headers["host"] == "schulichignite.com"
    assert req.headers["accept"] == "*/*" # TODO: Uncomment when feature is added
    # assert s.content == "{{'name':'kieran','age':24}}" # TODO: Uncomment when feature is added
    
    # TODO: Requires parsing
    ## PUT with content and headers
    # raw_request = "PUT / HTTP/1.1\nHost: schulichignite.com\nAccept: */*\n\n{{'name':'kieran','age':24}}"
    # req = s.parse_request(raw_request)
    # assert req.method == "PUT"
    # assert type(req) == Request # Will fail until a request object is returned
    # assert req.headers["host"] == "schulichignite.com"
    # assert req.headers["accept"] == "*/*" # TODO: Uncomment when feature is added
    # assert s.content == "{{'name':'kieran','age':24}}" # TODO: Uncomment when feature is added
    
    ## DELETE
    # raw_request = "DELETE / HTTP/1.1\nHost: schulichignite.com"
    # req = s.parse_request(raw_request)
    # assert req.method == "DELETE"
    # assert type(req) == Request # Will fail until a request object is returned
    # assert req.headers["host"] == "schulichignite.com"
    
    ## DELETE with content and headers
    # raw_request = "DELETE / HTTP/1.1\nHost: schulichignite.com\ncontent-type: application/json\n\n{{'id':'f78ae168-d643-4702-a2dd-7f58314dad96'}}"
    # req = s.parse_request(raw_request)
    # assert type(req) == Request # Will fail until a request object is returned
    # assert req.method == "DELETE"
    # assert req.headers["host"] == "schulichignite.com"
    # assert req.headers["content-type"] == "application/json"
    # assert s.content == "{{'id':'f78ae168-d643-4702-a2dd-7f58314dad96'}}"
    
    ## POST with content and headers
    # raw_request = "POST / HTTP/1.1\nHost: schulichignite.com\ncontent-type: application/json\n\n{{'id':'f78ae168-d643-4702-a2dd-7f58314dad96', 'name':'Kieran'}}"
    # req = s.parse_request(raw_request)
    # assert type(req) == Request # Will fail until a request object is returned
    # assert req.method == "POST"
    # assert req.headers["host"] == "schulichignite.com"
    # assert req.headers["content-type"] == "application/json"
    # assert s.content == "{{'id':'f78ae168-d643-4702-a2dd-7f58314dad96', 'name':'Kieran'}}"

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

    # Errors
    
    ## Incorrect header to be parsed # TODO
    