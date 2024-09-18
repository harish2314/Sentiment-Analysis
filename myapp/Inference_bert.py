import requests, os
from dotenv import load_dotenv


load_dotenv()
BERT_INFERENCE_API = os.getenv("BERT_INFERENCE_API")

API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
headers = {"Authorization": f"Bearer {BERT_INFERENCE_API}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "The product seems average at this price",
})

rating = int(output[0][0]['label'][0])
print(rating)
