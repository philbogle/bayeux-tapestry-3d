import sys

with open('index.html', 'r') as f:
    content = f.read()

lang_logic = """
        function changeLanguage(lang) {
            currentLanguage = lang;
            localStorage.setItem('bayeux_lang', currentLanguage);
            
            // Update UI buttons
            document.querySelectorAll('.lang-option').forEach(btn => {
                if (btn.getAttribute('data-lang') === currentLanguage) {
                    btn.style.background = '#8b7355';
                    btn.style.border = '1px solid #f4e4bc';
                } else {
                    btn.style.background = '#2c221a';
                    btn.style.border = '1px solid #444';
                }
            });
            
            // Translate static UI elements
            const uiDict = {
                'en': { help: 'Help', about: 'About', titles: 'Titles', notes: '☰ Notes' },
                'zh': { help: '帮助', about: '关于', titles: '标题', notes: '☰ 笔记' }
            };
            
            const dict = uiDict[currentLanguage] || uiDict['en'];
            document.querySelectorAll('#help-link').forEach(el => el.innerText = dict.help);
            document.querySelectorAll('#learn-more-link').forEach(el => el.innerText = dict.about);
            document.querySelectorAll('#toggle-supertitles').forEach(el => el.innerText = dict.titles);
            document.querySelectorAll('#notes-btn').forEach(el => el.innerText = dict.notes);
            
            document.getElementById('lang-dialog').style.display = 'none';
            
            // Re-render all 3D meshes
            annotations.forEach(ann => {
                if (ann.mesh) {
                    scene.remove(ann.mesh);
                    ann.mesh.geometry.dispose();
                    ann.mesh.material.map.dispose();
                    ann.mesh.material.dispose();
                }
                const str = (ann.data.translations && ann.data.translations[currentLanguage]) ? ann.data.translations[currentLanguage].text : ann.data.translations['en'].text;
                const newMesh = createTextMesh(str, ann.data.x !== undefined);
                newMesh.position.set(ann.data.x, ann.data.y, 0.05);
                newMesh.visible = false;
                ann.mesh = newMesh;
                scene.add(newMesh);
            });
        }
"""

listener_logic = """
        document.querySelectorAll('#lang-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                // Highlight current language
                document.querySelectorAll('.lang-option').forEach(opt => {
                    if (opt.getAttribute('data-lang') === currentLanguage) {
                        opt.style.background = '#8b7355';
                        opt.style.border = '1px solid #f4e4bc';
                    } else {
                        opt.style.background = '#2c221a';
                        opt.style.border = '1px solid #444';
                    }
                });
                document.getElementById('lang-dialog').style.display = 'block';
            });
        });

        document.getElementById('close-lang').addEventListener('click', () => {
            document.getElementById('lang-dialog').style.display = 'none';
        });

        document.querySelectorAll('.lang-option').forEach(btn => {
            btn.addEventListener('click', (e) => {
                changeLanguage(e.target.getAttribute('data-lang'));
            });
        });
"""

# Inject changeLanguage near createTextMesh
content = content.replace("function createTextMesh", lang_logic + "\n        function createTextMesh")

# Inject listeners near help listeners
content = content.replace("        // Close the Help/Controls dialog", listener_logic + "\n        // Close the Help/Controls dialog")

with open('index.html', 'w') as f:
    f.write(content)
