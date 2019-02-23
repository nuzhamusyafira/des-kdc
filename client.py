import socket
import threading
import sys
import DES_algo

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234

uname = input("Masukkan username: ")
ip = '10.198.9.8'
print("Masukkan IP Address:",ip)
key_client = input("Masukkan key: ")

s.connect((ip, port))
#s.send(uname.encode('ascii'))
s.sendall(str.encode('\n'.join([str(uname), str(key_client)])))
clientRunning = True
sessionKey = "        "

def receiveMsg(sock):
    serverDown = False
    while clientRunning and (not serverDown):
        try:
            global sessionKey
            msg = sock.recv(1024).decode('ascii')
            if '>>' in msg:
                print(msg, end='')    
            elif '##' in msg:
                msg=msg.replace('##', '')
                msg = DES_algo.toDecrypt(msg, sessionKey)
                print(msg)
            elif '!!' in msg:
                msg=msg.replace('!!', '')
                msg = DES_algo.toDecrypt(msg, key_client)
                sessionKey = msg
                print('Session Key :',msg)
            else:
                print(msg)
        except:
            print('Server tidak dapat diakses. Klik enter untuk exit...')
            serverDown = True

threading.Thread(target = receiveMsg, args = (s,)).start()
while clientRunning:
    tempMsg = input()
    if '**quit' in tempMsg:
        clientRunning = False
        s.send('**quit'.encode('ascii'))
    else:
        tempMsg = DES_algo.toEncrypt(tempMsg, sessionKey)
        msg = uname + '>>' + tempMsg
        s.send(msg.encode('ascii'))