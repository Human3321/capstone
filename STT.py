import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source :
  print('음성인식 시작')
  audio = r.listen(source) #마이크 로부터 음성 듣기
# with sr.AudioFile('C:\\Users\\samsung\\Desktop\\code\\TTS_STT\\sample_voidfishing.wav') as source :
#       audio = r.record(source)

try:
  text = r.recognize_google(audio, language='ko')
  print(text)
except sr.UnknownValueError:
  print('인식 실패')
except sr.RequestError as e:
  print('요청 실패 : {0}'.format(e))