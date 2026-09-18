import re

with open('index.html', 'r') as f:
    content = f.read()

replacements = [
    # Lighting UI Listeners
    (r"document\.getElementById\('amb-int'\)\.addEventListener", 
     r"// Update ambient light intensity in real-time from the lighting dev panel\n        document.getElementById('amb-int').addEventListener"),
    
    (r"document\.getElementById\('amb-color'\)\.addEventListener", 
     r"// Update ambient light color in real-time from the lighting dev panel\n        document.getElementById('amb-color').addEventListener"),
     
    (r"document\.getElementById\('torch-int'\)\.addEventListener", 
     r"// Update dynamic torch light intensity in real-time from the lighting dev panel\n        document.getElementById('torch-int').addEventListener"),
     
    (r"document\.getElementById\('torch-color'\)\.addEventListener", 
     r"// Update dynamic torch light color in real-time from the lighting dev panel\n        document.getElementById('torch-color').addEventListener"),

    # Window edge-case listeners
    (r"window\.addEventListener\('touchcancel'", 
     r"// Reset touch states if the browser cancels the touch event (e.g., system swipe gesture)\n        window.addEventListener('touchcancel'"),
     
    (r"window\.addEventListener\('mouseup',\s*\(\)\s*=>\s*\{\s*if\s*\(!isTouch\)\s*isMouseDown\s*=\s*false;\s*\}\);", 
     r"// Reset mouse dragging state when the mouse button is released anywhere on screen\n        window.addEventListener('mouseup', () => { if (!isTouch) isMouseDown = false; });"),
     
    (r"window\.addEventListener\('mouseleave',\s*\(\)\s*=>\s*\{\s*if\s*\(!isTouch\)\s*isMouseDown\s*=\s*false;\s*\}\);", 
     r"// Reset mouse dragging state if the cursor leaves the browser window entirely\n        window.addEventListener('mouseleave', () => { if (!isTouch) isMouseDown = false; });"),
     
    (r"window\.addEventListener\('mouseout',\s*\(e\)\s*=>\s*\{", 
     r"// Halt edge-scrolling if the mouse leaves the viewport completely\n        window.addEventListener('mouseout', (e) => {"),
     
    (r"window\.addEventListener\('mouseleave',\s*\(\)\s*=>\s*\{\s*mouseScrollDir\s*=\s*0;\s*\}\);", 
     r"// Fallback to halt edge-scrolling if mouseleave fires on the window\n        window.addEventListener('mouseleave', () => { mouseScrollDir = 0; });"),

    # Nav Button listeners (inside bindNavButton)
    (r"btn\.addEventListener\('mousedown',\s*start\);", 
     r"// Bind mouse/touch events to trigger the directional navigation impulse\n            btn.addEventListener('mousedown', start);"),

    # UI Checkbox
    (r"toggleSupertitles\.addEventListener\('change'", 
     r"// Toggle the visibility of all loaded English text meshes\n            toggleSupertitles.addEventListener('change'"),
     
    # Dialog listeners
    (r"link\.addEventListener\('click',\s*\(e\)\s*=>\s*\{\s*e\.preventDefault\(\);\s*document\.getElementById\('about-dialog'\)\.style\.display\s*=\s*'block';\s*\}\);", 
     r"// Open the About dialog when the top navigation link is clicked\n            link.addEventListener('click', (e) => { e.preventDefault(); document.getElementById('about-dialog').style.display = 'block'; });"),
     
    (r"link\.addEventListener\('click',\s*\(e\)\s*=>\s*\{\s*e\.preventDefault\(\);\s*document\.getElementById\('help-dialog'\)\.style\.display\s*=\s*'block';\s*\}\);", 
     r"// Open the Help/Controls dialog when the top navigation link is clicked\n            link.addEventListener('click', (e) => { e.preventDefault(); document.getElementById('help-dialog').style.display = 'block'; });"),
     
    (r"document\.getElementById\('close-dialog'\)\.addEventListener\('click'", 
     r"// Close the About dialog\n        document.getElementById('close-dialog').addEventListener('click'"),
     
    (r"document\.getElementById\('close-help'\)\.addEventListener\('click'", 
     r"// Close the Help/Controls dialog\n        document.getElementById('close-help').addEventListener('click'"),
     
    # Authoring Export
    (r"document\.getElementById\('auth-export'\)\.addEventListener\('click'", 
     r"// Export the current layout of 3D text meshes to the console as formatted JSON\n            document.getElementById('auth-export').addEventListener('click'"),
     
    # More UI
    (r"document\.getElementById\('lighting-controls-link'\)\.addEventListener\('click'", 
     r"// Open the hidden lighting configuration dialog\n        document.getElementById('lighting-controls-link').addEventListener('click'"),
     
    (r"document\.getElementById\('close-lighting'\)\.addEventListener\('click'", 
     r"// Close the hidden lighting configuration dialog\n        document.getElementById('close-lighting').addEventListener('click'"),
     
    (r"document\.getElementById\('music-toggle'\)\.addEventListener\('click'", 
     r"// Toggle the background YouTube audio player state between play and pause\n        document.getElementById('music-toggle').addEventListener('click'"),
]

for old, new in replacements:
    content = re.sub(old, new, content)

with open('index.html', 'w') as f:
    f.write(content)
