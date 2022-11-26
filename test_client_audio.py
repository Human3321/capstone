import socket
import threading, wave, pyaudio,pickle,struct
import time, os
from _thread import *

# HOST = '127.0.0.1'# 'tmp-zwadn.run.goorm.io'
# PORT = 9999 # 외부포트

HOST = '3.35.169.113'
PORT = 51752

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def audio_stream(client_socket):
    CHUNK = 1024
    wf = wave.open("C:/Users/samsung/Desktop/캡스톤_개발_음성소켓통신_AI/음성 소켓통신/Test-1.wav", 'rb')
    data = None
    cnt = 0
    while True:
        try:
            data = wf.readframes(CHUNK)
            if not data : # print(len(message), len(data), len(a));
                print('dede')
                break
            else:
                a = pickle.dumps(data) # data 객체 데이터 저장
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                cnt += len(data)
        except:
            print("error")
            break
    print('end')
    print(len(pickle.loads(a)), len(a), len(message), cnt)


def recv_data(client_socket) :
    i = 0
    while i == 0:
        data = client_socket.recv(1024)
        print("recive : ",int.from_bytes(data, byteorder='big'))
        i = 1
    client_socket.close()



audio_stream(client_socket)
recv_data(client_socket)
# t2.start()
