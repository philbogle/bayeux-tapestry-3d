import re

with open('index.html', 'r') as f:
    content = f.read()

replacements = [
    (r'// Reverted back to the original simple organic texture, without large splotches to avoid visible seams', r'// Organic texture with a uniform noise profile to avoid visible tiling seams'),
    (r'// Darkened the base wall color to make the scene more dramatic', r'// Dark base wall color creates a dramatic contrast with the illuminated tapestry'),
    (r'// Vertical drag eliminated on mobile', r'// Vertical dragging is disabled on mobile devices for stability'),
]

for old, new in replacements:
    content = re.sub(old, new, content)

with open('index.html', 'w') as f:
    f.write(content)
