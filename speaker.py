import time, os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# 음성인식 (듣기, STT)
def listen(recignizer, audio):
    try:
        text = r.recognize_google(audio, language='ko')
        print('[음성]' + text)
        answer(text)
    except sr.UnknownValueError:
        print('인식 실패')
    except sr.RequestError as e:
        print('요청 실패 : {0}'.format(e))

#대답
def answer(input_text) :
    answer_text = ''
    global vp_cnt, c
    if '계좌' in input_text :
        vp_cnt = vp_cnt + 2 
    elif '통장' in input_text :
        vp_cnt = vp_cnt + 2
    if vp_cnt >= 4 :
        print('보이스피싱 위험 !!!')
        vp_cnt = 0
        stop_listening(wait_for_stop = False)
        c = 0

vp_cnt = 0
r = sr.Recognizer()
m = sr.Microphone()

print('감지 중...')
stop_listening = r.listen_in_background(m, listen)

c = 1

while c == 1:
    time.sleep(0.01)
print('종료')