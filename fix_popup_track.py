import sys

with open('index.html', 'r') as f:
    content = f.read()

anim_old = """        function animate() {
            requestAnimationFrame(animate);"""

anim_new = """        function updatePopupPosition() {
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

content = content.replace(anim_old, anim_new)

with open('index.html', 'w') as f:
    f.write(content)
