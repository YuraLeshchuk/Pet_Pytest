def BracketMatcher(strParam):
  a = strParam.count("(")
  b = strParam.count(")")
  if a==b:
    return 1
  else:
    return 0


# keep this function call here
print(BracketMatcher(input()))