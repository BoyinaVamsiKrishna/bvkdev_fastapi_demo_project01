import re

def normalize_num(phn_num: str):
    return re.sub(r"\D", "", phn_num)

