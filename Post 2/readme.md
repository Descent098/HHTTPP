# Post 2; Create request and response objects from text

Now that we have our basic HTTP structure we need a way to read **actual** http requests/responses. Currently we have hardcoded everything, so today we will focus on creating everything we need for steps 2-4:

1. Recieve plaintext request
2. **Parse the plaintext into a `Request` object**
3. **Process the `Request` object and generate a `Reponse` object**
4. **Generate a plaintext response from the `Response` object**

## Terms & Concepts (TODO)

To start there are some terms we need to understand. Here's what we need to know about, and what we're going to cover in more detail later.

|Term | Description | Example |
|-----|-------------|---------|
| Parser | A piece of code that can read data in one format (usually plain text) and parse them into another format (object, different text format etc.) | A fast [HTTP parser](https://github.com/MagicStack/httptools) in python (also anything that works with HTTP will have some sort of parser) |
| Data Sanitization | Removing parts of an input that might cause undesirable behaviour | Cleaning text that comes in from a comment that could be interpreted as HTML so it doesn't render as HTML when people visit the comments later | 
| ... | ... | ... |

## What is regex?

Regex is a pattern matching language. It let's you define patterns of text that it will then return the matches for. So if you wanted to extract all the numbers from some text you can define a regex pattern. The patterns are called regex expressions, and are just plain text. For example all of the below are regex patterns:

```python
"[A-z]" # Match any single uppercase or lowercase character
"[a-z]" # Match any single lowercase character
"[aef]" # Match any single a, e or f
"\d" # Match any single digit (0-9)
```

Regex will usually parsed in python using the [re](https://docs.python.org/3/library/re.html) module (but we will also use [glob](https://docs.python.org/3/library/glob.html)), and will create `Match` objects. These `Match` objects contain each match for the pattern you define. There are lots of different ways to use regex, but we will use 2 ways, globbing and capture groups.

Capture groups is essentially the idea that we define a set of "groups", and for each `Match` in the pattern there will be "groups" of text matched. For example we might read the first line of a HTTP request we will want different groups for the method, slug and http version. To create groups you put a sub-expression into parenthesis. For example to capture a single letter, and a single digit into separate groups you do `([A-z])(\d)`. This will find any letter then digit, so for example with the string `"a1,b5,dt,r7"` would have 3 matches `a1, b5 and r7` each with 2 groups: 

- `a1`: Group 1 is `a`, group 2 is `1`
- `b5`: Group 1 is `b`, group 2 is `5`
- `r7`: Group 1 is `r`, group 2 is `7`

We will cover globbing in the next section, it is a bit easier to do and is used to get a list of files.There is not enough time to cover regex fully, but for each set of regex we will use there will be an image explaining each portion of the expression. You can check the [more resources](#more-resources) section for a general introduction to regex thatgoes into more details.

## Getting file lists (TODO)

There are two more attributes we have added to the `Server` class, `file_list` and `urls`. `file_list` is a list of all the paths of files in `Server.proxy_directory`, and URL's are going to be the URL's that correspond to each file. The code for this can be found in `Server.__post_init__()`, and in this section we will describe how we generate `Server.file_list`.

We are going to use the [glob](https://docs.python.org/3/library/glob.html) module to get a list of files. This lets us define patterns similar to regex, but it's specifically built for files. Since this is less applicable the basics are that `*` means replace with anything. So in our case to get every single file in a folder we can do `glob.glob("*.*")`. This is great, but what about if we have subdirectories (i.e. `/js/file.js`)? Now we need a fancier pattern. 

The easiest way to do this is following the pattern `<folder>/**/*`, this says all files in all folders. We then pass the recursive flag and it will find everything `glob.glob("<folder>/**/*, recursive=True)`. For performance reasons we are going to use `glob.iglob()`, and we will replace `<folder>` with the absolute path to the proxy_directory we set on our server object.

Putting it all together here is the basic idea:

```python
class Server:
    ... # More code

    def __post_init__(self):
        proxy_dir = os.path.abspath(self.proxy_directory) # Making path absolute makes this easier

        for file in glob.iglob(os.path.join(proxy_dir, '**',"*.*"), recursive=True):
            self.file_list.append(os.path.join(proxy_dir, file))
```

In the actual code I did the second part with a list comprehension:

```python
class Server:
    ... # More code

    def __post_init__(self):
        proxy_dir = os.path.abspath(self.proxy_directory)

        self.file_list = [
        f"{os.path.join(proxy_dir, file)}" 
        for file in glob.iglob(os.path.join(proxy_dir, '**',"*.*"), recursive=True)
        ]
```

### Creating URL's from file list (TODO)

This is important because it will allow us to do things like aliased URL's. So for example if we don't do this people could only access a file called `about.html` at `<domain>/about.html`. But we also want to do `<domain>/about`, so we need a dictionary mapping of these URL's to the files to be able to find it. 

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

## Parsing Requests (TODO)

...


### Parsing first line of request (TODO)

`(.*){3,4} (\/.*) HTTP\/(\d\.\d)`


## Parsing Responses (TODO)

... 

Now that we can parse headers and requests, let's look at how we should interpret responses. This won't really matter for our features, but it will be handy for testing later.


### Check first line of response (TODO)

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


## More resources

- [Interactive introduction to regex](https://regexone.com/lesson/introduction_abcs)
- [regex 101; Great tool for writing regex](https://regex101.com/)

