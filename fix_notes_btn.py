import sys

with open('index.html', 'r') as f:
    content = f.read()

# Desktop UI
desk_old = """            <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                Titles
            </label>"""
desk_new = """            <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                Titles
            </label>
            <button id="notes-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">📝 Notes</button>"""
content = content.replace(desk_old, desk_new)

# Mobile UI
mob_old = """                    <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                        <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                        Titles
                    </label>"""
mob_new = """                    <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                        <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                        Titles
                    </label>
                    <button id="notes-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">📝 Notes</button>"""
content = content.replace(mob_old, mob_new)

# Add event listener
listener_js = """
        const notesBtn = document.getElementById('notes-btn');
        if (notesBtn) {
            notesBtn.addEventListener('click', (e) => {
                e.preventDefault();
                let closestIndex = -1;
                let minDistance = Infinity;
                
                for (let i = 0; i < annotations.length; i++) {
                    const ann = annotations[i];
                    if (!ann || !ann.mesh || !ann.data) continue;
                    
                    const width = ann.mesh.geometry.parameters.width;
                    const centerPoint = ann.data.x + width / 2.0;
                    
                    const dist = Math.abs(camera.position.x - centerPoint);
                    if (dist < minDistance) {
                        minDistance = dist;
                        closestIndex = tituliData.indexOf(ann.data);
                    }
                }
                
                if (closestIndex !== -1) {
                    updatePopupUI(closestIndex, true);
                }
            });
        }
"""
# Insert before "document.querySelectorAll('#learn-more-link').forEach"
content = content.replace("document.querySelectorAll('#learn-more-link').forEach", listener_js + "\n        document.querySelectorAll('#learn-more-link').forEach")

with open('index.html', 'w') as f:
    f.write(content)
