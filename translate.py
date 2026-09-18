import json
import urllib.request
import urllib.parse
import time

def translate(text, target_lang='fr'):
    if not text:
        return ""
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return "".join([x[0] for x in result[0] if x[0]])
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text

def main():
    filename = 'tituli.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        if 'translations' in item and 'en' in item['translations']:
            en_trans = item['translations']['en']
            en_text = en_trans.get('text', '')
            en_context = en_trans.get('context', '')
            
            fr_text = translate(en_text, 'fr')
            fr_context = translate(en_context, 'fr')
            
            item['translations']['fr'] = {
                'text': fr_text,
                'context': fr_context
            }
            print(f"Translated scene {item.get('scene')} to French")
            time.sleep(0.2) # Be nice to the API
            
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
        
if __name__ == '__main__':
    main()
