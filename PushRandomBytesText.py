import socket
import os
import string
import random
import time

def random_bytes(length):
    return os.urandom(length)

def random_text(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def push_data(ip, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(data, (ip, port))

while True:
    # Push four random bytes to 127.0.0.1:3615
    data_bytes = random_bytes(4)
    push_data('127.0.0.1', 3615, data_bytes)
    
    # Push random text of 6 characters to 127.0.0.1:3614
    data_text = random_text(6).encode('utf-8')
    push_data('127.0.0.1', 3614, data_text)
    
    time.sleep(1)  # Sleep for a second to avoid overwhelming the server