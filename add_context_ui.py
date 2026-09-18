import sys

with open('index.html', 'r') as f:
    content = f.read()

# 1. Add HTML UI
lighting_dialog_end = """        <label>Ambient Intensity: <span id="val-amb-int">1.03</span></label><br>
        <input type="range" id="amb-int" min="0" max="2" step="0.01" value="1.03" style="width: 100%; margin-bottom: 10px;"><br>
        <label>Directional Intensity: <span id="val-dir-int">0.78</span></label><br>
        <input type="range" id="dir-int" min="0" max="2" step="0.01" value="0.78" style="width: 100%; margin-bottom: 10px;"><br>
        <label>Directional Tilt (Y): <span id="val-dir-y">10</span></label><br>
        <input type="range" id="dir-y" min="-50" max="50" step="1" value="10" style="width: 100%; margin-bottom: 10px;"><br>
        <label>Directional Depth (Z): <span id="val-dir-z">20</span></label><br>
        <input type="range" id="dir-z" min="0" max="100" step="1" value="20" style="width: 100%; margin-bottom: 20px;"><br>
        <div style="text-align: right;">
            <button id="close-lighting" style="padding: 5px 15px; background: #5a4a35; color: white; border: none; border-radius: 4px; cursor: pointer;">Close</button>
        </div>
    </div>"""

context_scroll_html = """
    <div id="context-scroll" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #f4e4bc; color: #3a2a1a; padding: 40px; border-radius: 4px; border: 2px solid #8b7355; z-index: 2000; max-width: 500px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 40px rgba(139, 115, 85, 0.2); font-family: 'MedievalSharp', serif;">
        <h3 id="context-title" style="margin-top: 0; font-size: 22px; border-bottom: 1px solid #8b7355; padding-bottom: 10px;">Scene Context</h3>
        <p id="context-text" style="font-size: 16px; line-height: 1.6; text-align: left; font-family: serif;"></p>
        <button id="close-context" style="margin-top: 20px; padding: 8px 20px; background: #8b7355; color: #f4e4bc; border: none; border-radius: 4px; cursor: pointer; font-family: 'MedievalSharp', serif; font-size: 16px;">Close</button>
    </div>"""

content = content.replace(lighting_dialog_end, lighting_dialog_end + context_scroll_html)

# 2. Add JS logic
js_additions_old = """        // Close the Help/Controls dialog
        document.getElementById('close-help').addEventListener('click', () => {
            document.getElementById('help-dialog').style.display = 'none';
        });"""
js_additions_new = """        // Close the Help/Controls dialog
        document.getElementById('close-help').addEventListener('click', () => {
            document.getElementById('help-dialog').style.display = 'none';
        });

        // Close the Context popup
        document.getElementById('close-context').addEventListener('click', () => {
            document.getElementById('context-scroll').style.display = 'none';
        });"""
content = content.replace(js_additions_old, js_additions_new)


# 3. Add dragging tracker and click listener
mousedown_old = """        window.addEventListener('mousedown', (e) => {
            if (isTouch) return;
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#title') || e.target.closest('#lighting-dialog') || e.target.closest('#about-dialog')) return;"""
mousedown_new = """        let isMouseDragging = false;
        
        window.addEventListener('mousedown', (e) => {
            if (isTouch) return;
            isMouseDragging = false;
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#title') || e.target.closest('#lighting-dialog') || e.target.closest('#about-dialog') || e.target.closest('#context-scroll')) return;"""
content = content.replace(mousedown_old, mousedown_new)


mousemove_old = """        window.addEventListener('mousemove', (e) => {
            if (isTouch) return; 
            
            // Update magnifying glass position and camera"""
mousemove_new = """        window.addEventListener('mousemove', (e) => {
            if (isTouch) return; 
            if (isMouseDown) isMouseDragging = true;
            
            // Update magnifying glass position and camera"""
content = content.replace(mousemove_old, mousemove_new)


click_listener = """
        // Handle clicking on annotations to show context
        window.addEventListener('click', (e) => {
            if (isMouseDragging || isDragging) return; // Prevent triggering after a pan
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#about-dialog') || e.target.closest('#lighting-dialog') || e.target.closest('#help-dialog') || e.target.closest('#context-scroll')) return;
            
            // Get click coordinates in normalized device space
            let clickX, clickY;
            if (e.clientX !== undefined) {
                clickX = (e.clientX / window.innerWidth) * 2 - 1;
                clickY = -(e.clientY / window.innerHeight) * 2 + 1;
            } else if (e.changedTouches && e.changedTouches.length > 0) {
                clickX = (e.changedTouches[0].clientX / window.innerWidth) * 2 - 1;
                clickY = -(e.changedTouches[0].clientY / window.innerHeight) * 2 + 1;
            } else {
                return;
            }
            
            dragRaycaster.setFromCamera(new THREE.Vector2(clickX, clickY), camera);
            
            // Only raycast against annotations that actually have a 'context' field
            const contextMeshes = annotations.filter(a => a.data.context).map(a => a.mesh).filter(m => m && m.visible);
            
            const intersects = dragRaycaster.intersectObjects(contextMeshes, false);
            if (intersects.length > 0) {
                const clickedMesh = intersects[0].object;
                const annoData = clickedMesh.userData.annotation;
                
                document.getElementById('context-text').innerText = annoData.context;
                document.getElementById('context-title').innerText = "Scene Context";
                document.getElementById('context-scroll').style.display = 'block';
            }
        });
"""

# Insert click listener before `window.addEventListener('wheel'`
wheel_old = """        let lastWheelTime = 0;
        // Handle trackpad / mouse wheel zooming and horizontal panning."""
wheel_new = click_listener + """        let lastWheelTime = 0;
        // Handle trackpad / mouse wheel zooming and horizontal panning."""
content = content.replace(wheel_old, wheel_new)

with open('index.html', 'w') as f:
    f.write(content)
