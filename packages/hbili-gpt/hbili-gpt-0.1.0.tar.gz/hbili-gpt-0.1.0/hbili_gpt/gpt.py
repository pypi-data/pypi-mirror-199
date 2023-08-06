# import openai
import requests
import logging

def chat(key, prompt, text):
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
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    return response.json()['choices'][0]['message']['content']

def segTranscipt(transcript):
    transcript = [{"text": item["content"], "index": index, "timestamp": item["from"]} for index, item in enumerate(transcript)]
    text = " ".join([x["text"] for x in sorted(transcript, key=lambda x: x["index"])])
    length = len(text)
    seg_length = 3500
    n = length // seg_length + 1
    division = len(transcript) // n
    new_l = [transcript[i * division: (i + 1) * division] for i in range(n)]
    segedTranscipt = [" ".join([x["text"] for x in sorted(j, key=lambda x: x["index"])]) for j in new_l]
    return segedTranscipt



"""
BilibiliSummary 有损压缩 
"""

limit = 7000 
def truncateTranscript(str):
    bytes = len(str.encode('utf-8'))
    if bytes > limit:
        ratio = limit / bytes
        newStr = str[:int(len(str)*ratio)]
        return newStr
    return str

def textToBinaryString(str):
    escstr = str.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
    binstr = ""
    for c in escstr:
        binstr += f"{ord(c):08b}"
    return binstr

def getChunckedTranscripts(textData, textDataOriginal):
    result = ""
    text = " ".join([x["text"] for x in sorted(textData, key=lambda x: x["index"])])
    bytes = len(textToBinaryString(text))
    
    if bytes > limit:
        evenTextData = [t for i, t in enumerate(textData) if i % 2 == 0]
        result = getChunckedTranscripts(evenTextData, textDataOriginal)
    else:
        if len(textDataOriginal) != len(textData):
            for obj in textDataOriginal:
                if any(t["text"] == obj["text"] for t in textData):
                    continue
                textData.append(obj)
                newText = " ".join([x["text"] for x in sorted(textData, key=lambda x: x["index"])])

                newBytes = len(textToBinaryString(newText))
                if newBytes < limit:
                    nextText = textDataOriginal[[t["text"] for t in textDataOriginal].index(obj["text"]) + 1]
                    nextTextBytes = len(textToBinaryString(nextText["text"]))
                    if newBytes + nextTextBytes > limit:
                        overRate = ((newBytes + nextTextBytes) - limit) / nextTextBytes
                        chunkedText = nextText["text"][:int(len(nextText["text"])*overRate)]
                        textData.append({"text": chunkedText, "index": nextText["index"]})
                        result = " ".join([x["text"] for x in sorted(textData, key=lambda x: x["index"])])

                    else:
                        result = newText
        else:
            result = text
    originalText = " ".join([x["text"] for x in sorted(textDataOriginal, key=lambda x: x["index"])])
    return originalText if result == "" else result