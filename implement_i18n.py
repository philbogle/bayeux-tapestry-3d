import sys

with open('index.html', 'r') as f:
    content = f.read()

# 1. State
state_js = """        const SCALE = 100; // 100 pixels = 1 Three.js unit
        let currentLanguage = localStorage.getItem('bayeux_lang') || 'en';"""
content = content.replace("        const SCALE = 100; // 100 pixels = 1 Three.js unit", state_js)

# 2. createTextMesh updates
mesh_old = """        function createTextMesh(text, isPlaced) {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const fontSize = 80; // High-res font rendering
            ctx.font = `normal ${fontSize}px 'MedievalSharp', serif`;
            ctx.letterSpacing = '3px';
            const metrics = ctx.measureText(text.toUpperCase());
            canvas.width = Math.ceil(metrics.width) + 20;
            canvas.height = fontSize * 1.5;
            
            // Re-apply context styles after canvas resize clears them
            ctx.font = `normal ${fontSize}px 'MedievalSharp', serif`;
            ctx.letterSpacing = '3px';
            ctx.fillStyle = (!isPlaced && isAuthoringMode) ? '#aa0000' : '#5b5349';
            ctx.textBaseline = 'top';
            ctx.fillText(text.toUpperCase(), 10, 10);"""
mesh_new = """        function createTextMesh(text, isPlaced) {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const fontSize = 80; // High-res font rendering
            const fontStr = currentLanguage === 'zh' ? `normal ${fontSize}px serif` : `normal ${fontSize}px 'MedievalSharp', serif`;
            ctx.font = fontStr;
            ctx.letterSpacing = '3px';
            const renderText = currentLanguage === 'zh' ? text : text.toUpperCase();
            const metrics = ctx.measureText(renderText);
            canvas.width = Math.ceil(metrics.width) + 20;
            canvas.height = fontSize * 1.5;
            
            // Re-apply context styles after canvas resize clears them
            ctx.font = fontStr;
            ctx.letterSpacing = '3px';
            ctx.fillStyle = (!isPlaced && isAuthoringMode) ? '#aa0000' : '#5b5349';
            ctx.textBaseline = 'top';
            ctx.fillText(renderText, 10, 10);"""
content = content.replace(mesh_old, mesh_new)

# 3. Load Tituli array references
load_old = """            // Force the browser to download the custom font (since it's not used in standard DOM) before rendering
            document.fonts.load('80px "MedievalSharp"').then(() => {
                data.forEach(t => {
                    const mesh = createTextMesh(t.english, t.x !== undefined);"""
load_new = """            // Force the browser to download the custom font (since it's not used in standard DOM) before rendering
            document.fonts.load('80px "MedievalSharp"').then(() => {
                data.forEach(t => {
                    const textStr = (t.translations && t.translations[currentLanguage]) ? t.translations[currentLanguage].text : t.translations['en'].text;
                    const mesh = createTextMesh(textStr, t.x !== undefined);"""
content = content.replace(load_old, load_new)

# 4. Context Popup logic
context_old = """            document.getElementById('context-title').innerText = `"${annoData.english}"`;
            document.getElementById('context-title').style.fontStyle = 'italic';
            
            const contextText = (annoData.context) ? annoData.context : "No historical context available for this scene.";"""
context_new = """            const localizedText = (annoData.translations && annoData.translations[currentLanguage]) ? annoData.translations[currentLanguage].text : annoData.translations['en'].text;
            document.getElementById('context-title').innerText = `"${localizedText}"`;
            document.getElementById('context-title').style.fontStyle = 'italic';
            
            let contextText = "No historical context available for this scene.";
            if (annoData.translations && annoData.translations[currentLanguage] && annoData.translations[currentLanguage].context) {
                contextText = annoData.translations[currentLanguage].context;
            } else if (annoData.translations && annoData.translations['en'].context) {
                contextText = annoData.translations['en'].context;
            }"""
content = content.replace(context_old, context_new)

# 5. Authoring Mode UI
auth_old = """            <p style="margin: 0;"><strong>English:</strong> <span id="auth-english"></span></p>"""
auth_new = """            <p style="margin: 0;"><strong>English:</strong> <span id="auth-english"></span></p>"""
# wait auth update
auth_set_old = """                    document.getElementById('auth-english').innerText = activeAnn.data.english || '';"""
auth_set_new = """                    document.getElementById('auth-english').innerText = activeAnn.data.translations['en'].text || '';"""
content = content.replace(auth_set_old, auth_set_new)

with open('index.html', 'w') as f:
    f.write(content)
