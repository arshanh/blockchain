import argparse
import json
from time import sleep

import redis

import util

blocknodes = util.getAddrsForHost('blockchain', 80)

@util.retry(redis.exceptions.ConnectionError, tries=10, delay=1)
def blpop(r, name):
    '''Do a blpop with retry'''
    return map(lambda x: str(x, 'utf8'), r.blpop(name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cadence', '-c', type=int, default=5,
            help='cadence to publish at (default = 5)')
    parser.add_argument('--localhost', '-l', action='store_true', default=False,
                        help='batch size to publish (default = 1)')
    args = parser.parse_args()

    if args.localhost:
        r = redis.from_url("redis://@localhost:6379/0")
    else:
        r = redis.from_url("redis://redis:6379/0")
    r = redis.from_url("redis://redis:6379/0")

    while True:
        name, transaction = blpop(r, 'queue')
        util.sendToNodes(nodes=blocknodes, 
                         method='POST',
                         path='transaction/new',
                         json=transaction)
        sleep(args.cadence)

