import sys

with open('index.html', 'r') as f:
    content = f.read()

ray_old = """                const intersects = hoverRaycaster.intersectObjects(annMeshes, false);
                if (intersects.length > 0) {
                    hoveredMesh = intersects[0].object;
                }
            }"""

ray_new = """                const intersects = hoverRaycaster.intersectObjects(annMeshes, false);
                if (intersects.length > 0) {
                    hoveredMesh = intersects[0].object;
                }
                
                // Change mouse cursor to indicate clickability
                if (!isAuthoringMode) {
                    document.body.style.cursor = hoveredMesh ? 'pointer' : 'default';
                }
            }"""
            
content = content.replace(ray_old, ray_new)

with open('index.html', 'w') as f:
    f.write(content)
