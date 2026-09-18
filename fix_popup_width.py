import sys

with open('index.html', 'r') as f:
    content = f.read()

html_old = """max-width: 420px;"""
html_new = """width: 420px; max-width: 90vw;"""

content = content.replace(html_old, html_new)

with open('index.html', 'w') as f:
    f.write(content)
