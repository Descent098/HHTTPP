# Post 3; Implementing the networking portion

We have what we need to make HTTP requests and responses properly, so now let's look at adding networking so we can see the results in the browser. It's important to note we're only covering enough networking to understand **this project**, we're not covering everything there is to know about networking. So keep in mind there might be more steps and technologies in real server interactions!

Another warning is that for this set of code there is no easy way to test it without a ton of boilerplate code and concepts I would need to cover, and as such there are no additional tests for this post. If you want to know if your code works then open the URL to your server in a browser and see if it loads ¯\\\_(ツ)\_/¯.

## How connections work

In previous posts we looked at a bunch of terms:

- Ip's and ports
  - ipv4 vs ipv6
  - Localhost
- hostname/DNS
- etc.

For simplicity we will only care about a few terms:

- Ip's
- Ports
- Protocols
- Berkley Sockets

When we want to connect to another computer we can think about it the same way we would when we're sending a letter, or even an email. There's a few things we need:

- A message
- A place to deliver the message
- A place to get a response
- A procedure to deliver the message

Here is what the equivalent mail to http values would look like:

|Role|HTTP|Mail|
|----|----|----|
|A message| HTTP request | A letter or package | 
|A place to deliver the message| The **client** IP address & port | An address | 
|A place to get a response| The **host** IP address & port | An address | 
|A procedure to deliver the message| HTTP over berkley sockets | The mail company rules through a post delivery person | 

So for the postal service when you send a letter they will:

0. Drop off the letter at a post office to be sent
1. Lookup the address on the letter/package
2. Find the corresponding physical location on the letter/package
3. Drive to the location following rules and procedures of the company, and drop off the letter/package

For retrieving a site they will:

0. If they used a domain they need to lookup the IP address associated with the domain
1. Start a connection with the IP address of the host through a berkley socket
2. Send an HTTP request through the socket
3. Wait for a response to be sent back from the server through the socket


## Berkley Sockets (TODO)

\**We will cover the basics, but if you want a breakdown of sockets in detail (in python and in the underlying C calls python is making) check out [this gist](https://gist.github.com/Descent098/783f68e1e3943e8796a3aaf8a14f8013).*

We've now looked at how berkley/bsd sockets are used, but let's get into specifics. Our steps were:

0. If they used a domain they need to lookup the IP address associated with the domain
1. Start a connection with the IP address of the host through a berkley socket
2. Send an HTTP request through the socket
3. Wait for a response to be sent back from the server through the socket

\**Keep in mind when you hear "sockets" in webdev it can mean berkley sockets, **or** [websockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)*

### So what actually are berkley sockets?

Berkley/bsd Sockets are a fancy API provided by your operating system that allows you to talk to your NIC (network interface card). Your NIC is what sends the 1s and 0s over the internet, and berkley sockets are an API built on top of the hardware to make it easier to work with lower-level networking. They basically allow you to talk back and forth between you and your NIC in human-friendly ways. Under the hood each persons NIC running the code might be doing different things when you dig into the details, but berkley sockets are a universal standard for interfacing with NICs for basically any brand/card in your PC.

In our analogy from before Berkley Sockets would be the mail person delivering the mail. It's job is to simply connect to a computer and send/recieve data. It has no rules about what protocols you talk using, or anything like that. This means they can be used for more than HTTP (like [telnet](https://en.wikipedia.org/wiki/Telnet) or [sftp](https://www.ssh.com/academy/ssh/sftp-ssh-file-transfer-protocol)).

## How to use them

There are 3 basic steps (and some sub-steps within them) to using berkley sockets as a server/host in your code:

1. Setup/config: Tell the socket what you intend to do with it, so it can set itself up for what you need. This includes what type of IP address ([IPV4](https://bluecatnetworks.com/glossary/what-is-ipv4/#:~:text=Now%2C%20exactly%20what%20is%20IPv4%3F) or [IPV6](https://en.wikipedia.org/wiki/IPv6_address#:~:text=An%20IPv6%20address%20is%20represented,the%20representation%20of%20IPv6%20addresses.)), [socket type/kind](https://stackoverflow.com/questions/5815675/what-is-sock-dgram-and-sock-stream), and any [options](https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html#Socket_002dLevel-Options) you want to use.
2. Binding and listening: When you tell the socket what IP address and port to bind to, as well as when to start listening for connections
   1. Call `.bind()` with the host and port, this "reserves" the port so other sockets can't use them on the same IP address
   2. Call `.listen()` to tell the socket to start listening for potential connections
   3. Call `.accept()` to say you're fine with the incomming connection (any validation steps for only allowing certain devices would happen between `.listen()` and `.accept()`)
3. Send/recv: This is when data is exchanged between the client and host

### How this works in python (TODO)

In python you create a socket with a [context manager](https://www.learndatasci.com/solutions/python-context-managers/). What this does is basically for the duration of the program a socket will be opened, but you must make sure to close the socket or else that port is constantly being used and never released. A context manager makes sure that a socket is always closed once you're done with it.

Here is what steps 1 and 2 would look like in python:

```python
import socket

ip = "127.0.0.1" # The IP address to use, this one specifies internal
port = 8338 # The port to bind to

# Step 1
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Set internal socket to allow SO_REUSEADDR (1 means true)

    # Step 2
    s.bind((ip, port)) # Bind the configured socket to the server (assign ip address and port number to the socket instance)
    s.listen(1) # Listen for incoming connections
    client_connection, client_address = s.accept() # Accept connections and return details about them
```

There's a few constants we're using here so let's explain what they do

| Constant name | Purpose | 
|---------------|---------|
| [socket.AF_INET](https://docs.python.org/3/library/socket.html#socket.AF_INET) | This specifies you want to use an [ipv4](https://www.juniper.net/documentation/us/en/software/junos/interfaces-security-devices/topics/topic-map/security-interface-ipv4-ipv6-protocol.html#:~:text=Length%20Subnet%20Masks-,IPv4%20Classful%20Addressing,-To%20provide%20flexibility) ip address instead of an [ipv6](https://en.wikipedia.org/wiki/IPv6_address#:~:text=An%20Internet%20Protocol%20Version%206,the%20destination%20of%20each%20packet.) one |
| [socket.SOCK_STREAM](https://docs.python.org/3/library/socket.html#socket.SOCK_STREAM) | This tells the socket to use [TCP](https://www.fortinet.com/resources/cyberglossary/tcp-ip#:~:text=Transmission%20Control%20Protocol%20(TCP)%20is,data%20and%20messages%20over%20networks.) instead of [UDP](https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/#:~:text=The%20User%20Datagram%20Protocol%2C%20or,connection%20before%20data%20is%20transferred.), this distinction is complicated, so don't worry about it for now, you will basically always use TCP unless you're in certain performance constrained situations but [here is a quick breakdown](https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/#:~:text=TCP%20vs.%20UDP,-UDP%20is%20faster)| 
| [socket.SOL_SOCKET](https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html#Socket_002dLevel-Options) | Allows you to set options for a socket (like SO_REUSEADDR below)| 
| [socket.SO_REUSEADDR](https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html#index-SO_005fREUSEADDR) | Lets you reuse a set port if you need to. This just helps avoid weird bugs when testing locally that can occur |

### Common gotchas (TODO)

...

- Mostly everything is just a bunch of strings. So all of the below are possible problems:
  - Not doing data validation
  - Using a different [encoding]()
- send/recv also has binary data to deal with
  - explain what it is etc.


## Resources (TODO)

- [Socket module](https://docs.python.org/3/library/socket.html)
- [Official python socket howto](https://docs.python.org/3/howto/sockets.html)
- [Another intro to sockets](https://realpython.com/python-sockets/)
- [Berkley Socket's (video)](https://www.youtube.com/watch?v=onQTzTJ5sqU)
- [Python Socket Programming Tutorial (video)](https://www.youtube.com/watch?v=3QiPPX-KeSc)
- [Socket Programming in Python(Simplified) - in 7 minutes! (Video, covers client and server)](https://www.youtube.com/watch?v=JNzfG7XMYSg)
