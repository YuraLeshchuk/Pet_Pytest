def FindIntersection(strArr):
    list1 = strArr[0].split(', ')
    list2 = strArr[1].split(', ')
    output = []

    for n in list1:
        if n in list2:
            output.append(n)

    if output:
        return ','.join(output)
    else:
        return 'false'


# keep this function call here
# print FindIntersection(raw_input())