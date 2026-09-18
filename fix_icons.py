import sys

with open('index.html', 'r') as f:
    content = f.read()

content = content.replace('🎵 Sound', '♪ Sound')
content = content.replace('🎵 Play Sound', '► Play Sound')
content = content.replace('⏸ Pause Sound', '|| Pause Sound')
content = content.replace('📝 Notes', '☰ Notes')

with open('index.html', 'w') as f:
    f.write(content)
