import socket
from time import time
from io import StringIO
import threading

file = StringIO()
prime_list = []


def is_prime(num):
    if num & 1 == 0:
        return False
    if num == 2:
        return True
    d = 3
    while d * d <= num:
        if num % d == 0:
            return False
        d = d + 2
    return True


def writer():
    global prime_list
    print(f'start writer {threading.current_thread().name}')
    while prime_list:
        num = prime_list.pop()
        if is_prime(num):
            file.write(str(num) + '\n')
    print(f'finish writer {threading.current_thread().name}')


def server():
    global prime_list
    print(f'Start server...')
    with socket.socket() as sock:
        sock.bind(('0.0.0.0', 9090))
        sock.listen(10)
        while True:
            conn, addr = sock.accept()
            print('connected', addr)
            data = ""
            start = time()
            while True:
                num = conn.recv(4096).decode()
                if not num:
                    break
                data += num
            prime_list = eval(data)
            prime_list_len = len(prime_list)
            print(f'Server list ready in {time() - start}')
            tasks = []
            for i in range(3):
                task = threading.Thread(target=writer, args=(), daemon=False)
                task.start()
                tasks.append(task)
            for task in tasks:
                task.join()
            break
    with open('test.txt', 'w') as f:
        f.write(file.getvalue())
    print(f'Server time is: {time() - start}')
    print(f'Server counter is: {prime_list_len}')
    print(f'======================')