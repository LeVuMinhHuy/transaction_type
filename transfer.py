import re

import params


def get_data(data):
    # data[0] is message
    # Sang nhượng thuê thì giá phải thỏa range (thuê: <=500tr, nếu content thuê mà >500tr thì coi như type=1)
    # Bán sang nhượng <=500 --> Lớn hơn thì coi như type=1
    # Content: Mặt bằng kinh doanh không tốt nên nhợợng lại giá 200tr
    if re.search(params.transfer_ptrn, data[0], re.I):
        return True
    return False
