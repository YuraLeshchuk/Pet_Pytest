def QuestionsMarks(s):
    a = 11
    b = 'false'
    c = 0
    for i in s:
        if i.isdigit():
            if int(i) + a == 10:
                if c != 3:
                    return 'false'
                b = 'true'
            c = 0
            a = int(i)
        elif i == '?':
            c += 1
    return b


# keep this function call here
print(QuestionsMarks("arrb6???4xxbl5???eee5"))