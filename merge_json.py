import json

with open('ui_dict.json', 'r', encoding='utf-8') as f:
    ui_data = json.load(f)

with open('tituli.json', 'r', encoding='utf-8') as f:
    tituli_data = json.load(f)

merged = {
    "ui": ui_data,
    "tituli": tituli_data
}

with open('bayeux_data.json', 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print("Merged data successfully!")
