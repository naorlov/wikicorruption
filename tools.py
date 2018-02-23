def common_pref_len(str1, str2):
    i = 0
    while i < len(str1) and i < len(str2) and str1[i] == str2[i]:
        i += 1
    return i

def acceptable_pref(str1, str2, accept):
    if common_pref_len(str1, str2) >= min(len(str1), len(str2)) - accept:
        return True
    return False

def has_intersection(year_id_arr1, year_id_arr2):
    has_intersection = False
    p1_id_set = set([estate[1] for estate in year_id_arr1])
    for _, id in year_id_arr2:
        if id in p1_id_set:
            has_intersection = True
            break
    return has_intersection
