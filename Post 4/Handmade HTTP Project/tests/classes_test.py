# Primary testing file
from pytest import raises
from hhttpp.classes import *

EXAMPLE_SITE_PATH = os.path.join(os.path.dirname(__file__), "example_site")

def test_MIME_type():
    MIMEType("text/html")
    MIMEType("image/png")
    
    # Test resource_path
    MIMEType("text/html", os.path.join(EXAMPLE_SITE_PATH,"index.html"))
    
    # Test generate_MIME_type_from_path()
    assert MIMEType.generate_MIME_type_from_path(os.path.join(EXAMPLE_SITE_PATH,"index.html")).type == "text/html"
    assert MIMEType.generate_MIME_type_from_path(os.path.join(EXAMPLE_SITE_PATH,"pico.min.css")).type == "text/css"
    assert MIMEType.generate_MIME_type_from_path(os.path.join(EXAMPLE_SITE_PATH,"styles.css")).type == "text/css"
    assert MIMEType.generate_MIME_type_from_path(os.path.join(EXAMPLE_SITE_PATH,"js","themeSwitcher.js")).type == "text/javascript"
    
    # Error
    ## Incorect format for type
    with raises(ValueError):
        MIMEType("text/html/css")
    with raises(ValueError):
        MIMEType("text html")
    with raises(ValueError):
        MIMEType("text/")
    with raises(ValueError):
        MIMEType("text/html/")
    ## Nonexistant resource
    with raises(ValueError):
        MIMEType("text/html", "asdfghjkg.html")
    with raises(ValueError):
        MIMEType("text/html", "asdfghjkg")
    

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
    s = Server(proxy_directory=os.path.join(os.path.dirname(__file__), "example_site"))
    
    # Test filelist
    assert os.path.join(os.path.dirname(__file__), "example_site", "posts.html") in s.file_list
    assert os.path.join(os.path.dirname(__file__), "example_site", "styles.css") in s.file_list
    assert not os.path.join(os.path.dirname(__file__), "example_site", "LICENSE") in s.file_list
    assert os.path.join(os.path.dirname(__file__), "example_site", "js","particles.min.js") in s.file_list
    assert os.path.join(os.path.dirname(__file__), "example_site", "js","themeSwitcher.js") in s.file_list
    assert os.path.join(os.path.dirname(__file__), "example_site", "posts","pelicans-in-calgary.html") in s.file_list
    
    # Test parse_request()
    
    ## Basic GET
    raw_request = "GET / HTTP/1.1\nHost: schulichignite.com"
    
    ### Check request
    req = s.parse_request(raw_request)
    assert type(req) == Request # Will fail until a request object is returned
    assert req.method == "GET"
    assert req.headers["host"] == "schulichignite.com"
    assert req.headers["accept"] == "*/*"
    
    ### Check response
    resp = s.generate_response(req)
    assert type(resp) == Response
    assert type(resp.status) == StatusCode
    assert resp.status.value == 200
    assert type(resp.type) == MIMEType
    assert resp.type.type == "text/html"
    assert resp.is_binary == False
    
    
    ## Basic GET for non-html files
    raw_request = "GET /img/low-poly-ice-caps.jpg HTTP/1.1\nHost: schulichignite.com"
    
    ### Check request
    req = s.parse_request(raw_request)
    assert type(req) == Request # Will fail until a request object is returned
    assert req.method == "GET"
    assert req.headers["host"] == "schulichignite.com"
    assert req.headers["accept"] == "*/*"
    
    ### Check response
    resp = s.generate_response(req)
    assert type(resp) == Response
    assert type(resp.status) == StatusCode
    assert resp.status.value == 200
    assert type(resp.type) == MIMEType
    assert resp.type.type == "image/jpeg"
    assert resp.is_binary == True
    
    ## GET with JSON content and headers
    raw_request = "GET / HTTP/1.1\nHost: schulichignite.com\nAccept: */*\n\n{{'name':'kieran','age':24}}"
    
    ### Check request
    req = s.parse_request(raw_request)
    assert type(req) == Request # Will fail until a request object is returned
    assert req.method == "GET"
    assert req.headers["host"] == "schulichignite.com"
    assert req.headers["accept"] == "*/*"
    assert req.content == "{{'name':'kieran','age':24}}"
    
    ### Check response
    resp = s.generate_response(req)
    assert type(resp) == Response
    assert type(resp.status) == StatusCode
    assert resp.status.value == 200
    assert type(resp.type) == MIMEType
    assert resp.type.type == "text/html"
    assert resp.is_binary == False
    
    
    ## PUT with content and headers
    
    ### Check request
    raw_request = "PUT / HTTP/1.1\nHost: schulichignite.com\nAccept: */*\n\n{{'name':'kieran','age':24}}"
    req = s.parse_request(raw_request)
    assert req.method == "PUT"
    assert type(req) == Request # Will fail until a request object is returned
    assert req.headers["host"] == "schulichignite.com"
    assert req.headers["accept"] == "*/*"
    assert req.content == "{{'name':'kieran','age':24}}"
    
    ### Check response
    resp = s.generate_response(req)
    assert type(resp) == Response
    assert type(resp.status) == StatusCode
    assert resp.status.value == 403
    assert type(resp.type) == MIMEType
    assert resp.type.type == "application/octet-stream"
    assert resp.is_binary == False
    
    ## DELETE
    raw_request = "DELETE / HTTP/1.1\nHost: schulichignite.com"
    req = s.parse_request(raw_request)
    assert req.method == "DELETE"
    assert type(req) == Request # Will fail until a request object is returned
    assert req.headers["host"] == "schulichignite.com"
    
    ### Check response
    resp = s.generate_response(req)
    assert type(resp) == Response
    assert type(resp.status) == StatusCode
    assert resp.status.value == 403
    assert type(resp.type) == MIMEType
    assert resp.type.type == "application/octet-stream"
    assert resp.is_binary == False
    
    ## DELETE with content and headers
    raw_request = "DELETE / HTTP/1.1\nHost: schulichignite.com\ncontent-type: application/json\n\n{{'id':'f78ae168-d643-4702-a2dd-7f58314dad96'}}"
    req = s.parse_request(raw_request)
    assert type(req) == Request # Will fail until a request object is returned
    assert req.method == "DELETE"
    assert req.headers["host"] == "schulichignite.com"
    assert req.headers["content-type"] == "application/json"
    assert req.content == "{{'id':'f78ae168-d643-4702-a2dd-7f58314dad96'}}"
    
    ### Check response
    resp = s.generate_response(req)
    assert type(resp) == Response
    assert type(resp.status) == StatusCode
    assert resp.status.value == 403
    assert type(resp.type) == MIMEType
    assert resp.type.type == "application/octet-stream"
    assert resp.is_binary == False
    
    ## POST with content and headers
    raw_request = "POST / HTTP/1.1\nHost: schulichignite.com\ncontent-type: application/json\n\n{{'id':'f78ae168-d643-4702-a2dd-7f58314dad96', 'name':'Kieran'}}"
    
    ### Check request
    req = s.parse_request(raw_request)
    assert type(req) == Request # Will fail until a request object is returned
    assert req.method == "POST"
    assert req.headers["host"] == "schulichignite.com"
    assert req.headers["content-type"] == "application/json"
    assert req.content == "{{'id':'f78ae168-d643-4702-a2dd-7f58314dad96', 'name':'Kieran'}}"
    
    ### Check response
    resp = s.generate_response(req)
    assert type(resp) == Response
    assert type(resp.status) == StatusCode
    assert resp.status.value == 403
    assert type(resp.type) == MIMEType
    assert resp.type.type == "application/octet-stream"
    assert resp.is_binary == False

    # Test log limit
    ## Default (500)
    for _ in range(600): 
        s.generate_response(s.parse_request(raw_request))
    assert len(s.logs) == 500

    ## Custom (700)
    s = Server(log_limit = 700)
    for _ in range(900): 
        s.generate_response(s.parse_request(raw_request))
    assert len(s.logs) == 700

    # Errors
    
    ## Incorrect header to be parsed
    
    ### Incorrect method
    raw_request = "G2ET / HTTP/1.1\nHost: schulichignite.com"
    with raises(ValueError):
        s.parse_request(raw_request)
    raw_request = "GeET / HTTP/1.1\nHost: schulichignite.com"
    with raises(ValueError):
        s.parse_request(raw_request)
    raw_request = "REMOVEPLZ / HTTP/1.1\nHost: schulichignite.com"
    with raises(ValueError):
        s.parse_request(raw_request)

    ### Incorrect version
    raw_request = "GET / HTTP/9\nHost: schulichignite.com"
    with raises(ValueError):
        s.parse_request(raw_request)
    raw_request = "GET / 1.1\nHost: schulichignite.com"
    with raises(ValueError):
        s.parse_request(raw_request)
    raw_request = "GET / /\nHost: schulichignite.com"
    with raises(ValueError):
        s.parse_request(raw_request)
    
    ### Incorrect headers
    raw_request = "GET / HTTP/1.1\nHost; schulichignite.com"
    assert len(s.parse_request(raw_request).headers) == 2
    