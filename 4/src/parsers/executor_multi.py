
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from itertools import repeat
from parsers.wiki_parser import wiki_parser, timer_func


@timer_func
def multi(mode, url, base_path, max_workers=5, deep=3):
    beginning = wiki_parser(url, base_path)
    for _ in range(deep - 1):
        executor = mode(max_workers=max_workers)
        temp = []
        futures = [executor.submit(wiki_parser, url, path)
                   for url, path in zip(beginning, repeat(base_path))]
        for i in futures:
            temp += i.result()
        beginning = temp
        executor.shutdown()


if __name__ == "__main__":
    multi(ThreadPoolExecutor, 'https://ru.wikipedia.org/wiki/Наруто',
          r'D:\inf\4\src')
    multi(ProcessPoolExecutor, 'https://ru.wikipedia.org/wiki/Наруто',
          r'D:\inf\4\src')
