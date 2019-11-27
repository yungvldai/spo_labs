from web3 import Web3
import sys
import math
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt


variant = 39
end_number = 8961400 - 10 * (variant - 2)
start_number = 8961400 - 10 * (variant - 1)
selection = []
toolbar_width = 50
BLOCK_DIV = (end_number - start_number) / toolbar_width
STATIC_REWARD = 3
map_fees_from_selection = []


def get_block_reward(_block):
    return STATIC_REWARD + gwei2eth(_block.gasUsed) + STATIC_REWARD * len(_block.uncles) / 32


def gwei2eth(gw):
    return gw / 1000000000


def get_block_fee(_block):
    return gwei2eth(_block.gasLimit)


def get_collection_by_key(map_, key):
    result = []
    for el in map_:
        result.append(el[key])
    return result


def blocks_loaded():
    goal = str(end_number - start_number)
    goal_len = len(goal)
    now = str(len(selection))
    now_len = len(now)
    now = ' ' * (goal_len - now_len) + now
    return now + '/' + goal


web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/b130f9d2fc724ec38061e3a2928f35e8"))
print('Blocks from', start_number, 'to', end_number)
sys.stdout.write("Downloading blocks... " + ("░" * toolbar_width) + ' ' + blocks_loaded())
for block_num in range(start_number, end_number):
    sys.stdout.write("\b" * (toolbar_width + len(blocks_loaded()) + 1))
    a = ("█" * int((block_num - start_number) / BLOCK_DIV + 1)) + \
        ('░' * (toolbar_width - int((block_num - start_number) / BLOCK_DIV + 1))) + ' ' + \
        blocks_loaded()
    sys.stdout.write(a)
    _block = web3.eth.getBlock(block_num, True)
    selection.append(_block)
sys.stdout.write("\b" * (toolbar_width + len(blocks_loaded()) + 1))
sys.stdout.write('[ \033[92mOK\033[0m ]\n')
print('Done. Downloaded', len(selection), 'blocks.')
for block in selection:
    map_fees_from_selection.append({
        'number': block.number,
        'reward': get_block_reward(block),
        'fee': get_block_fee(block),
        'percent': get_block_fee(block) / get_block_reward(block) * 100
    })
MX = np.mean(get_collection_by_key(map_fees_from_selection, 'fee'))
DX = np.var(get_collection_by_key(map_fees_from_selection, 'fee'))
ave_sqr_dev = math.sqrt(DX)
med = np.median(get_collection_by_key(map_fees_from_selection, 'fee'))
scatter = (
    np.amin(get_collection_by_key(map_fees_from_selection, 'fee')),
    np.amax(get_collection_by_key(map_fees_from_selection, 'fee'))
)
# stats
print('Summary:')
headers = ['MX', 'DX', 'ave sqr dev', 'med', 'scatter']
table = [[MX, DX, ave_sqr_dev, med, scatter]]
print(tabulate(table, headers, tablefmt="psql"))
# fee = f(block_number)
plt.plot(get_collection_by_key(map_fees_from_selection, 'number'), get_collection_by_key(map_fees_from_selection, 'fee'))
plt.xlabel('block number')
plt.ylabel('fee')
plt.xlim([start_number, end_number])
plt.show()
# reward % of fee = f(block_number)
plt.plot(get_collection_by_key(map_fees_from_selection, 'number'), get_collection_by_key(map_fees_from_selection, 'percent'))
plt.xlabel('block number')
plt.ylabel('reward % of fee')
plt.xlim([start_number, end_number])
plt.show()
