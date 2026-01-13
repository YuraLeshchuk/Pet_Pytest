def FirstFactorial(num):
    result = 1
    for i in range(1, num + 1):
        result *= i
    return result


# keep this function call here
# print FirstFactorial(raw_input())