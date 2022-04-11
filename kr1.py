# Двухсвязный цикл не понял как, сделал обычный вроде как
class Long:
    def __init__(self, num):
        self.znak = -1 if int(num) < 0 else 1
        if num != '':
            self.item = num[0]
            num = num[1:]
            if num != '':
                self.next = Long(num)
            else:
                self.next = None
    def __str__(self):
        res = ''
        a = self
        while a.next != None:
            res += a.item
            a = a.next
        else:
            res += a.item
        return str(int(res) * self.znak)
    __repr__ = __str__
    def __add__(self, other):
        a = str(self)
        b = str(other)
        return str(int(a) * self.znak + int(b) * other.znak)
    def __sub__(self, other):
        a = str(self)
        b = str(other)
        return str(int(a) * self.znak - int(b) * other.znak)
    def __neg__(self):
        if self.znak == 1:
            self.znak = -1
        else:
            self.znak = 1
    def __eq__(self, other):
        a = str(self)
        b = str(other)
        if a == b:
            return True
        else:
            return False
a = Long('1221')
b = a
c = Long('2312311')
print(str(a) + str(a))
print(Long('123754646564'))
print(Long('12356546') + Long('123'))
print(Long('123') - Long('123654645564'))
print(a == b,a == c)
