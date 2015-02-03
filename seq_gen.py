def add(a, b, union=False):
    if isinstance(a, str):
        if isinstance(b, str):
            a += b
    elif isinstance(a, list):
        if union:
            for b_b in b:
                if b_b not in a:
                    a.append(b_b)
        else:
            a.append(b)
    elif isinstance(a, set):
        a = a.union(b)
    else:
        raise TypeError
    return a


def gen_seq(vals, tp):
    if len(vals[0]) <= 1:
        return vals
    else:
        if tp == str:
            result = set()
        else:
            result = list()
        for i in vals:
            if tp == list:
                res = [[i[0]] + f for f in gen_seq([val[1:] for val in vals], tp)]
            else:
                res = [i[0] + f for f in gen_seq([val[1:] for val in vals], tp)]
            result = add(result, res, union=True)
        return result


def opt_gen_seq(a, b):
    if isinstance(a, str) and isinstance(b, str):
        tp = str
    elif isinstance(a, list) and isinstance(b, list):
        tp = list
    else:
        raise TypeError
    common = []
    a_dif = tp()
    b_dif = tp()
    if tp == str:
        result = set()
    else:
        result = list()

    for i in range(len(a)):
        if a[i] == b[i]:
            common.append(i)
        else:
            a_dif = add(a_dif, a[i])
            b_dif = add(b_dif, b[i])

    alt = gen_seq([a_dif, b_dif], tp)
    for al in alt:
        res = tp()
        k = 0
        for i in range(len(a)):
            if i in common:
                res = add(res, a[i])
            else:
                res = add(res, al[k])
                k += 1
        result = add(result, [res], union=True)
    return result

