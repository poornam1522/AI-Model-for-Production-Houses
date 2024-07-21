import json
import requests
from concurrent.futures import ThreadPoolExecutor as Executor
import spacy

nlp = spacy.load("en_core_web_sm",disable = ['ner', 'tagger','lemmatizer','textcat'])

gpt3_url = "https://api.openai.com/v1/completions"
gpt3_headers = {
    "content-type": "application/json",
    "Authorization":"Bearer xxxxxxxxxxxxxx"
    }

def getsentences(txt):
  sentences = [i.text.strip() for i in nlp(txt).sents if i.text.strip()!=""]
  return sentences

def getparaphrase(sentence):

  gpt3_payload = {
  "model":"text-davinci-002",
  "prompt":"The following is an original sentence followed by a paraphrased version of it with a diverse choice of words:\n\noriginal: Once, a group of frogs was roaming around the forest in search of water.\nparaphrase: A herd of frogs was wandering around the woods in search of water.\n###\noriginal: Puppies were adopted by numerous kind souls at the puppy drive.\nparaphrase: Many kind souls adopted puppies during the puppy drive.\n###\noriginal: Symptoms of influenza include fever and nasal congestion.\nparaphrase: A stuffy nose and elevated temperature are signs you may have the flu.\n###\noriginal: {0}\nparaphrase:".format(sentence),
  "temperature":0.85,
  "max_tokens":256,
  "top_p":1,
  "frequency_penalty":0.72,
  "presence_penalty":0.72,
  "stop":["###"]
  }

  response = requests.request("POST", gpt3_url, json=gpt3_payload, headers=gpt3_headers)
  response = response.json()
  paraphrased_sentence = response['choices'][0]['text']
  paraphrased_sentence = paraphrased_sentence.strip()
  return paraphrased_sentence

def lambda_handler(event, context):
    raw_string = r'{}'.format(event['body'])
    body = json.loads(raw_string)
    originaltext = body['text']
    sentences = getsentences(originaltext)

    with Executor() as executor:
        futures = [executor.submit(getparaphrase, s) for s in sentences]

    paraphrased_sentences = [f.result() for f in futures]
    full_paraphrased_text = ' '.join(paraphrased_sentences)


    print("original text: ", originaltext)
    print("paraphrased_text: ", full_paraphrased_text)

    output = {
            "paraphrased": full_paraphrased_text

        }

    return {
        "statusCode": 200,
        "body": json.dumps(output),
    }
