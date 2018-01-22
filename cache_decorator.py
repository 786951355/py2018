# 实现一个计时缓存装饰器，当在指定的ttl时间内，访问的属性值都一样，超过后则重新计算。

from time import time,sleep


class Ttl_property(object):
    def __init__(self, ttl=None):
        self.ttl = ttl

    def __call__(self, func):
        self.func = func
        return self

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # 获取上次的值
        last = instance.__dict__.get('price', None)
        # 如果为空，刚计算并设置计算值和当前的时间戳，返回计算后的值
        if last is None:
            result = self.func(instance)
            instance.__dict__[self.name] = (result, time())
            return result

        # 如果当前时间 减去上次的时间戳大于ttl值，则重新计算并设置更新新的计算值和时间戳
        if time() - last[1] > self.ttl:
            result = self.func(instance)
            instance.__dict__[self.name] = (result, time())
            return result
        # 否则就返回上一次的计算值
        return last[0]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = (value, time())

    def __set_name__(self, owner, name):
        self.name = name


class Book(object):
    def __init__(self):
        self._price = 100.0

    @Ttl_property(ttl=2)
    def price(self):
        self._price = self._price * 0.8
        return self._price

    # price = Ttl_property(ttl=2)(price)
    # price() = Ttl_property(ttl=2)(price)()

if __name__ == '__main__':
    book = Book()
    print(book.price) # book.price.__get__(book, Book)
    sleep(3)
    print(book.price)
    sleep(2)
    print(book.price)
    sleep(1)
    print(book.price)
