from gtts import gTTS
from playsound import playsound
# 영어 음성 인식
# text = 'can i help you?'
# tts = gTTS(text = text, lang = 'en')

text = 'KB국민은행 측에서 대출 청약 전에 민원신청 들어오신 내용으로 연락을 드렸는데 혹시 잠시 통화 괜찮으세요?'
tts = gTTS(text = text, lang = 'ko')
file_name = 'sample.mp3'
tts.save(file_name)

playsound(file_name)