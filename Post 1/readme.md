# Post 1; Setting up the HTTP protocol

For this post we will want to create the `Server`, `Request` and `Response` objects to house our info. This will help us model out the HTTP protocol, so we can do everything else we need to later.

## Terms

To start there are some terms we need to understand. Here are some of the basics:

|Term | Description | Example |
|Host | | |
|Proxy/alias | In our context we're using this to mean something that stands-in or is replaced by something else | For example HTTP is an alias for Hyper-text Transfer protocol. Essentially something can be thought of as equivalent as something else |


### Anatomy of a URL

Some of the most important terms we need to understand are what makes up a URL. A URL is what we type into a browser bar to get to a site (i.e. https://schulichignite.com). Here is a diagram breaking apart the different peices:

![](../images/Post%201/url-anatomy.png)

For those of you that can't read the image, this is the basic anatomy of a URL:

```
<protocol>://<domain/hostname/ip>:<port(optional)><slug/URI>
```

For example here are some URL's:

```
http://127.0.0.1:80/
http://localhost:8000/
http://thoth:32400/web/index
http://schulichignite.com/contact
http://example-site.co.uk/about-us
```

|Term | Description | Example |
|Protocol |  | `http://`, `https://`, `file://`|
|Slug/URI| | `/`, `/about`,`/blog/title`|


DOMAIN
PORT
HOSTNAME

## How HTTP Works

### Request <--> response

...

#### Headers

....

#### Status codes

...

#### MIME Types

...

## Let's look at existing sites

...

curl

httpie

browser dev tools

## How we're going to implement all this

...

## More resources

- [MDN HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [RFC-4229 Official Header Fields HTTP](https://datatracker.ietf.org/doc/html/rfc4229)
- [HTTPie (header visualizer)](https://httpie.io/)
- [CURL online headers](https://tools.keycdn.com/curl)
