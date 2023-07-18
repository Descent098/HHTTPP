


## What is regex? (TODO)

...

## Matching headers (TODO)

...

![](./../images/Post%202/regex-http-headers.png)

[Link to regex101](https://regex101.com/r/9IHYxj/1) 

You can do this with normal strings in python like this:

```python
response = """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Server: hhttpp

<!DOCTYPE HTML>
<html><body>
<h1>Hello, World!</h1>
</body></html>
"""

# Convert response to list of each line and skip the first line
response = response.split("\n")[1::]

headers = dict()

for line in response:
    if not line: # Empty line means content starts
        break # end loop
    line = line.split(":")
    headers[line[0]] = line[1]

print(headers) # {'Content-Type': ' text/html; charset=utf-8', 'Server': ' hhttpp'}
```

## Parsing Responses (TODO)

... 

Now that we can parse headers and requests, let's look at how we should interpret responses. This won't really matter for our features, but it will be handy for testing later.


### Check first line (TODO)

![](./../images/Post%202/regex-first-line-of-http-response.png)

[Link to regex101](https://regex101.com/r/707uYq/1) 

You can do this with normal strings in python like this:

```python
response = """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Server: hhttpp

<!DOCTYPE HTML>
<html><body>
<h1>Hello, World!</h1>
</body></html>
"""

# Convert response to list of each line
response = response.split("\n")

# Split the first line by spaces, and assign to variables
header_version, status_code, response_description = response[0].split(" ")

# Convert values to different types (this will throw errors if mistakes are made in the response)
header_version = float(header_version.split("/")[-1])
status_code = int(status_code)

print(f"{header_version=}, {status_code=}, {response_description=}")
```

### Find content (TODO)

With this one we also must set the `/s` flag, which will allow us to select multiple lines of content.

![](./../images/Post%202/regex-http-response-content.png)

[Link to regex101](https://regex101.com/r/YDue2M/1)

You can do this with normal strings in python like this:

```python
response = """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Server: hhttpp

<!DOCTYPE HTML>
<html><body>
<h1>Hello, World!</h1>
</body></html>
"""

# Convert response to list of each line and skip the first line
response = response.split("\n")[1::]

for index, line in enumerate(response):
    if not line: # Empty line means content starts
        # Recreate HTML joining each line with a newline at the end
        content = "\n".join(response[index+1::])
        break # end loop

print(content)
```