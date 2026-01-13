def LongestWord(sen):
    word_list = sen.split(' ')
    longest = ''
    for word in word_list:
        if len(longest) < len(word):
            longest = word
    return longest


# keep this function call here
# print LongestWord(raw_input())