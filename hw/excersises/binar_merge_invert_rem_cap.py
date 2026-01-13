def binary_array_to_number(arr):
    binary_string = "".join(map(str, arr))
    return int(binary_string, 2)

def merge_arrays(arr1, arr2):
    return sorted(list(set(arr1 + arr2)))

def invert(lst):
    return [-x for x in lst]

def remove_url_anchor(url):
  return url.split('#')[0]

def capitals(word):
    t = []
    for r in range(0, len(word)):
        if word[r].isupper():
            t.append(r)
    return t

def capitals(word):
    return [i for (i, c) in enumerate(word) if c.isupper()]

def FirstReverse(str):
    return str[::-1]
# keep this function call here
# print FirstReverse(raw_input())