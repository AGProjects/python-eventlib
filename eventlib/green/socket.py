__socket = __import__('socket')
for var in __socket.__all__:
    exec "%s = __socket.%s" % (var, var)
_fileobject = __socket._fileobject

from eventlib.api import get_hub
from eventlib.greenio import GreenSocket as socket
from eventlib.greenio import socketpair, fromfd

import warnings


def gethostbyname(name):
    if getattr(get_hub(), 'uses_twisted_reactor', None):
        globals()['gethostbyname'] = _gethostbyname_twisted
    else:
        globals()['gethostbyname'] = _gethostbyname_tpool
    return globals()['gethostbyname'](name)

def _gethostbyname_twisted(name):
    from twisted.internet import reactor
    from eventlib.twistedutil import block_on as _block_on
    return _block_on(reactor.resolve(name))

def _gethostbyname_tpool(name):
    from eventlib import tpool
    return tpool.execute(
        __socket.gethostbyname, name)

def getaddrinfo(*args, **kw):
    if getattr(get_hub(), 'uses_twisted_reactor', None):
        globals()['getaddrinfo'] = _getaddrinfo_twisted
    else:
        globals()['getaddrinfo'] = _getaddrinfo_tpool
    return globals()['getaddrinfo'](*args, **kw)

def _getaddrinfo_twisted(*args, **kw):
    from twisted.internet.threads import deferToThread
    from eventlib.twistedutil import block_on as _block_on
    return _block_on(deferToThread(__socket.getaddrinfo, *args, **kw))

def _getaddrinfo_tpool(*args, **kw):
    from eventlib import tpool
    return tpool.execute(
        __socket.getaddrinfo, *args, **kw)


# XXX there're few more blocking functions in socket
# XXX having a hub-independent way to access thread pool would be nice


_GLOBAL_DEFAULT_TIMEOUT = __socket._GLOBAL_DEFAULT_TIMEOUT

def create_connection(address, timeout=_GLOBAL_DEFAULT_TIMEOUT):
    """Connect to *address* and return the socket object.

    Convenience function.  Connect to *address* (a 2-tuple ``(host,
    port)``) and return the socket object.  Passing the optional
    *timeout* parameter will set the timeout on the socket instance
    before attempting to connect.  If no *timeout* is supplied, the
    global default timeout setting returned by :func:`getdefaulttimeout`
    is used.
    """

    msg = "getaddrinfo returns an empty list"
    host, port = address
    for res in getaddrinfo(host, port, 0, SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            sock = socket(af, socktype, proto)
            if timeout is not _GLOBAL_DEFAULT_TIMEOUT:
                sock.settimeout(timeout)
            sock.connect(sa)
            return sock

        except error, msg:
            if sock is not None:
                sock.close()

    raise error, msg


try:
    from eventlib.green import ssl as ssl_module
except ImportError:
    # no ssl support
    pass
else:
    # some constants the SSL module exports but not in __all__
    from eventlib.green.ssl import (RAND_add,
                                    RAND_egd,
                                    RAND_status,
                                    SSL_ERROR_ZERO_RETURN,
                                    SSL_ERROR_WANT_READ,
                                    SSL_ERROR_WANT_WRITE,
                                    SSL_ERROR_WANT_X509_LOOKUP,
                                    SSL_ERROR_SYSCALL,
                                    SSL_ERROR_SSL,
                                    SSL_ERROR_WANT_CONNECT,
                                    SSL_ERROR_EOF,
                                    SSL_ERROR_INVALID_ERROR_CODE)
    try:
        sslerror = __socket.sslerror
        __socket.ssl
        def ssl(sock, certificate=None, private_key=None):
            warnings.warn("socket.ssl() is deprecated. Use ssl.wrap_socket() instead.", DeprecationWarning, stacklevel=2)
            return ssl_module.sslwrap_simple(sock, private_key, certificate)
    except AttributeError:
        # if the real socket module doesn't have the ssl method or sslerror
        # exception, we don't emulate them
        pass

