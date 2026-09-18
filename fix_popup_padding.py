import sys

with open('index.html', 'r') as f:
    content = f.read()

html_old = """    <div id="context-scroll" style="display: none; position: fixed; top: 60px; left: 50%; transform: translateX(-50%); background: rgba(244, 228, 188, 0.85); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); color: #3a2a1a; padding: 40px; border-radius: 4px; border: 2px solid rgba(139, 115, 85, 0.8); z-index: 2000; max-width: 500px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 40px rgba(139, 115, 85, 0.2); font-family: 'MedievalSharp', serif;">"""

html_new = """    <div id="context-scroll" style="display: none; position: fixed; top: 60px; left: 50%; transform: translateX(-50%); background: rgba(244, 228, 188, 0.70); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); color: #3a2a1a; padding: 25px 30px; border-radius: 4px; border: 2px solid rgba(139, 115, 85, 0.8); z-index: 2000; max-width: 500px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 40px rgba(139, 115, 85, 0.2); font-family: 'MedievalSharp', serif;">"""

content = content.replace(html_old, html_new)

with open('index.html', 'w') as f:
    f.write(content)
