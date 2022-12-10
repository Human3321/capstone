import socket, os
import threading, wave, pyaudio, pickle,struct
import time, os
import speech_recognition as sr
from gtts import gTTS
from AI.BILSTM import VP_predict


# 쓰레드에서 실행되는 코드
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신
def audio_stream(client_socket, addr):
    r = sr.Recognizer()
    # CHUNK는 음성데이터를 불러올 때 한번에 몇개의 정수를 불러올 지 의미
    CHUNK = 1024
    # RATE는 음성 데이터의 샘플링 레이트 #hz
    RATE = 44100
    cnt = 0 # 전체 받은 bytes 길이 확인 용
    data = client_socket.recv(4*1024) # 바이트(bytes) 객체
    test = b"" # msg(bytes 객체) -> audiodata 형 변환을 위해 저장
    text = "" 

    payload_size = struct.calcsize("Q") # 바이트 데이터의 크기 8
    while True:
        try:
            # msg 크기 + α
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024) # 4K
                if not packet: break
                data+=packet
            # msg 길이 분리
            packed_msg_size = data[:payload_size]
            # 보낸 데이터(a 일부 or 이상)
            data = data[payload_size:]
            # msg 길이 pack -> unpack (tuple)
            # [0] => pack한 msg 길이
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            while len(data) < msg_size:
                # 남은 msg 가져오기
                data += client_socket.recv(4*1024)
            cnt += len(data) + 8
            # 의미있는 msg만(a) 추출
            frame_data = data[:msg_size]
            # cnt += len(frame_data)
            # 다음 msg 길이 등등
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)
            test += frame
            # 남은 or 수신된 data == 0 and 지금까지 데이터 길이 > 400000(대략 수신된 msg 길이)
            # 수정 필요
            if len(data) == 0 and len(test) >= 400000 :
                # print(len(test))
                # print(cnt) # 총 데이터+기록된 데이터 길이 확인
                # bytes -> AudioData 변환
                audio = sr.AudioData(test, RATE, 2)
                test = b""
                try :
                    # STT 시작
                    text = r.recognize_google(audio, language='ko')
                    # 잘 인식했나 확인용
                    print(text)
                except sr.UnknownValueError:
                    print('인식 실패')
                except sr.RequestError as e:
                    print('요청 실패 : {0}'.format(e))
                finally :
                    break
        except Exception as e :
            print("disconnection")
            break
    # 빅엔디안 형식 길이 2 bytes로 변환 후 클라이언트에 송신
    client_socket.sendall(VP_predict(text).to_bytes(2, 'big'))
    # 연결 종료
    client_socket.close()
    print('Audio closed', addr[0], ':', addr[1])
    
    
# 서버 IP 및 열어줄 포트
HOST = '0.0.0.0'
PORT = 9996

# 서버 소켓 생성
print('>> Server Start')
# 소켓 설정(TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 서버 연결 + 생성
server_socket.bind((HOST, PORT))
# 대기 clinet 설정 => 기본값
server_socket.listen()

try:
    while True:
        print('>> Wait' , threading.active_count())
        client_socket, addr = server_socket.accept();	
        client_th = threading.Thread(target=audio_stream, args = (client_socket, addr));	
        client_th.start();	
except Exception as e :
    print ('에러 : ',e)

finally:
    server_socket.close()
    
