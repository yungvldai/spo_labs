from async_loader import get_blocks
import operator
import config
import math
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt


def wei2gwei(w):
    return w / 1000000000


def gwei2eth(gw):
    return gw / 1000000000


def get_txns_fee(_block):
    summary = 0
    for transaction in _block['dict_txns']:
        summary += (gwei2eth(wei2gwei(transaction['gasPrice'])) * transaction['receipt']['gasUsed'])
    return summary


def get_block_reward(_block):
    return config.STATIC_REWARD + get_txns_fee(_block) + len(_block['uncles']) * 5 / 32


def get_collection_by_key(map_, key):
    result = []
    for el in map_:
        result.append(el[key])
    return result


def reorder(source):
    source.sort(key=operator.itemgetter('number'))


def analyse():
    map_from_blocks = []

    for block in get_blocks():
        map_from_blocks.append({
            'number': block['number'],
            'reward': get_block_reward(block),
            'fee': get_txns_fee(block),
            'percent': get_txns_fee(block) / get_block_reward(block) * 100
        })

    reorder(map_from_blocks)
    print(map_from_blocks)

    MX = np.mean(get_collection_by_key(map_from_blocks, 'fee'))
    DX = np.var(get_collection_by_key(map_from_blocks, 'fee'))
    ave_sqr_dev = math.sqrt(DX)
    med = np.median(get_collection_by_key(map_from_blocks, 'fee'))
    scatter = (
        np.amin(get_collection_by_key(map_from_blocks, 'fee')),
        np.amax(get_collection_by_key(map_from_blocks, 'fee'))
    )
    # stats
    print('Summary:')
    headers = ['MX', 'DX', 'ave sqr dev', 'med', 'scatter']
    table = [[MX, DX, ave_sqr_dev, med, scatter]]
    print(tabulate(table, headers, tablefmt="psql"))
    # fee = f(block_number)
    plt.plot(get_collection_by_key(map_from_blocks, 'number'), get_collection_by_key(map_from_blocks, 'fee'))
    plt.xlabel('block number')
    plt.ylabel('fee')
    plt.xlim([config.start_number, config.end_number])
    plt.show()
    # reward % of fee = f(block_number)
    plt.plot(get_collection_by_key(map_from_blocks, 'number'), get_collection_by_key(map_from_blocks, 'percent'))
    plt.xlabel('block number')
    plt.ylabel('reward % of fee')
    plt.xlim([config.start_number, config.end_number])
    plt.show()
