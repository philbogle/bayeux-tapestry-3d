import json
import urllib.request
import urllib.parse
import time

def translate(text):
    if not text:
        return text
    
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q=" + urllib.parse.quote(text)
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        
        # The result is an array of arrays. The first element of the main array contains the translated sentences.
        translated_text = "".join([sentence[0] for sentence in data[0]])
        return translated_text
    except Exception as e:
        print(f"Error translating: {e}")
        return text

def main():
    with open('tituli.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i, item in enumerate(data):
        if 'translations' in item and 'en' in item['translations']:
            en_text = item['translations']['en'].get('text', '')
            en_context = item['translations']['en'].get('context', '')
            
            print(f"Translating scene {item.get('scene', i)}...")
            
            zh_text = translate(en_text)
            zh_context = translate(en_context)
            
            item['translations']['zh'] = {
                'text': zh_text,
                'context': zh_context
            }
            
            time.sleep(0.1) # Be nice to the API

    with open('tituli.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Translation complete and saved to tituli.json")

if __name__ == '__main__':
    main()
