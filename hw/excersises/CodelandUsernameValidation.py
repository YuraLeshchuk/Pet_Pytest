def CodelandUsernameValidation(str):
  # code goes here
  if len(str) >= 4 and len(str) <= 25 and str[0].isalpha() and str[-1] !='_':
    for i in str:
      if i.isalpha() or i.isdigit() or i =='_':
        return 'true'
  else:
    return 'false'
# keep this function call here
# print CodelandUsernameValidation(raw_input())