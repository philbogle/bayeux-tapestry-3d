import sys

with open('index.html', 'r') as f:
    content = f.read()

html_old = """    <div id="context-scroll" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #f4e4bc; color: #3a2a1a; padding: 40px; border-radius: 4px; border: 2px solid #8b7355; z-index: 2000; max-width: 500px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 40px rgba(139, 115, 85, 0.2); font-family: 'MedievalSharp', serif;">
        <h3 id="context-title" style="margin-top: 0; font-size: 22px; border-bottom: 1px solid #8b7355; padding-bottom: 10px;">Scene Context</h3>
        <p id="context-text" style="font-size: 16px; line-height: 1.6; text-align: left; font-family: serif;"></p>
        <button id="close-context" style="margin-top: 20px; padding: 8px 20px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 16px;">Close</button>
    </div>"""

html_new = """    <div id="context-scroll" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #f4e4bc; color: #3a2a1a; padding: 40px; border-radius: 4px; border: 2px solid #8b7355; z-index: 2000; max-width: 500px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 40px rgba(139, 115, 85, 0.2); font-family: 'MedievalSharp', serif;">
        <h3 id="context-title" style="margin-top: 0; font-size: 22px; border-bottom: 1px solid #8b7355; padding-bottom: 10px;">Scene Context</h3>
        <p id="context-text" style="font-size: 16px; line-height: 1.6; text-align: left; font-family: serif;"></p>
        <div style="display: flex; justify-content: space-between; margin-top: 20px;">
            <button id="prev-scene" style="padding: 8px 15px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 16px;">&laquo; Prev</button>
            <button id="close-context" style="padding: 8px 20px; background: #5a4a35; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 16px;">Close</button>
            <button id="next-scene" style="padding: 8px 15px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 16px;">Next &raquo;</button>
        </div>
    </div>"""

content = content.replace(html_old, html_new)

with open('index.html', 'w') as f:
    f.write(content)
