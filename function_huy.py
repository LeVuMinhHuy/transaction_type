import json
import re
from xacdinh import xacdinh


s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def remove_accents(input_str):
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s

def find_sub_list(sl,l):
    results=[]
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            results.append((ind,ind+sll-1))
    #print(results)
    return results

numbers = r'(\d+)\s*(,\s*\d+)*(\.\s*\d+)*'
cur_u_man_r = r'\s*(dong|trieu\s*\d*|trieu\s*\d*|tr\s*\d*|t[i|y]\s*\d*|USD|\$\s*(USD)?)\s*(\/\s*1?\s*thang)?(\/\s*1?\s*nam)?(\/\s*1?\s*m\s?2)?'
def get_price_keyword(data):
  result = []
  content_tmp = remove_accents(data['content']).lower()
  content = ''
  for i in range(len(content_tmp)):
    if content_tmp[i] == '\n' or content_tmp[i] == '\r':
      continue
    content += content_tmp[i]
  result.append(data)
  cur_list = re.findall(numbers + cur_u_man_r, content)
  lst = []
  for cur in cur_list:
    str = ''
    for word in cur:
      if word == '' or cur.index(word) == 0 or word[0] == '.' or word[0] == ',':
        str += word
      else:
        str += ' ' + word
    lst.append(str+'+Bán')
  result.append(lst)  
  return result

def getFullPrice(listPhuong):
    lstPriceSell = []
    lstPriceRent = []
    # lstPriceUnknown = []

    for p in listPhuong[1]:
        priceAndType = p.split('+')
        priceAndType.insert(0, listPhuong[0])

        resultPrice = get_price(priceAndType)

        # print('result price', resultPrice)
        if resultPrice[1] == 0:
            lstPriceSell.append(resultPrice[0])
        elif resultPrice[1] == 1:
            lstPriceRent.append(resultPrice[0])
        elif resultPrice[1] == 2:
            lstPriceSell.append(0)
            lstPriceRent.append(0)
        
    print('Price Sell', lstPriceSell)
    print('Price Rent', lstPriceRent)
    print('\n')
    # print(lstPriceUnknown)



def get_price(priceAndType):
    ty=['ty','ti']
    trieu=['trieu','tr']
    nam=['nam']

    gia = []

    priceAndType[1] = remove_accents(priceAndType[1]).lower().split(' ')
    # print("a", priceAndType[1])

    for t in ty:
        if t in priceAndType[1] or (t + 'TL') in priceAndType[1]:
            k = 1000000000
    for tr in trieu:
        if tr in priceAndType[1] or (tr + 'TL') in priceAndType[1]:
            k = 1000000

    if ',' in priceAndType[1][0]:
        lstT = priceAndType[1][0].split(',')
        priceAndType[1][0] = lstT[1]
        priceAndType[1].insert(0, ',')
        priceAndType[1].insert(0, lstT[0])
        pivot = priceAndType[1].index(',')
        f = priceAndType[1][pivot - 1]
        s = priceAndType[1][pivot + 1]
        if f.isdigit() and s.isdigit():
            gia.append(float(f + '.' + s) * k)

    if '.' in priceAndType[1][0]:
        lstT = priceAndType[1][0].split('.')
        priceAndType[1][0] = lstT[1]
        priceAndType[1].insert(0, '.')
        priceAndType[1].insert(0, lstT[0])
        # print(priceAndType[1])
        pivot = priceAndType[1].index('.')
        if pivot < len(priceAndType[1]) - 1:
            f = priceAndType[1][pivot - 1]
            s = priceAndType[1][pivot + 1]
            if f.isdigit() and s.isdigit():
                gia.append(float(f + '.' + s) * k)

    if len(gia) == 0:
        check_t_tr = 0
        for t in ty:
            if t in priceAndType[1] or (t + 'TL') in priceAndType[1]:
                pivot = priceAndType[1].index(t)
                k = 1000000000
                if pivot < len(priceAndType[1]) - 1:
                    if priceAndType[1][pivot - 1].isdigit():
                        if priceAndType[1][pivot + 1].isdigit():
                            gia.append(k * float(priceAndType[1][pivot - 1] + '.' + priceAndType[1][pivot + 1]))
                            check_t_tr += 1
                        else:
                            gia.append(k * float(priceAndType[1][pivot - 1]))

                else:
                    if priceAndType[1][pivot - 1].isdigit():
                        gia.append(k * float(priceAndType[1][pivot - 1]))

        if check_t_tr != 1:
            check_t=0
            for tr in trieu:
                if tr in priceAndType[1] or (tr + 'TL') in priceAndType[1]:
                    pivot = priceAndType[1].index(tr)
                    k = 1000000
                    if priceAndType[1][pivot - 1].isdigit():
                        gia.append(k * float(priceAndType[1][pivot - 1]))
                check_t=1

            if check_t==1:
                if 'm' in priceAndType[1]:
                        tmp = str(priceAndType[0]['id']) + 'can xac dinh lai'
                        if xacdinh(priceAndType[0]) > 0 and xacdinh(priceAndType[0]) != tmp:
                            print("Area: ",xacdinh(priceAndType[0]))
                            if len(gia) >0:
                                gia[0]=gia[0] * xacdinh(priceAndType[0])
    for n in nam:
        if n in priceAndType[1]:
            if len(gia) > 0:
                gia[0] = gia[0] /12

    # print(priceAndType[2])
    if priceAndType[2] == 'Bán':
        gia.append(0)
    elif priceAndType[2] == 'Thuê':
        gia.append(1)
    elif priceAndType[2] == 'None':
        gia.append(2)

    # print("giá", gia)
    return gia

    

def phuong(dataset):
    ban = []
    thue = []
    aBan = []
    aThue = []
    addrB = []
    addrT = []

    index = []
    ind = []
    for data in dataset:
        ban.append(data['id'])
        thue.append(data['id'])
        content = remove_accents(data['content']).lower().split(' ')
        for c in range(0, len(content)):
            if content[c] in ['ban', 'ban,', 'ban.', 'nhuong', 'nhuong,', 'nhuong.']:
                addrB.append(c)
            if content[c] in ['thue', 'thue,', 'thue.']:
                addrT.append(c)
            continue
        ban.append(addrB)
        thue.append(addrT)
        aBan.append(ban)
        aThue.append(thue)
        ban = []
        thue = []
        addrB = []
        addrT = []

        ind.append(data['id'])
        test = get_price_keyword(data)
        text = []
        addr = []
        for t in test:
            # t.split(' ')
            for i in content:
                if i in t:
                    # print(content.index(i))
                    text.append(t)
                    addr.append(content.index(i))
                    break
        ind.append(text)
        ind.append(addr)
        # print(data['id'])
        index.append(ind)
        ind = []
        text = []
        addr = []
    # print("Price index: ", index)
    # print("Ban index: ", aBan)
    # print("Thue index: ", aThue)

    res = []
    result = []
    for i in range(0, len(dataset)):
        if len(index[i][1]) == 0:
            # res.append("a")
            # res.append("+None")
            res.append(str(index[i][0]) + "+None")
        else:
            res.append(index[i][0])
            if index[i][1] != []:
                for p in index[i][1]:
                    if aBan[i][1] == [] and aThue[i][1] == []:
                        res.append(p + "+None")
                    elif aBan[i][1] != [] and aThue[i][1] == []:
                        res.append(p + "+Ban")
                    elif aBan[i][1] == [] and aThue[i][1] != []:
                        res.append(p + "+Thue")
                    else:
                        sellB = []
                        rentB = []
                        sellA = []
                        rentA = []
                        for q in range(0, len(index[i][2])):
                            if len(aBan[i][1]) >= 1:
                                for b in range(0, len(aBan[i][1])):
                                    if aBan[i][1][b] < index[i][2][q]:
                                        sellB.append(aBan[i][1][b])
                                    elif q == len(index[i][2]) - 1 and aBan[i][1][b] > index[i][2][q]:
                                        sellA.append(aBan[i][1][b])
                                    else:
                                        continue
                            if len(aThue[i][1]) >= 1:
                                for th in range(0, len(aThue[i][1])):
                                    if aThue[i][1][th] < index[i][2][q]:
                                        rentB.append(aThue[i][1][th])
                                    elif q == (len(index[i][2]) - 1) and aThue[i][1][th] > index[i][2][q]:
                                        rentA.append(aThue[i][1][th])
                                    else:
                                        continue
                            if sellB != [] and rentB != []:
                                if sellB[len(sellB) - 1] < rentB[len(rentB) - 1]:
                                    res.append(p + "+Thue")
                                else:
                                    res.append(p + "+Ban")
                            elif sellB != [] and rentB == []:
                                res.append(p + "+Ban")
                            elif sellB == [] and rentB != []:
                                res.append(p + "+Thue")
                            elif sellB == [] and rentB == [] and q == len(index[i][2]) - 1:
                                if sellA != [] and rentA != []:
                                    if sellA[len(sellB) - 1] < rentA[len(rentB) - 1]:
                                        res.append(p + "+Ban")
                                    else:
                                        res.append(p + "+Thue")
                                elif sellA != [] and rentA == []:
                                    res.append(p + "+Ban")
                                elif sellA == [] and rentA != []:
                                    res.append(p + "+Thue")
                                elif sellA == [] and rentA == []:
                                    res.append(p + "+None")
                            sellA = []
                            sellB = []
                            rentA = []
                            rentB = []

        res = []
        result.append(res)

    return result
    # print(result)



with open('data.json', encoding="utf-8") as json_file:
    dataset = json.load(json_file)
    newdata = phuong(dataset)
    print(newdata)
    # getFullPrice(newdata)

    # for data in dataset:
    #     passList = [118250]
    #     if data['id'] in passList:
    #         continue

    #     # lstTemp = []
    #     # att = data['attributes']
    #     # for i in att:
    #     #     if i['type'] == 'price':
    #     #         lstTemp.append(i['content'] + '+' + 'Bán')

    #     # print(lstTemp)

    #     # getFullPrice([data, lstTemp])

    
    #     listHung = get_price_keyword(data)
    #     print(listHung[1])
    #     getFullPrice(listHung)


    # getFullPrice([dataset[0], ['14,5 tr+Bán']])


        