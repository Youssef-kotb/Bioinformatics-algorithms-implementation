def suffix_array(s):
    return sorted(range(len(s)), key=lambda i: s[i:])

def inverse_suffix_array(sa):
    inv = [0] * len(sa)
    for i, val in enumerate(sa):
        inv[val] = i
    return inv
