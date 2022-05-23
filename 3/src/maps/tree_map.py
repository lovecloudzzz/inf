from src.maps.base_map import BaseMap


class Knot:
    def __init__(self, key, data, right=None, left=None):
        self.data = data
        self.right = right
        self.left = left
        self.key = key

    def __eq__(self, other):
        if isinstance(other, Knot):
            if self.key == other.key:
                return True
            return False
        return False

    def __ne__(self, other):
        if isinstance(other, Knot):
            if self == other:
                return False
            return True
        return True

    def __lt__(self, other):
        if isinstance(other, Knot):
            if self.key < other.key:
                return True
            return False
        raise TypeError

    def __gt__(self, other):
        if isinstance(other, Knot):
            if self.key > other.key:
                return True
            return False
        raise TypeError


class TreeMap(BaseMap):
    def __init__(self, root=None):
        self.root = root
        self.length = 0

    def __setitem__(self, key, data):
        def inner_setitem(knot):
            if knot is None:
                return Knot(key, data)
            if key == knot.key:
                knot.data = data
            elif key < knot.key:
                knot.left = inner_setitem(knot.left)
            else:
                knot.right = inner_setitem(knot.right)

            return knot

        self.root = inner_setitem(self.root)
        self.length += 1

    def __getitem__(self, key):
        def inner_getitem(knot):
            if knot is None:
                raise KeyError("Элемента с таким ключем нет.")
            if key == knot.key:
                return knot
            if key > knot.key:
                return inner_getitem(knot.right)
            return inner_getitem(knot.left)

        return inner_getitem(self.root).data

    @staticmethod
    def find_min_node(knot):
        if knot.left is not None:
            return TreeMap.find_min_node(knot.left)
        return knot

    def __delitem__(self, key):
        def inner_delitem(knot, key):
            if knot is None:
                raise KeyError("Элемента с таким ключем нет.")
            if key < knot.key:
                knot.left = inner_delitem(knot.left, key)
                return knot
            if key > knot.key:
                knot.right = inner_delitem(knot.right, key)
                return knot
            if knot.left is None and knot.right is None:
                return None
            if knot.left is not None and knot.right is None:
                return knot.left
            if knot.left is None and knot.right is not None:
                return knot.right
            if knot.left is not None and knot.right is not None:
                min_node = TreeMap.find_min_node(knot.right)
                knot.key = min_node.key
                knot.data = min_node.data
                knot.right = inner_delitem(knot.right, min_node.key)
                return knot
            raise KeyError

        self.root = inner_delitem(self.root, key)
        self.length -= 1

    def __iter__(self):
        def iter_node(node):
            if node is not None:
                yield from iter_node(node.left)
                yield node.key, node.data
                yield from iter_node(node.right)

        yield from iter_node(self.root)

    def __len__(self):
        return self.length

    def __bool__(self):
        return len(self) != 0

    def clear(self):
        self.root = None


if __name__ == "__main__":
    tree = TreeMap()
    tree["asd"] = 6
    tree["zxc"] = 3
    tree["qwe"] = 5
    tree["sdsa"] = 2
    tree["qweqw"] = 8
    tree["xzcx"] = 10
    tree["gfdgfd"] = 7
    tree.write(r"D:\inf\3\src\test.txt")
    new_tree = TreeMap.read(r"D:\inf\3\src\test.txt")
    for key, value in new_tree:
        print((key, value))
