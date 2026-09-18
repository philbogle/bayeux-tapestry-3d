import sys

with open('index.html', 'r') as f:
    content = f.read()

old_block = """            // LOD Tile Manager: Evaluates which tiles intersect the camera frustum and handles async texture loading/unloading to preserve memory
            const processTiles = (tileArray, levelStr, isHighRes, unloadZ) => {
                // If it's a high-res layer and we're zoomed out, aggressively unload everything
                if (isHighRes && camera.position.z > unloadZ && (!magActive || magCamera.position.z > unloadZ)) {
                    for (let tile of tileArray) {
                        if (tile.loaded && tile.mesh.material !== emptyMaterial) {
                            if (tile.mesh.material.map) tile.mesh.material.map.dispose();
                            tile.mesh.material.dispose();
                            tile.mesh.material = emptyMaterial;
                            tile.loaded = false;
                            tile.loading = false;
                        }
                    }
                    return;
                }
                
                // For high-res tiles, we use a tighter margin so we don't spam requests for tiles slightly off screen"""

new_block = """            // LOD Tile Manager: Evaluates which tiles intersect the camera frustum and handles async texture loading/unloading to preserve memory
            const processTiles = (tileArray, levelStr, isHighRes, unloadZ) => {
                // For high-res tiles, we use a tighter margin so we don't spam requests for tiles slightly off screen"""

content = content.replace(old_block, new_block)

with open('index.html', 'w') as f:
    f.write(content)
