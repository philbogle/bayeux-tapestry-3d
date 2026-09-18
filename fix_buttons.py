import sys

with open('index.html', 'r') as f:
    content = f.read()

html_old = """        <div style="display: flex; justify-content: space-between; margin-top: 20px;">
            <button id="prev-scene" style="padding: 8px 15px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 16px;">&laquo; Prev</button>
            <button id="close-context" style="padding: 8px 20px; background: #5a4a35; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 16px;">Close</button>
            <button id="next-scene" style="padding: 8px 15px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 16px;">Next &raquo;</button>
        </div>"""

html_new = """        <div style="display: flex; justify-content: space-between; margin-top: 15px;">
            <button id="prev-scene" style="padding: 5px 12px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 14px;">&laquo; Prev</button>
            <button id="close-context" style="padding: 5px 16px; background: #5a4a35; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 14px;">Close</button>
            <button id="next-scene" style="padding: 5px 12px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 14px;">Next &raquo;</button>
        </div>"""

content = content.replace(html_old, html_new)

with open('index.html', 'w') as f:
    f.write(content)
