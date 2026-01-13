x = {'key_1': 1, 'key_2': 2}
x['key_1']                    # get '1' by key 'key_1'
x['key_1'] = 5                # set '5' by key 'key_1'
del x['key_1']                # delete key 'key_1'

x = { 'key': 'value',
     1: 'value_2',
    ('a', 'b'): 'value_3'     }
# get by key
x['key']                # get 'value' by key str
x[1]                       # get 'value_2' by key int
x[('a', 'b')]           # get 'value_3' by key tuple

data = {'a': 1, 'b': 2, 'c': 3}
# keys and values
for k, v in data.items():
    print(k)
    print(v)

'123456789'[0]       # the first item
'123456789'[-1]      # the last item
'123456789'[:5]      # the first five items
'123456789'[-4:]     # the last four items
'123456789'[::2]     # every second item
'123456789'[::-1]    # reversed

for index, value in enumerate(res):
    print(index)
    print(value)

# for val1, val2, val3 in zip(data, data2, data3):
#     print(val1)
#     print(val2)

