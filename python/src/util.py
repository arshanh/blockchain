import socket

def getAddrsForHost(host, port):
    # only interested in unique sockaddrs
    return {sockaddr for family, socktype, proto, canonname, sockaddr
            in socket.getaddrinfo(host, port)}

