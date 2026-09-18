import sys

with open('index.html', 'r') as f:
    content = f.read()

html_old = """background: rgba(244, 228, 188, 0.70);"""
html_new = """background: rgba(244, 228, 188, 0.95);"""

content = content.replace(html_old, html_new)

with open('index.html', 'w') as f:
    f.write(content)
