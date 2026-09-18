import sys

with open('index.html', 'r') as f:
    content = f.read()

mob_old = """                    <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                        <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                        Titles
                    </label>"""
mob_new = """                    <button id="toggle-supertitles" style="pointer-events: auto; background: rgba(214,168,72,0.3); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">T Titles</button>"""
content = content.replace(mob_old, mob_new)


# Titles JS
title_old = """            // Toggle the visibility of all loaded English text meshes
            const toggleSupertitles = document.getElementById('toggle-supertitles');
            if (toggleSupertitles) {
                toggleSupertitles.addEventListener('change', (e) => {
                    showSupertitles = e.target.checked;
                    const container = document.getElementById('annotations-container');
                    if (container) {
                        container.style.display = e.target.checked ? 'block' : 'none';
                    }
                });
            }"""

title_new = """            // Toggle the visibility of all loaded English text meshes
            const toggleSupertitles = document.getElementById('toggle-supertitles');
            if (toggleSupertitles) {
                toggleSupertitles.addEventListener('click', (e) => {
                    e.preventDefault();
                    showSupertitles = !showSupertitles;
                    toggleSupertitles.style.background = showSupertitles ? 'rgba(214,168,72,0.3)' : 'rgba(20,20,20,0.8)';
                    const container = document.getElementById('annotations-container');
                    if (container) {
                        container.style.display = showSupertitles ? 'block' : 'none';
                    }
                });
            }"""
content = content.replace(title_old, title_new)

# Notes JS
notes_old = """        const notesBtn = document.getElementById('notes-btn');
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
        }"""

notes_new = """        const notesBtn = document.getElementById('notes-btn');
        if (notesBtn) {
            notesBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const popup = document.getElementById('context-scroll');
                
                // Toggle logic
                if (popup && popup.style.display !== 'none') {
                    popup.style.display = 'none';
                    notesBtn.style.background = 'rgba(20,20,20,0.8)';
                    return;
                }
                
                notesBtn.style.background = 'rgba(214,168,72,0.3)';
                
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
        }"""
content = content.replace(notes_old, notes_new)

# Update notes background when closed manually
close_old = """        // Close the Context popup
        document.getElementById('close-context').addEventListener('click', () => {
            document.getElementById('context-scroll').style.display = 'none';
        });"""

close_new = """        // Close the Context popup
        document.getElementById('close-context').addEventListener('click', () => {
            document.getElementById('context-scroll').style.display = 'none';
            const btn = document.getElementById('notes-btn');
            if (btn) btn.style.background = 'rgba(20,20,20,0.8)';
        });"""
content = content.replace(close_old, close_new)

with open('index.html', 'w') as f:
    f.write(content)
