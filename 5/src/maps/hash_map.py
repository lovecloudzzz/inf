from src.maps.base_map import BaseMap


class Node:
    def __init__(self, data=None, next_node=None):
        self._data = data
        self.next = next_node

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def compare_data(self, value) -> bool:
        return self.data == value


class List:
    def __init__(self):
        self.head = None
        self.length = 0
        self.node = None

    def get_last(self) -> Node:
        if self.length != 0:
            node = self.head
            while node.next is not None:
                node = node.next
            return node
        raise IndexError("Список пустой.")

    def add_node(self, data) -> None:
        self.length += 1
        if not isinstance(data, Node):
            data = Node(data)
        if self.head is None:
            self.head = data
        else:
            self.get_last().next = data

    def output(self) -> None:
        if self.head is None:
            print(None)
        else:
            node = self.head
            while node.next is not None:
                print(node.data)
                node = node.next
            print(node.data)

    def input(self) -> None:
        print("Чтобы закончить ввод напишите 'stop'.")
        condition = input()
        while True:
            if condition == "stop":
                answer = input("Закончить ввод? Дайте ответ 'yes' или 'no'.\n")
                if answer == "yes":
                    break
                answer = input("Добавить 'stop' в список? Дайте ответ 'yes' или 'no'.\n")
                if answer == "no":
                    condition = input()
            self.add_node(condition)
            self.length += 1
            condition = input()

    def del_head(self) -> None:
        self.head = self.head.next
        self.length -= 1

    def del_tail(self) -> None:
        if self.length == 1:
            self.head = None
            self.length -= 1
        elif self.length > 1:
            node = self.head
            while node.next.next is not None:
                node = node.next
            node.next = None
            self.length -= 1

    def remove(self, value, for_all=False) -> None:
        node = self.head
        if node.compare_data(value):
            self.del_head()
            if for_all is False:
                return
        while node.next.next is not None:
            if node.next.compare_data(value):
                node.next = node.next.next
                self.length -= 1
                if for_all is False:
                    return
            node = node.next
        if node.next.compare_data(value):
            node.next = node.next.next
            self.length -= 1

    def __iter__(self):
        self.node = self.head
        return self

    def __next__(self):
        node = self.node
        if node is None:
            raise StopIteration
        self.node = self.node.next
        return node.data

    def __getitem__(self, item):
        if self.length >= item:
            node = self.head
            i = 0
            while i < item:
                node = node.next
                i += 1
            return node.data
        raise IndexError

    def __setitem__(self, key, value):
        if self.length >= key:
            node = self.head
            i = 0
            while i < key:
                node = node.next
                i += 1
            node.data = value


class HashMap(BaseMap):
    def __init__(self, _size=10):
        self._inner_list = List()
        for _ in range(_size):
            self._inner_list.add_node(List())
        self._size = _size
        self._cnt = 0

    def get_size(self):
        return self._size

    @property
    def inner_list(self):
        return self._inner_list

    @property
    def cnt(self):
        return self._cnt

    def __getitem__(self, key):
        result = self._inner_list[hash(key) % self._size]
        if result.length == 0:
            raise KeyError("Ключ не найден.")
        for i in result:
            if i[0] == key:
                return i[1]
        raise KeyError("Ключ не найден.")

    def __setitem__(self, key, value):
        if self._inner_list[hash(key) % self._size].length == 0:
            self._cnt += 1
        flag = True
        for i in range(self._inner_list[hash(key) % self._size].length):
            if self._inner_list[hash(key) % self._size][i][0] == key:
                self._inner_list[hash(key) % self._size][i] = (key, value)
                flag = False
                break
        if flag:
            self._inner_list[hash(key) % self._size].add_node((key, value))
            if self._cnt >= 0.8 * self._size:
                self._size *= 2
                new_inner_list = List()
                for _ in range(self._size):
                    new_inner_list.add_node(List())
                for i in self._inner_list:
                    if i.length != 0:
                        for j in i:
                            new_inner_list[hash(j[0]) % self._size].add_node(j)
                self._inner_list = new_inner_list
                new_cnt = 0
                for i in self._inner_list:
                    if i.length != 0:
                        new_cnt += 1
                self._cnt = new_cnt

    def __delitem__(self, key):
        deleted = self[key]
        self._inner_list[hash(key) % self._size].remove((key, deleted))
        if self._inner_list[hash(key) % self._size].length == 0:
            self._cnt -= 1

    def __len__(self):
        return self.__iter__().length

    def __iter__(self):
        temp = List()
        for i in self._inner_list:
            for j in i:
                temp.add_node(j)
        return temp.__iter__()

    def __bool__(self):
        return len(self) != 0

    def clear(self):
        self._size = 10
        self._cnt = 0
        self._inner_list = List()
        for _ in range(10):
            self._inner_list.add_node(List())

    def set_from_list(self, lis):
        self.clear()
        for i in lis:
            self[i[0]] = i[1]
