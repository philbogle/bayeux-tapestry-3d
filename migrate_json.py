import json

with open('tituli.json', 'r') as f:
    data = json.load(f)

for item in data:
    english_text = item.pop('english', '')
    context_text = item.pop('context', 'No historical context available for this scene.')
    
    item['translations'] = {
        'en': {
            'text': english_text,
            'context': context_text
        }
    }

with open('tituli.json', 'w') as f:
    json.dump(data, f, indent=2)

print("tituli.json migrated successfully.")
