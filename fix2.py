import sys

with open('index.html', 'r') as f:
    content = f.read()

# 1. Mousemove
mousemove_old = """            // Normalized Device Coordinates (-1 to +1) required by Three.js Raycaster to map 2D screen touches into the 3D scene
            mouseCoords.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouseCoords.y = -(e.clientY / window.innerHeight) * 2 + 1;"""
            
mousemove_new = """            // Normalized Device Coordinates (-1 to +1) required by Three.js Raycaster to map 2D screen touches into the 3D scene
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


# 2. updateTiles definition
updateTiles_old = """            // The margin acts as an off-screen buffer, forcing tiles to load just outside the camera's field of view
            const margin = isPhone ? 20 : 60; // Much larger buffer for desktop to prevent pop-in during fast scrolls"""

updateTiles_new = """            // The margin acts as an off-screen buffer, forcing tiles to load just outside the camera's field of view
            const margin = isPhone ? 20 : 60; // Much larger buffer for desktop to prevent pop-in during fast scrolls
            
            let magMinX = 0, magMaxX = 0;
            if (magActive) {
                const magVisibleHeight = 2 * Math.tan(vFOV / 2) * magCamera.position.z;
                const magVisibleWidth = magVisibleHeight * magCamera.aspect;
                magMinX = magCamera.position.x - magVisibleWidth / 2;
                magMaxX = magCamera.position.x + magVisibleWidth / 2;
            }"""
content = content.replace(updateTiles_old, updateTiles_new)


# 3. animate loop renderTarget update (the previous script failed on this because of missing code maybe?)
animate_old = """            updateCamera();
            updateTiles();"""
animate_new = """            updateCamera();
            updateTiles();
            
            if (magActive) {
                renderer.setRenderTarget(magRenderTarget);
                renderer.render(scene, magCamera);
                renderer.setRenderTarget(null);
            }"""
content = content.replace(animate_old, animate_new)

with open('index.html', 'w') as f:
    f.write(content)
