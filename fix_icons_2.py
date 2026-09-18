import sys

with open('index.html', 'r') as f:
    content = f.read()

content = content.replace('T Titles', 'Titles')
content = content.replace('🔍', '⌕')
content = content.replace('♪ Sound', '♪')
content = content.replace('► Play Sound', '►')
content = content.replace('|| Pause Sound', '||')

with open('index.html', 'w') as f:
    f.write(content)
