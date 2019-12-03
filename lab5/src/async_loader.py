from web3 import Web3
from threading import Thread
import config

WEB3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/b130f9d2fc724ec38061e3a2928f35e8"))
blocks = []
on_load_listener = None

threads_statuses = []
for i in range(0, config.threads):
    threads_statuses.append(False)


def check_all_are_closed():
    for thread_index in range(0, config.threads):
        if not threads_statuses[thread_index]:
            return False
    return True


def close_thread(num, thread):
    threads_statuses[num] = True
    if check_all_are_closed() and on_load_listener is not None:
        on_load_listener()


def get_blocks():
    return blocks


def subscribe_listener(callback):
    global on_load_listener
    on_load_listener = callback


class GetBlockThread(Thread):
    def __init__(self, thread_args):
        Thread.__init__(self)
        self.name = thread_args['name']
        self.start_block = thread_args['start_block']
        self.end_block = thread_args['end_block']
        self.index = thread_args['index']

    def run(self):
        print("%s started" % self.name)
        for block_num in range(self.start_block, self.end_block + 1):
            block = WEB3.eth.getBlock(block_num, True)
            mutable_block = dict(block)
            mutable_block['dict_txns'] = []
            for transaction in mutable_block['transactions']:
                for_mutate = dict(transaction)
                for_mutate['receipt'] = WEB3.eth.getTransactionReceipt(transaction.hash)
                mutable_block['dict_txns'].append(for_mutate)
            blocks.append(mutable_block)
            print(self.name + " " + str(block_num) + " @ " + str(len(blocks)) + "/" + str(
                config.end_number - config.start_number))
        print("%s finished. Loaded blocks [%d, %d]." % (self.name, self.start_block, self.end_block))
        close_thread(self.index, self)
