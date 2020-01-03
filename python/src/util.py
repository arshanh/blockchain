import socket

def getAddrsForHost(host, port):
    # only interested in unique sockaddrs
    try:
        return {sockaddr[0] for family, socktype, proto, canonname, sockaddr
                in socket.getaddrinfo(host, port)}
    except socket.gaierror:
        print('Host lookup failed. This is expected if you are running outside of swarm/stack mode')

    return set()

