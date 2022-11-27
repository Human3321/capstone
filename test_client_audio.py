import socket
import threading, wave, pyaudio,pickle,struct
import time, os
from _thread import *

# HOST = '127.0.0.1'# 'tmp-zwadn.run.goorm.io'
# PORT = 9999 # 외부포트

HOST = '3.35.169.113' # 호스트 IP
PORT = 51752 # 외부포트

# 소켓 설정(TCP)
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT)) #소켓 서버 연결

# audio(.wav) 전송 함수
def audio_stream(client_socket):
    CHUNK = 1024 # 읽고올 최대 프레임
    wf = wave.open("C:/Users/samsung/Desktop/캡스톤_개발_음성소켓통신_AI/음성 소켓통신/Test-1.wav", 'rb')
    data = None
    cnt = 0
    while True:
        try:
            # 최대 n 프레임의 오디오를 bytes 객체로 읽고 반환
            data = wf.readframes(CHUNK)
            if not data : 
                # audio(.wav) 전송 끝
                print('전송 끝')
                break
            else:
                # 데이터 자료형에 상관없이 (byte형식)으로 저장
                a = pickle.dumps(data) # data 객체 데이터 저장
                # pickle로 저장한 msg 길이(struct -> packing) + msg
                message = struct.pack("Q",len(a))+a
                # msg 서버로 전송
                client_socket.sendall(message)
                # 얼마 보냈는지 count cnt 변수
                # cnt += len(data)
        except: 
            print("error")
            break
    # 전송 끝
    print('end') 
    # 마지막에 보낸 msg 길이 + 총 msg 길이
    # print(len(pickle.loads(a)), len(a), len(message), cnt)

# 서버로 부터 결과 수신
def recv_data(client_socket) :
    i = 0
    while i == 0:
        # 결과 수신 (0(vp) or 1(non-vp))
        data = client_socket.recv(1024)
        # 받은 결과 print
        print("recive : ",int.from_bytes(data, byteorder='big'))
        i = 1
    # 반복문 종료
    # 서버 연결 끊기
    client_socket.close()


# audio 전송
audio_stream(client_socket)
# 그에 따른 결과 수신
recv_data(client_socket)
# t2.start()
