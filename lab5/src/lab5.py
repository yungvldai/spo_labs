from async_loader import GetBlockThread, subscribe_listener, get_blocks
import config
from data_analyser import analyse


def generate_threads():
    blocks_range = config.end_number - config.start_number
    range_per_thread = int(blocks_range / config.threads if blocks_range >= config.threads else blocks_range)
    threads_args = []
    for i in range(0, config.threads):
        threads_args.append({
            'start_block': config.start_number + (range_per_thread * i),
            'end_block': config.start_number + (range_per_thread * (i + 1) - 1),
            'name': 'Thread #' + str(i + 1),
            'index': i
        })
    return threads_args


print('Blocks from', config.start_number, 'to', config.end_number)
for thread_args in generate_threads():
    thread = GetBlockThread(thread_args)
    thread.start()


def on_load():
    analyse()


subscribe_listener(on_load)
