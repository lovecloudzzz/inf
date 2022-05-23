
import threading as thr
from parsers.wiki_parser import wiki_parser, timer_func


def run_wiki_parser(urls, base_path):
    result = []
    for i in urls:
        result.append(wiki_parser(i, base_path))
    return result


def run_multi(urls, base_path, deep):
    for i in urls:
        multi(i, base_path, deep)


@timer_func
def multi(url, base_path, deep=3, quantity_workers=3):
    beginning = wiki_parser(url, base_path)
    step = len(beginning) // 3 + 1

    if deep == 2:
        thrs = []
        for j in range(quantity_workers):
            thrs.append(thr.Thread(target=run_wiki_parser,
                                   args=(beginning[j * step:(j + 1) * step], base_path)))
        for i in thrs:
            i.start()
        for i in thrs:
            i.join()

    elif deep > 2:
        thrs1 = []
        for j in range(quantity_workers):
            thrs1.append(thr.Thread(target=run_multi,
                                    args=(beginning[j * step:(j + 1) * step], base_path, deep - 1)))
        for i in thrs1:
            i.start()
        for i in thrs1:
            i.join()


if __name__ == "__main__":
    multi('https://ru.wikipedia.org/wiki/Нартуо',
          r'D:\inf\4\src')
    print("done")
