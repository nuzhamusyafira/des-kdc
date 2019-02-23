import socket
import threading
import re
import random
import string
import DES_algo

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = str(socket.gethostbyname(socket.gethostname()))
port = 1234

clients = {}
clientKeys = {}

s.bind((ip, port))
s.listen()
print('IP Address Server: %s'%ip)

letters = string.ascii_lowercase
sessionKey = ''.join(random.choice(letters) for i in range(8))
#print(sessionKey)
def handleClient(client, uname):
    clientConnected = True
    keys = clients.keys()
    while clientConnected:
        try:
            msg = client.recv(1024).decode('ascii')
            found = False
            if '**quit' in msg:
                response = 'Goodbye!'
                client.send(response.encode('ascii'))
                clients.pop(uname)
                print(uname + ' logout dari server')
                clientConnected = False
            else:
                for name in keys:
                    if(uname!=name):
                        temp=msg
                        msg = uname +'>>'
                        print(msg, end='')
                        msg2=temp
                        msg2=msg2.replace(uname+'>>', '')
                        msg2=re.findall('..',msg2)
                        for x in range(len(msg2)):
                            msg2[x]=chr(int(msg2[x],16))
                        print(''.join(msg2))
                        msg=uname+'>>'
                        clients.get(name).send(msg.encode('ascii'))
                        msg = temp
                        msg = msg.replace(uname+'>>', '##')
                        clients.get(name).send(msg.encode('ascii'))
                        found = True
                if(not found):
                    client.send('Gagal mengirim pesan, tidak ada lawan bicara.'.encode('ascii'))
        except:
            clients.pop(uname)
            print(uname + ' logout dari server')
            clientConnected = False


while serverRunning:
    client, address = s.accept()
    #uname = client.recv(1024).decode('ascii')
    uname, keyclient = [str(i) for i in client.recv(1024).decode('ascii').split('\n')]
    print(str(uname),'connected to the server with master key',str(keyclient))
    client.send('Halo! Mulai chat dengan lawan bicaramu!'.encode('ascii'))
    
    if(client not in clients):
        clients[uname] = client
        clientKeys[uname] = keyclient
        encryptedSessionKey = DES_algo.toEncrypt(sessionKey, keyclient)
        msg = '!!' + encryptedSessionKey
        client.send(msg.encode('ascii'))
        threading.Thread(target = handleClient, args = (client, uname, )).start()