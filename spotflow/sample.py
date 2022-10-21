def absolute(x):
    if x < 0:
        x = -x
    return x


def sum(iter, start=0):
    count = start
    for i in iter:
        count += i
    return count


absolute(-10)       # 10
sum([1, 2])         # 3
sum([1, 2, 3], 1)   # 7
