import sys

with open('index.html', 'r') as f:
    content = f.read()

html_old = """    <div id="context-scroll" style="display: none; position: fixed; top: 25px; left: 50%; transform: translateX(-50%); background: rgba(244, 228, 188, 0.95); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); color: #3a2a1a; padding: 15px 20px; border-radius: 4px; border: 2px solid rgba(139, 115, 85, 0.8); z-index: 2000; width: 420px; max-width: 90vw; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 40px rgba(139, 115, 85, 0.2); font-family: 'MedievalSharp', serif;">
        <h3 id="context-title" style="margin-top: 0; font-size: 19px; border-bottom: 1px solid #8b7355; padding-bottom: 8px;">Scene Context</h3>
        <p id="context-text" style="font-size: 14.5px; line-height: 1.5; text-align: left; font-family: serif; margin-bottom: 12px; min-height: 100px;"></p>
        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
            <button id="prev-scene" style="padding: 5px 12px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 14px;">&laquo; Prev</button>
            <button id="close-context" style="padding: 5px 16px; background: #5a4a35; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 14px;">Close</button>
            <button id="next-scene" style="padding: 5px 12px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 14px;">Next &raquo;</button>
        </div>
    </div>"""

html_new = """    <div id="context-scroll" style="display: none; position: fixed; top: 25px; left: 50%; transform: translateX(-50%); background: rgba(244, 228, 188, 0.95); backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); color: #3a2a1a; padding: 15px 20px; border-radius: 4px; border: 2px solid rgba(139, 115, 85, 0.8); z-index: 2000; width: 420px; max-width: 90vw; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 40px rgba(139, 115, 85, 0.2); font-family: 'MedievalSharp', serif;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
            <button id="prev-scene" style="padding: 5px 12px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 14px;">&laquo; Prev</button>
            <button id="close-context" style="padding: 5px 16px; background: #5a4a35; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 14px;">Close</button>
            <button id="next-scene" style="padding: 5px 12px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 14px;">Next &raquo;</button>
        </div>
        <h3 id="context-title" style="margin-top: 0; font-size: 19px; border-bottom: 1px solid #8b7355; padding-bottom: 8px;">Scene Context</h3>
        <p id="context-text" style="font-size: 14.5px; line-height: 1.5; text-align: left; font-family: serif; margin-bottom: 0;"></p>
    </div>"""

content = content.replace(html_old, html_new)

with open('index.html', 'w') as f:
    f.write(content)
