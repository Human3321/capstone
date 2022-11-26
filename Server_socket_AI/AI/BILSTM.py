from konlpy.tag import Mecab
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re
from tensorflow.keras.models import load_model

save_model = '/workspace/Server_socket_AI/AI/best_model_2.h5'
save_tokenizer = '/workspace/Server_socket_AI/AI/tokenizer_2.pickle'
loaded_model = load_model(save_model)

stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게', '만', '게임', '겜', '되', '음', '면']
tmp = ['히히', '땡땡땡', '땡땡', '땡']
stopwords = stopwords + tmp

# 형태소 분석기 Mecab을 사용하여 토큰화 작업을 수행
mecab = Mecab()

max_len = 200

with open(save_tokenizer, 'rb') as handle:
    tokenizer = pickle.load(handle)

def VP_predict(new_sentence):
    new_sentence_data = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
    new_sentence_data = mecab.morphs(new_sentence_data) # 토큰화
    new_sentence_data = [word for word in new_sentence_data if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence_data]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new, verbose=0)) # 예측
    # print("="*40)
    # print("=>보이스피싱일 확률 {:.2f}%".format(score * 100))
    if(score > 0.6):
        return 1
        # print("판별 결과 : 보이스피싱입니다.")
    else:
        return 0
        # print("판별 결과 : 보이스피싱이 아닙니다.")
    # print()
    # print("-"*40)
    # return score
# # VP o
# print(VP_predict('본인이 직접 움직일 필요 없으시고요 그냥 그 통장 안에 잔고없는 통장과 연결된 현금카드 갖고 계시는 거 있죠?\n네\n그냥 그 현금인출카드만 저희쪽으로 한 달 동안 빌려주시는 거에요'))
# VP_predict('어 저는 금융범죄 수사 1팀장을 맡고 있는 신승용 검사라고 합니다.\n메모하세요 자 명의 도용 사건 내용 이해하셨나요?\n자 그럼 이 사건에 대해서는 지금 본인 사건이기 때문에 본인께서 구체적으로 알 권리가 있습니다.\n따라서 본 검사는 이번 사건에 대해서 구체적으로 설명을 해드릴 건데 설명 도중에 이해 못하시는 부분이 있으면 질문해 주시기 바랍니다.\n음 저희 검찰은 김혜선 외 공범 8명 금융범죄 사기단을 검거했습니다.')
# VP_predict('면허증 뭐 여권 같은 것도 전혀 없으신 거죠? 재발급 받아 보신 적도 한번도 없으신 거고.')

# # VP x
# VP_predict('A : 저번에 빌린 10만원 언제 갚을거야?\nB : 까먹고 있었네.\n계좌번호 불러줘 지금 바로 송금할께\nA : 국민은행 ***…\nB : 송금했어. 다음번에 내가 밥 한번 살께')
# VP_predict('반갑습니다 상담사 땡땡땡입니다\n예 수고하십니다 저 세탁기가 작동이 안 돼요\n작동이 안 된다면은 뭐 전원은 들어오는데 회전만 안 되는 거에여\n네 전원은 들어와요\n많이 답답하셨겠습니다 고객님 저희 세탁기가 일반 통세탁기세여 드럼세탁기세여\n예 드럼 세탁기여\n드럼이구 혹시 사용하신 지는 일 년이 지나셨어여')