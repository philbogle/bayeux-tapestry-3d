import json

with open('tituli.json', 'r') as f:
    data = json.load(f)

for i, item in enumerate(data, start=1):
    print(f"{i}. {item['english']}")

