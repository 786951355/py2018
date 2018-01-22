class Meta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.subclass.append(cls)


class Base(metaclass=Meta):
    subclass = []

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < len(self.subclass):
            val = self.subclass[self.count]
            self.count += 1
            return val
        else:
            raise StopIteration()


class A(Base):
    pass

class B(Base):
    pass

print(A in list(Base()))
for i in Base():
    print(i.__name__)