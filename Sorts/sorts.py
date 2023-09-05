def insertion(shuffled):
    ordered = []


def xor_swap(my_list, a, b):
    if a == b:
        return
    my_list[a] = int(my_list[a] ^ my_list[b])
    my_list[b] = int(my_list[a] ^ my_list[b])
    my_list[a] = int(my_list[a] ^ my_list[b])


def traditional_swap(my_list, a, b):
    if a == b:
        return
    temp = my_list[a]
    my_list[a] = my_list[b]
    my_list[b] = temp


def additive_swap(my_list, a, b):
    if a == b:
        return
    my_list[a] += my_list[b]
    my_list[b] += my_list[a] - my_list[b]
    my_list[a] -= my_list[b]


def insertion_sort(l):
    for idx in range(1, len(l)):
        while idx > 0:
            if l[idx] > l[idx-1]:
                l[idx], l[idx-1] = l[idx-1], l[idx]
            idx -= 1
    return l


def selection_sort(l):
    for idx in range(len(l)):
        g = greatest(l[idx:]) + idx
        l[g], l[idx] = l[idx], l[g]


def transpose(l, c):
    new = []
    for i in range(c):
        for j in range(c):
            new.append(l[j*c + i])
    return new


def column_sort(l, c):
    selection_sort(l)
    return transpose(l, c)


def greatest(l):
    g = 0
    for i in range(len(l)):
        g = i if l[i] > l[g] else g
    return g