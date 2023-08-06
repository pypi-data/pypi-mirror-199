def unique_list(iterable):
    ans = list()
    for x in iterable:
        if x not in ans:
            ans.append(x)
    return ans
    