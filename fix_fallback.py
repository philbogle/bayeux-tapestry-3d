import sys

with open('index.html', 'r') as f:
    content = f.read()

func_old = """        function handleAnnotationClick(clientX, clientY, target) {
            console.log('handleAnnotationClick triggered at', clientX, clientY);
            if (target && target.closest && (target.closest('#ui') || target.closest('#authoring-panel') || target.closest('#about-dialog') || target.closest('#lighting-dialog') || target.closest('#help-dialog') || target.closest('#context-scroll'))) {
                console.log('Click ignored due to UI target');
                return;
            }
            
            mouseCoords.x = (clientX / window.innerWidth) * 2 - 1;
            mouseCoords.y = -(clientY / window.innerHeight) * 2 + 1;
            dragRaycaster.setFromCamera(mouseCoords, camera);
            
            // Only raycast against annotations that actually have a 'context' field
            const contextMeshes = annotations.filter(a => a.data.context).map(a => a.mesh).filter(m => m && m.visible);
            console.log('Context meshes available to click:', contextMeshes.length);
            
            const intersects = dragRaycaster.intersectObjects(contextMeshes, false);
            console.log('Intersections:', intersects.length);
            
            if (intersects.length > 0) {
                const clickedMesh = intersects[0].object;
                const annoData = clickedMesh.userData.annotation;
                
                document.getElementById('context-text').innerText = annoData.context;
                document.getElementById('context-title').innerText = "Scene Context";
                document.getElementById('context-scroll').style.display = 'block';
                console.log('Popup displayed!');
            }
        }"""
        
func_new = """        function handleAnnotationClick(clientX, clientY, target) {
            if (target && target.closest && (target.closest('#ui') || target.closest('#authoring-panel') || target.closest('#about-dialog') || target.closest('#lighting-dialog') || target.closest('#help-dialog') || target.closest('#context-scroll'))) {
                return;
            }
            
            mouseCoords.x = (clientX / window.innerWidth) * 2 - 1;
            mouseCoords.y = -(clientY / window.innerHeight) * 2 + 1;
            dragRaycaster.setFromCamera(mouseCoords, camera);
            
            // Raycast against all visible annotations
            const annMeshes = annotations.map(a => a.mesh).filter(m => m && m.visible);
            
            const intersects = dragRaycaster.intersectObjects(annMeshes, false);
            
            if (intersects.length > 0) {
                const clickedMesh = intersects[0].object;
                const annoData = clickedMesh.userData.annotation;
                
                const contextText = (annoData && annoData.context) ? annoData.context : "No historical context has been added for this scene yet. (Pending translation/context update)";
                document.getElementById('context-text').innerText = contextText;
                document.getElementById('context-title').innerText = "Scene Context";
                document.getElementById('context-scroll').style.display = 'block';
            }
        }"""
content = content.replace(func_old, func_new)

with open('index.html', 'w') as f:
    f.write(content)
