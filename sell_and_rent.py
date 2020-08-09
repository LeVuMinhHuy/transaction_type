import re

import params


def get_data(data):
    if data[0] is None:
        return False
    #text = data[0].replace('\n', '').replace('\r', '')
    if re.search(params.s_and_r_ptrn, data[0], re.I):
        # if data[1] > 0 and data[2] > 0:
        #     return True
        return True
    else:
        return False
