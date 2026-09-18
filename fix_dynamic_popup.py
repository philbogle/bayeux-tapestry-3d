import sys

with open('index.html', 'r') as f:
    content = f.read()

# Modify updatePopupUI
ui_old = """        function updatePopupUI(index) {"""
ui_new = """        function updatePopupUI(index, shouldAutoScroll = true) {"""
content = content.replace(ui_old, ui_new)

scroll_old = """            if (annoData.x !== undefined) {
                // Find the mesh to calculate its width so we can center on it perfectly
                const annObj = annotations.find(a => a.data === annoData);
                if (annObj && annObj.mesh) {
                    const width = annObj.mesh.geometry.parameters.width;
                    autoScrollTargetX = annoData.x + (width / 2.0);
                } else {
                    autoScrollTargetX = annoData.x;
                }
            }"""
scroll_new = """            if (shouldAutoScroll && annoData.x !== undefined) {
                // Find the mesh to calculate its width so we can center on it perfectly
                const annObj = annotations.find(a => a.data === annoData);
                if (annObj && annObj.mesh) {
                    const width = annObj.mesh.geometry.parameters.width;
                    autoScrollTargetX = annoData.x + (width / 2.0);
                } else {
                    autoScrollTargetX = annoData.x;
                }
            }"""
content = content.replace(scroll_old, scroll_new)

# Add updateDynamicPopup inside animate
anim_old = """        function animate() {
            requestAnimationFrame(animate);"""
anim_new = """        function updateDynamicPopup() {
            const popup = document.getElementById('context-scroll');
            if (!popup || popup.style.display === 'none') return;
            if (autoScrollTargetX !== null) return; // Don't interfere with auto-scrolling
            
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
            
            if (closestIndex !== -1 && closestIndex !== currentPopupSceneIndex) {
                // Only update if it's reasonably close to the center of the screen (within 10 units of distance)
                // This prevents the popup from jumping to a scene that is completely off-screen
                if (minDistance < 8.0) {
                    updatePopupUI(closestIndex, false);
                }
            }
        }

        function animate() {
            requestAnimationFrame(animate);
            updateDynamicPopup();"""
content = content.replace(anim_old, anim_new)

with open('index.html', 'w') as f:
    f.write(content)
