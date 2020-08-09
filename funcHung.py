numbers = r'(\d+)\s*(,\s*\d+)*(\.\s*\d+)*'
cur_u_man_r = r'\s*(dong|trieu\s*\d*|trieu\s*\d*|tr\s*\d*|t[i|y]\s*\d*|USD|\$\s*(USD)?|ngan|VND|d)\s*(\/\s*1?\s*thang)?(\/\s*1?\s*nam)?(\/\s*1?\s*m\s?2)?'
def get_price_keyword(data):
  result = []
  content = remove_accents(data['content']).lower()
  result.append(data['id'])
  cur_list = re.findall(numbers + cur_u_man_r, content)
  for cur in cur_list:
    str = ''
    for word in cur:
      if word == '':
        continue
      else:
        str += word + ' '
    result.append(str)
  return result

print(get_price_keyword(data))