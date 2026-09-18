import re

with open('index.html', 'r') as f:
    content = f.read()

# Extract the annotations array block
start_idx = content.find('const annotations = [')
end_idx = content.find('];', start_idx)
annotations_text = content[start_idx:end_idx]

# Extract the "text" fields
texts = re.findall(r"text:\s*'([^']+)'", annotations_text)

for i, text in enumerate(texts, start=1):
    print(f"{i}. {text}")

