import speech_recognition as sr
r = sr.Recognizer()
# with sr.Microphone() as source :
  # print('음성인식 시작')
  # audio = r.listen(source) #마이크 로부터 음성 듣기
with sr.AudioFile('C:\\Users\\samsung\\Desktop\\git\\sample_voidfishing.wav') as source :
      print('음성인식 시작')
      audio = r.record(source)
try:
  text = r.recognize_google(audio, language='ko')
  # text1 = r.recognize_ibm(audio, language='ko')
  # text2 = r.recognize_bing(audio, language='ko')
  # text3 = r.recognize_google_cloud(audio, language='ko')
  print(text)
  # print(text1)
  # print(text2)
  # print(text3)

except sr.UnknownValueError:
  print('인식 실패')
except sr.RequestError as e:
  print('요청 실패 : {0}'.format(e))