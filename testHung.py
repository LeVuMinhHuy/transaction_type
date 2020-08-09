import re 

text = 'Ban nha mat tien 120trieu/thang'
numbers = r'(\d+)\s*(,\s*\d+)*(\.\s*\d+)*'
cur_u_man_r = r'\s*(dong|trieu\s*\d*|trieu\s*\d*|tr\s*\d*|t[i|y]\s*\d*|USD|\$\s*(USD)?|ngan|VND|d)\s*(\/\s*1?\s*thang)?(\/\s*1?\s*nam)?(\/\s*1?\s*m2)?'
print(re.findall(numbers+cur_u_man_r, text))

# def find_sub_list(sl,l):
#     results=[]
#     sll=len(sl)
#     for ind in (i for i,e in enumerate(l) if e==sl[0]):
#         if l[ind:ind+sll]==sl:
#             results.append((ind,ind+sll-1))

#     return results

# a = ['một', 'con', 'vịt', 'có', '25', 'cái', 'cánh', 'giá', '25', 'triệu', '/', 'tháng']
# b = ['25','triệu', 'tháng']

# print(find_sub_list(b,a))