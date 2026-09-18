import re

with open('index.html', 'r') as f:
    content = f.read()

replacements = [
    (r'// Restore antialiasing for a smoother visual experience', r'// Enable antialiasing for smooth geometry edges'),
    (r'// Increased depth from 40 to 120 so the floor/ceiling don\'t clip at max zoom \(Z=40\)', r'// Depth set to 120 so the floor and ceiling don\'t clip when the camera zooms out to Z=40'),
]

for old, new in replacements:
    content = re.sub(old, new, content)

with open('index.html', 'w') as f:
    f.write(content)
