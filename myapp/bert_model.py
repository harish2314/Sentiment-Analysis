from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)

# tokenizer.save_pretrained('sentiment_analysis_tokenizer')
# model.save_pretrained('sentiment_analysis_bert_model')

tokenizer = AutoTokenizer.from_pretrained(os.path.join(BASE_DIR,"myapp/sentiment_analysis_tokenizer"))

bert_model = AutoModelForSequenceClassification.from_pretrained(os.path.join(BASE_DIR,"myapp/sentiment_analysis_bert_model"))

test_text = "After one month use, Bad bluetooth connection, and specially mice is very worst, i mean I have to speak very loud during call otherwise second person will not be able to hear. If any one want to listen music he can go with it but one who is looking it for call must go with other options.Review after using 5 months:- Now I am facing issue with Bluetooth connectivity, when I go to pair new device then this headphone is not even discoverable. Very bad experience"
test_token = tokenizer.encode(test_text, return_tensors='pt')
test_result = bert_model(test_token)
test_result = int(torch.argmax(test_result.logits))+1

label = ""
if test_result == 3:
  label = "NEUTRAL"
elif test_result < 3:
  label = "NEGATIVE"
else:
  label = "POSITIVE"
print(f"Content: {test_text}\nLabel: {label}\nRating: {test_result}")