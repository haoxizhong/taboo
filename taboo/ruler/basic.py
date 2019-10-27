import torch
import os
import urllib 
from transformers import (        BertConfig, BertForSequenceClassification, BertTokenizer,
                                  GPT2Config, GPT2LMHeadModel, GPT2Tokenizer)

class TabooBasicRuler:
    def __init__(self):
        # ppl ruler
        config_class, model_class, tokenizer_class = GPT2Config, GPT2LMHeadModel, GPT2Tokenizer
        config = config_class.from_pretrained("gpt2")
        self.tokenizer = tokenizer_class.from_pretrained("gpt2", do_lower_case=True)
        self.model = model_class.from_pretrained("gpt2", config=config)

        # next sentence
        _, model_class, tokenizer_class = BertConfig, BertForSequenceClassification, BertTokenizer
        self.bert_tokenizer = tokenizer_class.from_pretrained("bert-base-uncased")

        home_path = os.environ['HOME']

        if not os.path.exists(os.path.join(home_path, ".taboo_ckp")):
            os.makedirs(os.path.join(home_path, ".taboo_ckp"))
            # config.json
            url = 'https://thunlp.oss-cn-qingdao.aliyuncs.com/taboo/config.json'  
            urllib.request.urlretrieve(url, os.path.join(home_path, ".taboo_ckp", "config.json"))
            # pytorch_model.bin
            url = 'https://thunlp.oss-cn-qingdao.aliyuncs.com/taboo/pytorch_model.bin'  
            urllib.request.urlretrieve(url, os.path.join(home_path, ".taboo_ckp", "pytorch_model.bin"))
        self.bert_model = model_class.from_pretrained(os.path.join(home_path, ".taboo_ckp"))


    def check_relevance(self, sent, sentences):
        last_sentence = sentences[-1]

        block_size = 254
        y1 = self.bert_tokenizer.tokenize(last_sentence)[:block_size]
        y2 = self.bert_tokenizer.tokenize(sent)[:block_size]
        y = ["[CLS]"] + y1 + ["[SEP]"] + y2 + ["[SEP]"]
        y = self.bert_tokenizer.convert_tokens_to_ids(y)
        types = [0] * (len(y1)+2) + [1] * (len(y2)+1)
        atten = [1] * len(y)

        pads = 512 - len(y)
        y = y + [0] * pads
        types = types + [0] * pads
        atten = atten + [0] * pads

        batch = [
            torch.LongTensor([y]),
            torch.LongTensor([atten]),
            torch.LongTensor([types]),
            torch.LongTensor([[0]])
        ]

        with torch.no_grad():
            inputs = {'input_ids':      batch[0],
                    'attention_mask': batch[1],
                    'token_type_ids': batch[2],
                    'labels':         batch[3]}
            outputs = self.bert_model(**inputs)
            _, logits = outputs[:2]

        if logits[0][0] < logits[0][1]:
            return True
        else:
            return False

    def check_available(self, sent):
        tokens = self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(sent))
        batch = torch.LongTensor([tokens])
        with torch.no_grad():
            outputs = self.model(batch, labels=batch)
        lm_loss = outputs[0]
        # ppl = torch.exp(lm_loss / len(tokens))
        ppl = torch.exp(lm_loss).item()
        if ppl < 50:
            return True
        else:
            return False
