import sys

with open('index.html', 'r') as f:
    content = f.read()

# Revert animate() tracking
anim_old = """        function updatePopupPosition() {
            const popup = document.getElementById('context-scroll');
            if (!popup || popup.style.display === 'none') return;
            
            const annoData = tituliData[currentPopupSceneIndex];
            if (!annoData || annoData.x === undefined) return;
            
            const vec = new THREE.Vector3(annoData.x, 0, 0);
            vec.project(camera);
            
            const leftPx = (vec.x * 0.5 + 0.5) * window.innerWidth;
            
            // Keep it from sliding completely off-screen by clamping it?
            // Actually, letting it slide off-screen is perfectly intuitive. 
            // However, we should clamp it so the Close button remains accessible if they want to dismiss it?
            // Let's clamp it to at least half its width from the edges so it stays visible
            const minX = 210; // half of 420px width
            const maxX = window.innerWidth - 210;
            const clampedLeft = Math.max(minX, Math.min(maxX, leftPx));
            
            popup.style.left = clampedLeft + 'px';
            popup.style.transform = 'translateX(-50%)';
        }

        function animate() {
            requestAnimationFrame(animate);
            updatePopupPosition();"""

anim_new = """        function animate() {
            requestAnimationFrame(animate);"""

content = content.replace(anim_old, anim_new)

# Restore popup static left:50%
# Actually, the inline style is still `left: 50%; transform: translateX(-50%);` from HTML, 
# so I don't need to change the HTML if I just restore it when displaying it.
# Let's fix updatePopupUI to reset its CSS to left:50% when opened!
ui_old = """            document.getElementById('next-scene').style.pointerEvents = (index === tituliData.length - 1) ? 'none' : 'auto';
            
            document.getElementById('context-scroll').style.display = 'block';
            
            if (annoData.x !== undefined) {
                autoScrollTargetX = annoData.x;
            }
        }"""

ui_new = """            document.getElementById('next-scene').style.pointerEvents = (index === tituliData.length - 1) ? 'none' : 'auto';
            
            // Restore static center positioning
            const popup = document.getElementById('context-scroll');
            popup.style.left = '50%';
            popup.style.transform = 'translateX(-50%)';
            popup.style.display = 'block';
            
            if (annoData.x !== undefined) {
                // Find the mesh to calculate its width so we can center on it perfectly
                const annObj = annotations.find(a => a.data === annoData);
                if (annObj && annObj.mesh) {
                    const width = annObj.mesh.geometry.parameters.width;
                    autoScrollTargetX = annoData.x + (width / 2.0);
                } else {
                    autoScrollTargetX = annoData.x;
                }
            }
        }"""
        
content = content.replace(ui_old, ui_new)

with open('index.html', 'w') as f:
    f.write(content)
