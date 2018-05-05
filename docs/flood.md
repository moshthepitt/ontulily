# Flooding

A critical component of `ontulily` is the ability to do [HTTP flooding](https://en.wikipedia.org/wiki/HTTP_Flood).

The basic idea is to send seemingly legitimate GET, POST or other requests to a target in large volumes with the goal being to overwhelm the target.

Therefore we need to do this in a way that:

* ensures we can actually flood the target with a great number of requests
* ensures we make it very difficult for the target to tell whether our requests are legitimate users or not
* ensures that we hide ourselves, if possible
* ensures that we can scale this up easily

## Flooding the target

We will use asynchronous tools to increase the number of concurrent requests that we can make at any one time.  We will use:

* asyncio

## Confusing the target

We will attempt to make our requests look like legitimate requests.  Ideas on how to do this:

* fake user agents
* mimic a real browser e.g. Execute javascript, etc
* mimic a real user e.g. Click some links, etc

## Hiding ourselves

We will attempt to make our requests as untraceable as possible by using:

* fake user agents
* proxies
* tor

## Scale

Right now our scaling is concerned with efficiency.  All our code must be as efficient as possible and use as few resources (RAM, CPU) as we can get away with.

## Implementation

The actual HTTP requests will be made using:

### python requests

The ever popular [requests](http://docs.python-requests.org/en/master/) library is an obvious choice of a tool to use.  We use it because it is popular and familiar and implementing our flooding goals using it feels like it will be a nice and fun challenge.

However, we do acknowledge that it limits us severely when it comes to our goals of `Confusing the target`.
