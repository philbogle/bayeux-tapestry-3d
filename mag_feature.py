import sys

with open('index.html', 'r') as f:
    content = f.read()

# 1. HTML button
btn_html = '                <button id="mag-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">🔍 Magnifier</button>\n'
content = content.replace('                <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">\n                Titles\n            </label>\n', 
                          '                <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">\n                Titles\n            </label>\n' + btn_html)

# 2. Camera Setup
mag_setup = """        // Magnifying Glass Setup
        let magActive = false;
        const magRenderTarget = new THREE.WebGLRenderTarget(512, 512);
        const magCamera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
        magCamera.position.z = 2.5; // Zoomed in tight for maximum detail
        
        const uiScene = new THREE.Scene();
        const uiCamera = new THREE.OrthographicCamera(window.innerWidth / -2, window.innerWidth / 2, window.innerHeight / 2, window.innerHeight / -2, 1, 10);
        uiCamera.position.z = 5;
        
        const lensGeo = new THREE.CircleGeometry(150, 64);
        const lensMat = new THREE.MeshBasicMaterial({ map: magRenderTarget.texture });
        const lensMesh = new THREE.Mesh(lensGeo, lensMat);
        
        const lensBorderGeo = new THREE.RingGeometry(150, 153, 64);
        const lensBorderMat = new THREE.MeshBasicMaterial({ color: 0xd6a848 });
        const lensBorder = new THREE.Mesh(lensBorderGeo, lensBorderMat);
        
        lensMesh.add(lensBorder);
        lensMesh.position.set(-9999, -9999, 0);
        uiScene.add(lensMesh);
"""
content = content.replace("        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);",
                          "        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);\n" + mag_setup)

# 3. Mousemove update
mousemove_old = """        window.addEventListener('mousemove', (e) => {
            if (isTouch) return; 
            
            // Normalize mouse coordinates for raycasting
            mouseCoords.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouseCoords.y = -(e.clientY / window.innerHeight) * 2 + 1;"""

mousemove_new = """        window.addEventListener('mousemove', (e) => {
            if (isTouch) return; 
            
            // Normalize mouse coordinates for raycasting
            mouseCoords.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouseCoords.y = -(e.clientY / window.innerHeight) * 2 + 1;
            
            // Update magnifying glass position and camera
            if (magActive) {
                lensMesh.position.x = e.clientX - window.innerWidth / 2;
                lensMesh.position.y = - (e.clientY - window.innerHeight / 2);
                
                dragRaycaster.setFromCamera(mouseCoords, camera);
                const planeZ0 = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
                const target = new THREE.Vector3();
                if (dragRaycaster.ray.intersectPlane(planeZ0, target)) {
                    magCamera.position.x = target.x;
                    magCamera.position.y = target.y;
                }
            }"""
content = content.replace(mousemove_old, mousemove_new)

# 4. Resize update
resize_old = """            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);"""
resize_new = """            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            uiCamera.left = window.innerWidth / -2;
            uiCamera.right = window.innerWidth / 2;
            uiCamera.top = window.innerHeight / 2;
            uiCamera.bottom = window.innerHeight / -2;
            uiCamera.updateProjectionMatrix();"""
content = content.replace(resize_old, resize_new)

# 5. updateTiles logic
updateTiles_old = """            const minX = camera.position.x - visibleWidth / 2;
            const maxX = camera.position.x + visibleWidth / 2;"""
updateTiles_new = """            const minX = camera.position.x - visibleWidth / 2;
            const maxX = camera.position.x + visibleWidth / 2;
            
            let magMinX = 0, magMaxX = 0;
            if (magActive) {
                const magVisibleHeight = 2 * Math.tan(vFOV / 2) * magCamera.position.z;
                const magVisibleWidth = magVisibleHeight * magCamera.aspect;
                magMinX = magCamera.position.x - magVisibleWidth / 2;
                magMaxX = magCamera.position.x + magVisibleWidth / 2;
            }"""
content = content.replace(updateTiles_old, updateTiles_new)

processTiles_old = """                    const inMainView = (tileRight >= minX - margin) && (tileLeft <= maxX + margin);
                    
                    if (inMainView) {"""
processTiles_new = """                    const inMainView = (tileRight >= minX - margin) && (tileLeft <= maxX + margin);
                    const inMagView = magActive && isHighRes && (tileRight >= magMinX - margin) && (tileLeft <= magMaxX + margin);
                    
                    if (inMainView || inMagView) {"""
content = content.replace(processTiles_old, processTiles_new)

# 6. animate loop logic
animate_old = """        function animate() {
            requestAnimationFrame(animate);

            updateCamera();"""
animate_new = """        function animate() {
            requestAnimationFrame(animate);

            updateCamera();
            
            if (magActive) {
                renderer.setRenderTarget(magRenderTarget);
                renderer.render(scene, magCamera);
                renderer.setRenderTarget(null);
            }"""
content = content.replace(animate_old, animate_new)

render_old = "            renderer.render(scene, camera);"
render_new = """            renderer.render(scene, camera);
            if (magActive) {
                renderer.autoClear = false;
                renderer.clearDepth();
                renderer.render(uiScene, uiCamera);
                renderer.autoClear = true;
            }"""
content = content.replace(render_old, render_new)

# 7. Listeners for M key and button
listeners_old = """        // Handle keyboard navigation (arrow keys/WASD) and prevent default scrolling behavior.
        window.addEventListener('keydown', (e) => {"""
listeners_new = """        const magToggleBtn = document.getElementById('mag-toggle');
        if (magToggleBtn) {
            magToggleBtn.addEventListener('click', () => {
                magActive = !magActive;
                magToggleBtn.style.background = magActive ? 'rgba(214,168,72,0.3)' : 'rgba(20,20,20,0.8)';
                if (!magActive) lensMesh.position.set(-9999, -9999, 0);
            });
        }
        
        // Handle keyboard navigation (arrow keys/WASD) and prevent default scrolling behavior.
        window.addEventListener('keydown', (e) => {
            if (e.key.toLowerCase() === 'm' && !isPhone) {
                magActive = !magActive;
                if (magToggleBtn) magToggleBtn.style.background = magActive ? 'rgba(214,168,72,0.3)' : 'rgba(20,20,20,0.8)';
                if (!magActive) lensMesh.position.set(-9999, -9999, 0);
            }"""
content = content.replace(listeners_old, listeners_new)

with open('index.html', 'w') as f:
    f.write(content)
