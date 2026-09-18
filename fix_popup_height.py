import sys

with open('index.html', 'r') as f:
    content = f.read()

html_old = """<p id="context-text" style="font-size: 14.5px; line-height: 1.5; text-align: left; font-family: serif; margin-bottom: 12px;"></p>"""
html_new = """<p id="context-text" style="font-size: 14.5px; line-height: 1.5; text-align: left; font-family: serif; margin-bottom: 12px; min-height: 100px;"></p>"""

content = content.replace(html_old, html_new)

with open('index.html', 'w') as f:
    f.write(content)
