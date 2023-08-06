import requests
from typing import List


def chat_gpt(key, prompt, text):
    API_KEY = key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    }
    response = requests.post(
        'https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    return response.json()['choices'][0]['message']['content']


def seg_transcript(transcript: List[str]):
    transcript = [{"text": item["text"], "index": index,
                   "timestamp": item["start"]} for index, item in enumerate(transcript)]
    text = " ".join([x["text"]
                    for x in sorted(transcript, key=lambda x: x["index"])])
    length = len(text)
    seg_length = 3500
    n = length // seg_length + 1
    division = len(transcript) // n
    new_l = [transcript[i * division: (i + 1) * division] for i in range(n)]
    segedTranscipt = [" ".join([x["text"] for x in sorted(
        j, key=lambda x: x["index"])]) for j in new_l]
    return segedTranscipt
