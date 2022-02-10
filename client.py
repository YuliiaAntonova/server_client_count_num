import socket
from time import time


def is_prime(n):
    a = list(range(n + 1))
    a[1] = 0
    lst = []
    i = 2
    while i <= n:
        if a[i] != 0:
            lst.append(a[i])
            for j in range(i, n + 1, i):
                a[j] = 0
        i += 1
    return lst


def client():
    start = time()
    prime_list = is_prime(2000000)
    prime_len = len(prime_list)
    with socket.socket() as sock:
        sock.connect(('127.0.0.1', 9090))
        sock.send(str(prime_list).encode())
    print(f'Client time is: {time() - start}')
    print(f'Client counter is: {prime_len}')
    print(f'======================')