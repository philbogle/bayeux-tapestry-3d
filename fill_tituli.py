import json

with open('tituli.json', 'r') as f:
    data = json.load(f)

start_x = 172.13
end_x = 600.0
unplaced = [item for item in data if 'x' not in item]
num_unplaced = len(unplaced)

if num_unplaced > 0:
    spacing = (end_x - start_x) / (num_unplaced + 1)
    
    current_x = start_x + spacing
    for item in data:
        if 'x' not in item:
            item['x'] = current_x
            item['y'] = 1.0
            current_x += spacing

with open('tituli.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Filled missing coordinates")
