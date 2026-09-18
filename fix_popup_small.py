import sys

with open('index.html', 'r') as f:
    content = f.read()

html_old = """    <div id="context-scroll" style="display: none; position: fixed; top: 60px; left: 50%; transform: translateX(-50%); background: rgba(244, 228, 188, 0.70); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); color: #3a2a1a; padding: 25px 30px; border-radius: 4px; border: 2px solid rgba(139, 115, 85, 0.8); z-index: 2000; max-width: 500px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 40px rgba(139, 115, 85, 0.2); font-family: 'MedievalSharp', serif;">
        <h3 id="context-title" style="margin-top: 0; font-size: 22px; border-bottom: 1px solid #8b7355; padding-bottom: 10px;">Scene Context</h3>
        <p id="context-text" style="font-size: 16px; line-height: 1.6; text-align: left; font-family: serif;"></p>
        <div style="display: flex; justify-content: space-between; margin-top: 15px;">"""

html_new = """    <div id="context-scroll" style="display: none; position: fixed; top: 25px; left: 50%; transform: translateX(-50%); background: rgba(244, 228, 188, 0.70); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); color: #3a2a1a; padding: 15px 20px; border-radius: 4px; border: 2px solid rgba(139, 115, 85, 0.8); z-index: 2000; max-width: 420px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 40px rgba(139, 115, 85, 0.2); font-family: 'MedievalSharp', serif;">
        <h3 id="context-title" style="margin-top: 0; font-size: 19px; border-bottom: 1px solid #8b7355; padding-bottom: 8px;">Scene Context</h3>
        <p id="context-text" style="font-size: 14.5px; line-height: 1.5; text-align: left; font-family: serif; margin-bottom: 12px;"></p>
        <div style="display: flex; justify-content: space-between; margin-top: 10px;">"""

content = content.replace(html_old, html_new)

with open('index.html', 'w') as f:
    f.write(content)
