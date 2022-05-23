class Knot:
    def __init__(self, key, data, right=None, left=None, parent=None):
        self.data = data
        self.right = right
        self.left = left
        self.key = key
        self.parent = parent

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


class TreeMap:
    def __init__(self, head=None):
        self.head = head

    def __setitem__(self, key, data):
        if self.head is None:
            self.head = Knot(key, data)
        else:
            knot = self.head
            while True:
                if key == knot.key:
                    knot.data = data
                    return
                elif key > knot.key:
                    if knot.right is not None:
                        knot = knot.right
                    else:
                        knot.right = Knot(key, data, parent=knot)
                        return
                else:
                    if knot.left is not None:
                        knot = knot.left
                    else:
                        knot.left = Knot(key, data, parent=knot)
                        return

    def find(self, key):
        knot = self.head
        while knot.key != key:
            if key > knot.key:
                if knot.right is None:
                    return None
                else:
                    knot = knot.right
            else:
                if knot.left is None:
                    return None
                else:
                    knot = knot.left
        return knot

    def __getitem__(self, key):
        try:
            return self.find(key).data
        except (TypeError, AttributeError):
            raise KeyError("Элемент c таким ключом отсутствует")

    def find_knot_with_min_key(self, beginning=None):
        if beginning is None:
            knot = self.head
        else:
            knot = beginning
        while knot.left is not None:
            knot = knot.left
        return knot

    def __delitem__(self, key):
        knot = self.find(key)
        if knot is None:
            raise KeyError
        head = False
        if knot == self.head:
            head = True
        else:
            if knot > knot.parent:
                right = True
            else:
                right = False
        if (knot.right is None) and (knot.left is None):
            if head:
                self.head = None
            else:
                if right:
                    knot.parent.right = None
                else:
                    knot.parent.left = None
        elif knot.right is None:
            if head:
                self.head = knot.left
                self.head.parent = None
            else:
                if right:
                    knot.parent.right = knot.left
                else:
                    knot.parent.left = knot.left
                knot.left.parent = knot.parent
        elif knot.left is None:
            if head:
                self.head = knot.right
                self.head.parent = None
            else:
                if right:
                    knot.parent.right = knot.right
                else:
                    knot.parent.left = knot.right
                knot.right.parent = knot.parent
        else:
            min_right_knot = self.find_knot_with_min_key(knot.right)
            if head:
                self.head = min_right_knot
                if min_right_knot != knot.right:
                    min_right_knot.parent.left = min_right_knot.right
                    if min_right_knot.right is not None:
                        min_right_knot.right.parent = min_right_knot.parent
                    knot.right.parent = min_right_knot
                    min_right_knot.right = knot.right
                min_right_knot.parent = None
                min_right_knot.left = knot.left
                knot.left.parent = min_right_knot
            else:
                if right:
                    knot.parent.right = min_right_knot
                else:
                    knot.parent.left = min_right_knot
                if min_right_knot != knot.right:
                    min_right_knot.parent.left = min_right_knot.right
                    if min_right_knot.right is not None:
                        min_right_knot.right.parent = min_right_knot.parent
                    knot.right.parent = min_right_knot
                    min_right_knot.right = knot.right
                min_right_knot.left = knot.left
                min_right_knot.parent = knot.parent
                knot.left.parent = min_right_knot

if __name__ == "__main__":
    pass