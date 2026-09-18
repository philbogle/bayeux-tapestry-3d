import sys

with open('index.html', 'r') as f:
    content = f.read()

# 1. Add handleAnnotationClick function and remove the faulty window click listener
remove_click_old = """        // Handle clicking on annotations to show context
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
        });"""

helper_function = """        function handleAnnotationClick(clientX, clientY, target) {
            if (target && (target.closest('#ui') || target.closest('#authoring-panel') || target.closest('#about-dialog') || target.closest('#lighting-dialog') || target.closest('#help-dialog') || target.closest('#context-scroll'))) return;
            
            mouseCoords.x = (clientX / window.innerWidth) * 2 - 1;
            mouseCoords.y = -(clientY / window.innerHeight) * 2 + 1;
            dragRaycaster.setFromCamera(mouseCoords, camera);
            
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
        }"""
content = content.replace(remove_click_old, helper_function)


# 2. Add hasTouchDragged
touchstart_old = """        // Initialize touch tracking, halt any existing momentum, and handle raycasting for Authoring mode drags.
        window.addEventListener('touchstart', (e) => { 
            isTouch = true; """
touchstart_new = """        let hasTouchDragged = false;
        
        // Initialize touch tracking, halt any existing momentum, and handle raycasting for Authoring mode drags.
        window.addEventListener('touchstart', (e) => { 
            isTouch = true; 
            hasTouchDragged = false;"""
content = content.replace(touchstart_old, touchstart_new)


touchmove_old = """        window.addEventListener('touchmove', (e) => { 
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#about-dialog') || e.target.closest('#lighting-dialog')) return;
            if (draggedAnnotation) {"""
touchmove_new = """        window.addEventListener('touchmove', (e) => { 
            hasTouchDragged = true;
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#about-dialog') || e.target.closest('#lighting-dialog')) return;
            if (draggedAnnotation) {"""
content = content.replace(touchmove_old, touchmove_new)


touchend_old = """            if (e.touches.length === 0) {
                isDragging = false;
            }
        });"""
touchend_new = """            if (e.touches.length === 0) {
                isDragging = false;
                if (!hasTouchDragged && e.changedTouches.length > 0) {
                    handleAnnotationClick(e.changedTouches[0].clientX, e.changedTouches[0].clientY, e.target);
                }
            }
        });"""
content = content.replace(touchend_old, touchend_new)


# 3. Update mouseup
mouseup_old = """        // Reset mouse dragging state when the mouse button is released anywhere on screen
        window.addEventListener('mouseup', () => {
            if (draggedAnnotation) {
                draggedAnnotation = null;
                document.body.style.cursor = 'default';
                localStorage.setItem('bayeux-tituli', JSON.stringify(annotations.map(a => a.data)));
                return;
            }
            if (!isTouch && isMouseDown) {
                isMouseDown = false;
                document.body.style.cursor = 'default';
            }
        });"""
mouseup_new = """        // Reset mouse dragging state when the mouse button is released anywhere on screen
        window.addEventListener('mouseup', (e) => {
            if (draggedAnnotation) {
                draggedAnnotation = null;
                document.body.style.cursor = 'default';
                localStorage.setItem('bayeux-tituli', JSON.stringify(annotations.map(a => a.data)));
                return;
            }
            if (!isTouch && isMouseDown) {
                isMouseDown = false;
                document.body.style.cursor = 'default';
                if (!isMouseDragging) {
                    handleAnnotationClick(e.clientX, e.clientY, e.target);
                }
            }
        });"""
content = content.replace(mouseup_old, mouseup_new)

with open('index.html', 'w') as f:
    f.write(content)
