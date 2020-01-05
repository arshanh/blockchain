import argparse
import json
import itertools
from time import sleep
import csv

import redis

from util import make_batch, retry

class TransactionProducer:
    def __init__(self, source_file, batch_size):
        self.source_file = source_file
        self.batch_size = batch_size

    def produce(self):
        '''
        Produce a islice of batch_size lines
        islice is like slice but returns an iterator instead of actually
        creating a list. So this is equivalent to f[:self.batch_size]
        '''
        with open(self.source_file, 'r') as f:
            tsv = csv.reader(f, delimiter="\t")
            headers = next(tsv, None) # consume header row
            
            # Honestly I'm sorry how confusing the next 10 lines of code are

            def chunk(): 
                return make_batch(tsv, self.batch_size)

            def to_transaction(_batch):
                # This is pretty sneaky but it creates a dictionairy where
                # the keys are the headers and the values are the rows
                # Eg. {'block_id': '609023', 'hash': '36f3fcd1...
                # I use map because I need to apply it to each row in batch
                return map(dict, map(lambda row: zip(headers, row), _batch))

            # This means "keep calling chunk until it returns ()"
            # aka "keep making batches until you can't anymore"
            for batch in iter(chunk, ()):
                yield to_transaction(batch)

@retry(redis.exceptions.ConnectionError, tries=10, delay=1)
def rpush(r, name, values):
    '''Push retry on failure'''
    r.rpush(name, *values)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f',
                    help='File to read from')
    parser.add_argument('--cadence', '-c', type=int, default=5, 
            help='cadence to publish at (default = 5)')
    parser.add_argument('--batch_size', '-b',  type=int, default=1,
                        help='batch size to publish (default = 1)')
    parser.add_argument('--localhost', '-l', action='store_true', default=False,
                        help='batch size to publish (default = 1)')
    args = parser.parse_args()

    if args.localhost:
        r = redis.from_url("redis://@localhost:6379/0")
    else:
        r = redis.from_url("redis://redis:6379/0")

    producer = TransactionProducer(args.file, args.batch_size)
    for batch in producer.produce():
        # Push the whole batch at once
        values = list(map(json.dumps, batch))
        rpush(r, 'queue', values)
        sleep(args.cadence)

