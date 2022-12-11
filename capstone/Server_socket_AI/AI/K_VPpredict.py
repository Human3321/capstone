import torch
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
import pickle
from torch import nn
from kobert_tokenizer import KoBERTTokenizer
from kobert import get_pytorch_kobert_model

bertmodel, vocab = get_pytorch_kobert_model()

M_PATH = '/content/drive/MyDrive/캡스톤/best_model.pth'
T_PATH = "/content/drive/MyDrive/캡스톤/tok.pickle"
V_PATH = "/content/drive/MyDrive/캡스톤/vocab.pickle"

device = torch.device('cpu')

max_len = 200 # 해당 길이를 초과하는 단어에 대해선 bert가 학습하지 않음
batch_size = 64 # 배치 크기

class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer,vocab, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len,vocab=vocab, pad=pad, pair=pair)
        
        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    # i번째 데이터와 데이터의 label return
    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))
         
    # label 길이
    def __len__(self):
        return (len(self.labels))

# KoBERT 모델 구현
class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,#은닉층
                 num_classes=2,   ##클래스 수 조정##
                 dr_rate=None, #dropout 비율
                 params=None): 
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate
                 
        self.classifier = nn.Linear(hidden_size , num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)
    
    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)
        
        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device),return_dict=False)
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)

tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')

with open(T_PATH, 'rb') as handle:
    tok = pickle.load(handle)
    
with open(V_PATH, 'rb') as handle:
    vocab = pickle.load(handle)

model = BERTClassifier(bertmodel,  dr_rate=0.5)
model.load_state_dict(torch.load(M_PATH, map_location=device))

def calc_accuracy(X):
    max_vals, max_indices = torch.max(X, 1)
    acc = nn.functional.softmax(X, dim=-1).cpu().numpy()
    return acc[0][max_indices]


def VP_predict(predict_sentence):
    data = [predict_sentence, '0']
    dataset_another = [data] 

    another_test = BERTDataset(dataset_another, 0, 1, tok, vocab, max_len, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)
    test_acc = 0.0
    model.eval() 
    with torch.no_grad():
      for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate((test_dataloader)):
          token_ids = token_ids.long().to(device)
          segment_ids = segment_ids.long().to(device)
          valid_length= valid_length
          label = label.long().to(device)
          out = model(token_ids, valid_length, segment_ids)
          prediction = out.cpu().detach().numpy().argmax()
          test_acc = calc_accuracy(out)
      print(predict_sentence)
      print("=>보이스피싱일 확률 {:.2f}%".format(test_acc * 100))
      if prediction == 1:
        return 1
      else:
        return 0

# VP o
print(VP_predict('본인이 직접 움직일 필요 없으시고요 그냥 그 통장 안에 잔고없는 통장과 연결된 현금카드 갖고 계시는 거 있죠?\n네\n그냥 그 현금인출카드만 저희쪽으로 한 달 동안 빌려주시는 거에요'))
print(VP_predict('어 저는 금융범죄 수사 1팀장을 맡고 있는 신승용 검사라고 합니다.\n메모하세요 자 명의 도용 사건 내용 이해하셨나요?\n자 그럼 이 사건에 대해서는 지금 본인 사건이기 때문에 본인께서 구체적으로 알 권리가 있습니다.\n따라서 본 검사는 이번 사건에 대해서 구체적으로 설명을 해드릴 건데 설명 도중에 이해 못하시는 부분이 있으면 질문해 주시기 바랍니다.\n음 저희 검찰은 김혜선 외 공범 8명 금융범죄 사기단을 검거했습니다.'))
print(VP_predict('면허증 뭐 여권 같은 것도 전혀 없으신 거죠? 재발급 받아 보신 적도 한번도 없으신 거고.'))

# VP x
print(VP_predict('A : 저번에 빌린 10만원 언제 갚을거야?\nB : 까먹고 있었네.\n계좌번호 불러줘 지금 바로 송금할께\nA : 국민은행 ***…\nB : 송금했어. 다음번에 내가 밥 한번 살께'))
print(VP_predict('반갑습니다 상담사 땡땡땡입니다\n예 수고하십니다 저 세탁기가 작동이 안 돼요\n작동이 안 된다면은 뭐 전원은 들어오는데 회전만 안 되는 거에여\n네 전원은 들어와요\n많이 답답하셨겠습니다 고객님 저희 세탁기가 일반 통세탁기세여 드럼세탁기세여\n예 드럼 세탁기여\n드럼이구 혹시 사용하신 지는 일 년이 지나셨어여'))