import os
import uuid
import re
import requests as req
import bs4 as bs
from src.maps.hash_map import HashMap


def wiki_parser(url: str, base_path):
    base_path += "\\base_path"

    if os.path.exists(base_path):
        print("Создание не удалось: папка base_path уже создана.\n", end="")
    else:
        os.mkdir(base_path)
        print("Папка base_path создана.\n", end="")

    flag = True
    dirlist = os.listdir(base_path)
    path = base_path
    for i in dirlist:
        with open(os.path.join(base_path, i, "url.txt"), "r", encoding="utf-8") as url_file:
            if url_file.read() == url:
                flag = False
                path += "\\" + i
                print("_____поиск url завершен, url уже был обработан_____\n", end="")
                break
    print("поиск url завершен, url еще не был обработан\n", end="")
    if flag:
        path += "\\" + uuid.uuid4().hex
        os.mkdir(path)
        with open(path + "\\url.txt", "w", encoding="utf-8") as url_file:
            url_file.write(url)
        text = req.request("GET", url).content
        with open(path + "\\content.bin", "wb") as content_file:
            content_file.write(text)

        print("_____url обработан_____\n", end="")
    with open(path + "\\content.bin", "rb") as content_file:
        soup = bs.BeautifulSoup(content_file, "lxml")
        hash_map = HashMap()
        for string in soup.stripped_strings:
            string = string.replace(".", "")
            string = string.replace(":", "")
            string = string.replace(";", "")
            string = string.replace(",", "")
            string = string.replace("«", "")
            string = string.replace("»", "")
            for word in string.split():
                if word[0] in r"""`-=_+[]{}\|/,.?'"№:;~1234567890!@#$%^&*()""":
                    continue
                try:
                    hash_map[word] += 1
                except KeyError:
                    hash_map[word] = 1
        hash_map.write(path + "\\words.txt")
        href_list = []
        for tag in soup.find_all(href=re.compile("^/wiki/")):
            href_list.append("https://ru.wikipedia.org" + tag["href"])
        print("выполнение закончено")
        return href_list


if __name__ == "__main__":
    rez = wiki_parser('https://ru.wikipedia.org/wiki/Наруто',
                      r'D:\inf\3\src')
    for j in rez:
        print(j)
