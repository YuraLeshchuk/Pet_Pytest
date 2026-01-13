def my_generator():
    print("gen activated")
    yield '1 msg'
    print('do smth 1')
    yield '2 msg'
    print('do snth 2')
    return 'Gen Return'
gen = my_generator()
next(gen)


def add_logging(func):
    def wrapper(*args, **kwargs):
        print('Do something before function call')
        res = func(*args, **kwargs)
        print('Do something after function call')
        return res
    return wrapper

@add_logging
def my_func(i):
    print(i)

my_func('Hi there')

sorted(users, key=lambda i: (i[1], i[0]))
[('John', 25), ('Mat', 30), ('Ann', 31)]

res = 'abc'.replace('ab', 'xy')   # 'xyc'

summary = lambda a, b: a + b
res = summary(5, 6)