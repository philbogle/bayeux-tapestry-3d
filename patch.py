import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update authoring panel HTML
html = re.sub(
    r'<!-- Authoring Panel -->.*?</div>',
    '''<!-- Authoring Panel -->
    <div id="authoring-panel" style="display: none; position: fixed; top: 20px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.85); color: white; padding: 20px; border: 2px solid #d6a848; z-index: 1000; font-family: monospace; max-width: 400px; text-align: center;">
        <h3 style="margin-top:0; color: #d6a848;">Text Authoring Mode</h3>
        <p style="color: #aaa; font-size: 12px; margin-bottom: 20px;"><em>Drag any text label to reposition it. Changes save locally.</em></p>
        <button id="auth-export" style="padding: 8px 12px; cursor: pointer;">Export JSON</button>
    </div>''',
    html,
    flags=re.DOTALL
)

# 2. Update authoring JS logic block
auth_logic_replacement = '''        // --- AUTHORING MODE LOGIC ---
        let tituliData = [];
        let isAuthoringMode = urlParams.get('author') === '1';

        if (isAuthoringMode) {
            document.getElementById('authoring-panel').style.display = 'block';
            
            document.getElementById('auth-export').addEventListener('click', () => {
                const exportData = annotations.map(a => a.data);
                console.log(JSON.stringify(exportData, null, 2));
                alert('Exported ' + exportData.length + ' scenes to console! See developer tools.');
            });
        }
        // ----------------------------'''

html = re.sub(
    r'// --- AUTHORING MODE LOGIC ---.*?// ----------------------------',
    auth_logic_replacement,
    html,
    flags=re.DOTALL
)

# 3. Add draggedAnnotation and dragRaycaster before mousedown
mousedown_str = '''        window.addEventListener('mousedown', (e) => {'''
mousedown_repl = '''        let draggedAnnotation = null;
        const dragRaycaster = new THREE.Raycaster();

        window.addEventListener('mousedown', (e) => {
            if (isTouch) return;
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#title') || e.target.closest('#lighting-dialog') || e.target.closest('#about-dialog')) return;
            
            if (isAuthoringMode) {
                mouseCoords.x = (e.clientX / window.innerWidth) * 2 - 1;
                mouseCoords.y = -(e.clientY / window.innerHeight) * 2 + 1;
                dragRaycaster.setFromCamera(mouseCoords, camera);
                const annMeshes = annotations.map(a => a.mesh).filter(m => m && m.visible);
                const intersects = dragRaycaster.intersectObjects(annMeshes, false);
                if (intersects.length > 0) {
                    draggedAnnotation = intersects[0].object.userData.annotation;
                    document.body.style.cursor = 'grabbing';
                    return; // Prevent camera panning
                }
            }'''
html = html.replace(
    '''        window.addEventListener('mousedown', (e) => {
            if (isTouch) return;
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#title') || e.target.closest('#lighting-dialog') || e.target.closest('#about-dialog')) return;''',
    mousedown_repl
)

# 4. update mouseup
html = html.replace(
    '''        window.addEventListener('mouseup', () => {
            if (!isTouch && isMouseDown) {''',
    '''        window.addEventListener('mouseup', () => {
            if (draggedAnnotation) {
                draggedAnnotation = null;
                document.body.style.cursor = 'default';
                localStorage.setItem('bayeux-tituli', JSON.stringify(annotations.map(a => a.data)));
                return;
            }
            if (!isTouch && isMouseDown) {'''
)

# 5. update mousemove
html = html.replace(
    '''        window.addEventListener('mousemove', (e) => {
            if (isTouch) return; 
            
            // Track normalized mouse coordinates for 3D hover raycasting
            mouseCoords.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouseCoords.y = -(e.clientY / window.innerHeight) * 2 + 1;
            
            if (isMouseDown) {''',
    '''        window.addEventListener('mousemove', (e) => {
            if (isTouch) return; 
            
            // Track normalized mouse coordinates for 3D hover raycasting
            mouseCoords.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouseCoords.y = -(e.clientY / window.innerHeight) * 2 + 1;
            
            if (draggedAnnotation) {
                dragRaycaster.setFromCamera(mouseCoords, camera);
                const intersects = dragRaycaster.intersectObjects(scene.children, true);
                if (intersects.length > 0) {
                    draggedAnnotation.data.x = intersects[0].point.x;
                    draggedAnnotation.data.y = intersects[0].point.y;
                    if (typeof updateAnnotations === 'function') updateAnnotations();
                }
                return;
            }
            
            if (isMouseDown) {'''
)

# 6. touchstart
html = html.replace(
    '''            if (e.touches.length === 1) {
                isDragging = true;''',
    '''            if (e.touches.length === 1) {
                if (isAuthoringMode) {
                    mouseCoords.x = (e.touches[0].clientX / window.innerWidth) * 2 - 1;
                    mouseCoords.y = -(e.touches[0].clientY / window.innerHeight) * 2 + 1;
                    dragRaycaster.setFromCamera(mouseCoords, camera);
                    const annMeshes = annotations.map(a => a.mesh).filter(m => m && m.visible);
                    const intersects = dragRaycaster.intersectObjects(annMeshes, false);
                    if (intersects.length > 0) {
                        draggedAnnotation = intersects[0].object.userData.annotation;
                        return; // Prevent panning
                    }
                }
                isDragging = true;'''
)

# 7. touchmove
html = html.replace(
    '''        window.addEventListener('touchmove', (e) => {
            if (!isTouch) return;
            
            if (e.touches.length === 1 && isDragging) {
                e.preventDefault(); // Prevent native browser scrolling/bounce''',
    '''        window.addEventListener('touchmove', (e) => {
            if (!isTouch) return;
            
            if (draggedAnnotation && e.touches.length === 1) {
                e.preventDefault();
                mouseCoords.x = (e.touches[0].clientX / window.innerWidth) * 2 - 1;
                mouseCoords.y = -(e.touches[0].clientY / window.innerHeight) * 2 + 1;
                dragRaycaster.setFromCamera(mouseCoords, camera);
                const intersects = dragRaycaster.intersectObjects(scene.children, true);
                if (intersects.length > 0) {
                    draggedAnnotation.data.x = intersects[0].point.x;
                    draggedAnnotation.data.y = intersects[0].point.y;
                    if (typeof updateAnnotations === 'function') updateAnnotations();
                }
                return;
            }

            if (e.touches.length === 1 && isDragging) {
                e.preventDefault(); // Prevent native browser scrolling/bounce'''
)

# 8. touchend
html = html.replace(
    '''        window.addEventListener('touchend', (e) => { 
            mouseScrollDir = 0; 
            if (e.touches.length < 2) {''',
    '''        window.addEventListener('touchend', (e) => { 
            if (draggedAnnotation) {
                draggedAnnotation = null;
                localStorage.setItem('bayeux-tituli', JSON.stringify(annotations.map(a => a.data)));
                return;
            }
            mouseScrollDir = 0; 
            if (e.touches.length < 2) {'''
)

# 9. Link mesh.userData.annotation
html = html.replace(
    '''                    const annObj = { data: t, mesh: mesh, isHovered: false, currentHover: 0 };
                    annotations.push(annObj);''',
    '''                    const annObj = { data: t, mesh: mesh, isHovered: false, currentHover: 0 };
                    mesh.userData.annotation = annObj;
                    annotations.push(annObj);'''
)

with open('index.html', 'w') as f:
    f.write(html)

print("Patch applied")
