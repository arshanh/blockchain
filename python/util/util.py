import socket
from time import sleep
from functools import wraps
from itertools import chain, islice

import requests

def getAddrsForHost(host, port):
    # only interested in unique sockaddrs
    try:
        return {sockaddr[0] for family, socktype, proto, canonname, sockaddr
                in socket.getaddrinfo(host, port)}
    except socket.gaierror:
        print('Host lookup failed. This is expected if you are running outside of swarm/stack mode')

    return set()

def retry(ExceptionToCheck,
          tries=4,
          delay=1,
          logger=None,
          msg='',
          raiseIfFails=None,
          doIfFails=None):
    """ Retry calling the decorated function.

        retry is a factory funtion which creates a decorator named
        deco_retry. Deco_retry retries the function or method it
        decorates according to the configuration passed to retry
        as arguments.

        doIfFails allows for a function to be specified which will be
        executed after an attempt fails. This can be used to reset state
        before the next retry attempt/an exception is raised. This function
        is passed (*args, **kwargs) which will simply be the arguments
        passed to the decorated function (including self if it is a method)

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param logger: logger
    :type logger: logger instance
    :param msg: custom message to emit on retry
    :type msg: str
    :param raiseIfFails: exception to raise on failure
    :type Exception
    :param doIfFails: Code to run on failure (is passed the same arguments that are passed
                      to the decorated function or method)
    :type doIfFails: Callable that is passed (*args, **kwargs)
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            _tries = tries
            while _tries >= 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    if msg:
                        print(msg)
                    _msg = "%s, Retrying in %d seconds..." % (str(e), delay)
                    print(_msg)
                    if doIfFails:
                        doIfFails(*args, **kwargs)
                    sleep(delay)
                    _tries -= 1

            if raiseIfFails:
                raise raiseIfFails

            return f(*args, **kwargs)

        return f_retry

    return deco_retry

@retry(requests.exceptions.ConnectionError, tries=10, delay=1)
def request(method, path, json):
    if method == 'GET':
        r = requests.get(path, json=json)
    elif method == 'POST':
        r = requests.post(path, json=json)
    return r

def sendToNodes(nodes, method, path, json):
    for node in nodes:
        print(f'Sending messaged to {node}')
        r = request(method=method,
                    path=f'http://{node}/{path}',
                    json=json)

        if r.status_code != 200:
            print(f'Message error: path {path} to {node}, {r.status_code}')

def make_batch(iterable, n):
    '''Return an iterator of n elements from an iterable'''
    def prepend(value, iterator):
        "Prepend a single value in front of an iterator"
        return chain([value], iterator)

    # Emulate a peek by getting next and the putting it back
    try:
        peek = next(iterable)
    except StopIteration:
        # If iterator is exhausted return empty tuple
        return ()

    return islice(prepend(peek, iterable), n)
