import sys

with open('index.html', 'r') as f:
    content = f.read()

# Add French option to language picker
lang_opts_old = """        <div id="lang-options" style="display: flex; flex-direction: column; gap: 10px; margin-top: 20px;">
            <button class="lang-option" data-lang="en" style="padding: 10px; background: #5a4a35; color: white; border: 1px solid #d6a848; border-radius: 4px; cursor: pointer; font-size: 16px;">English</button>
            <button class="lang-option" data-lang="zh" style="padding: 10px; background: #2c221a; color: white; border: 1px solid #444; border-radius: 4px; cursor: pointer; font-size: 16px;">中文 (Chinese)</button>
        </div>"""
lang_opts_new = """        <div id="lang-options" style="display: flex; flex-direction: column; gap: 10px; margin-top: 20px;">
            <button class="lang-option" data-lang="en" style="padding: 10px; background: #5a4a35; color: white; border: 1px solid #d6a848; border-radius: 4px; cursor: pointer; font-size: 16px;">English</button>
            <button class="lang-option" data-lang="zh" style="padding: 10px; background: #2c221a; color: white; border: 1px solid #444; border-radius: 4px; cursor: pointer; font-size: 16px;">中文 (Chinese)</button>
            <button class="lang-option" data-lang="fr" style="padding: 10px; background: #2c221a; color: white; border: 1px solid #444; border-radius: 4px; cursor: pointer; font-size: 16px;">Français (French)</button>
        </div>"""
content = content.replace(lang_opts_old, lang_opts_new)

# Update uiDict in changeLanguage
dict_old = """            // Translate static UI elements
            const uiDict = {
                'en': { help: 'Help', about: 'About', titles: 'Titles', notes: '☰ Notes' },
                'zh': { help: '帮助', about: '关于', titles: '标题', notes: '☰ 笔记' }
            };
            
            const dict = uiDict[currentLanguage] || uiDict['en'];
            document.querySelectorAll('#help-link').forEach(el => el.innerText = dict.help);
            document.querySelectorAll('#learn-more-link').forEach(el => el.innerText = dict.about);
            document.querySelectorAll('#toggle-supertitles').forEach(el => el.innerText = dict.titles);
            document.querySelectorAll('#notes-btn').forEach(el => el.innerText = dict.notes);"""
dict_new = """            // Translate static UI elements
            const uiDict = {
                'en': { help: 'Help', about: 'About', titles: 'Titles', notes: '☰ Notes', prev: 'Prev', next: 'Next', close: 'Close' },
                'zh': { help: '帮助', about: '关于', titles: '标题', notes: '☰ 笔记', prev: '上一个', next: '下一个', close: '关闭' },
                'fr': { help: 'Aide', about: 'À propos', titles: 'Titres', notes: '☰ Notes', prev: 'Préc', next: 'Suivant', close: 'Fermer' }
            };
            
            const dict = uiDict[currentLanguage] || uiDict['en'];
            document.querySelectorAll('#help-link').forEach(el => el.innerText = dict.help);
            document.querySelectorAll('#learn-more-link').forEach(el => el.innerText = dict.about);
            document.querySelectorAll('#toggle-supertitles').forEach(el => el.innerText = dict.titles);
            document.querySelectorAll('#notes-btn').forEach(el => el.innerText = dict.notes);
            
            const prevBtn = document.getElementById('prev-scene');
            const nextBtn = document.getElementById('next-scene');
            const closeBtn = document.getElementById('close-context');
            if (prevBtn) prevBtn.innerText = dict.prev;
            if (nextBtn) nextBtn.innerText = dict.next;
            if (closeBtn) closeBtn.innerText = dict.close;"""
content = content.replace(dict_old, dict_new)

# Font change for French
font_old = """const fontStr = currentLanguage === 'zh' ? `normal ${fontSize}px serif` : `normal ${fontSize}px 'MedievalSharp', serif`;"""
font_new = """const fontStr = currentLanguage === 'zh' ? `normal ${fontSize}px serif` : `normal ${fontSize}px 'MedievalSharp', serif`;""" # French uses MedievalSharp fine

with open('index.html', 'w') as f:
    f.write(content)
