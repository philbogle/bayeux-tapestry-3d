import sys
import re

with open('index.html', 'r') as f:
    content = f.read()

globe_btn = """            <button id="lang-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px; display: flex; align-items: center; justify-content: center;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg></button>"""

# Find the About link and insert globe button after it
content = content.replace('<a href="#" id="learn-more-link" style="color: #d6a848; text-decoration: none; pointer-events: auto;">About</a>', '<a href="#" id="learn-more-link" style="color: #d6a848; text-decoration: none; pointer-events: auto;">About</a>\n' + globe_btn)

# Insert Dialog HTML after Help Dialog
lang_dialog = """
    <div id="lang-dialog" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(20, 20, 20, 0.95); color: white; padding: 20px 30px; border-radius: 8px; border: 1px solid #444; z-index: 1000; min-width: 300px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5); font-family: serif;">
        <h3 style="margin-top: 0;">Select Language</h3>
        <div id="lang-options" style="display: flex; flex-direction: column; gap: 10px; margin-top: 20px;">
            <button class="lang-option" data-lang="en" style="padding: 10px; background: #5a4a35; color: white; border: 1px solid #d6a848; border-radius: 4px; cursor: pointer; font-size: 16px;">English</button>
            <button class="lang-option" data-lang="zh" style="padding: 10px; background: #2c221a; color: white; border: 1px solid #444; border-radius: 4px; cursor: pointer; font-size: 16px;">中文 (Chinese)</button>
        </div>
        <div style="text-align: right; margin-top: 20px;">
            <button id="close-lang" style="padding: 5px 15px; background: #444; color: white; border: none; border-radius: 4px; cursor: pointer;">Cancel</button>
        </div>
    </div>
"""
content = content.replace('    <div id="help-dialog"', lang_dialog + '    <div id="help-dialog"')

with open('index.html', 'w') as f:
    f.write(content)
