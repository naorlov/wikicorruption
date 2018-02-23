def common_pref_len(str1: str, str2: str):
    i = 0
    while i < len(str1) and i < len(str2) and str1[i] == str2[i]:
        i += 1
    return i

def acceptable_pref(str1: str, str2: str, accept: int):
    if common_pref_len(str1, str2) >= min(len(str1), len(str2)) - accept:
        return True
    return False
