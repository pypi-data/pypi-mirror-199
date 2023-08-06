def pluck(arr, fields):
    if not fields:
        return arr

    if "ALL" in fields:
        return arr

    new_arr = []
    for a in arr:
        o = {k: v for k, v in a.items() if k.replace("#", "") in fields}
        new_arr.append(o)
    return new_arr
