def BracketCombinations(num):
    if num <= 1:
        return 1

    res = 0
    for i in range(num):
        res += BracketCombinations(i) * BracketCombinations(num - i - 1)
    # code goes here
    return res


# keep this function call here
print
# BracketCombinations(raw_input())