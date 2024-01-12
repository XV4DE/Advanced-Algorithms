import time


def runs_in(my_func, input):
    start = time.time()
    my_func(input)
    return time.time() - start


def fib(n, already_done={}):
    if n < 2:
        return 1
    return fib(n-1, already_done) + fib(n-2, already_done)


def fast_fib(n, already_done={}):
    if n < 2:
        return 1
    if n < len(already_done):
        return already_done[n]
    already_done[n] = fib(n-1, already_done) + fib(n-2, already_done)
    return already_done[n]