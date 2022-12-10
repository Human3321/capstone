import time, os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from vp_check import softmax_in, softmax_lo, softmax_부사
from vp_check import vp_word_in, vp_word_lo, 부사

# with sr.AudioFile('C:\\Users\\samsung\\Desktop\\code\\TTS_STT\\sample_voidfishing.wav') as source :
#       audio = r.record(source)

# 음성인식 (듣기, STT)
def listen(recignizer, audio):
    try:
        text = r.recognize_google(audio, language='ko')
        print('[음성1]' + text)
        answer(text)
    except sr.UnknownValueError:
        print('인식 실패')
    except sr.RequestError as e:
        print('요청 실패 : {0}'.format(e))

#대답
# 형태소 분석 추가 논의
def answer(input_text) :
    global vp_cnt, check_l
    input_text = input_text.split()
    for word in input_text:
        if vp_word_in.get(word):
            vp_cnt = vp_cnt + softmax_in(vp_word_in[word])
        elif vp_word_lo.get(word):
            vp_cnt = vp_cnt + softmax_lo(vp_word_lo[word])
        # elif 부사.get(word) :
        #     부사[word][0] = 부사[word][0] + 1
        #     if 부사[word][0] > 2 :
        #         vp_cnt = vp_cnt + softmax_부사(부사[word][1])
    if vp_cnt >= 0.6:
        print('보이스피싱 위험 !!!')
        stop_listening(wait_for_stop = False)
        check_l = False
    print(vp_cnt)

vp_cnt = 0
r = sr.Recognizer()
m = sr.Microphone()

print('감지 중...')
stop_listening = r.listen_in_background(m, listen)

check_l = True

while check_l:
    time.sleep(0.001)
print('종료')