import sys

with open('index.html', 'r') as f:
    content = f.read()

loop_old = """                for (let tile of tileArray) {
                    const isMainVisible = (tile.xCenter >= minX && tile.xCenter <= maxX);
                    const isMagVisible = magActive && isHighRes && (tile.xCenter >= magMinX - actualMargin && tile.xCenter <= magMaxX + actualMargin);
                    const isVisible = isMainVisible || isMagVisible;
                    
                    if (isVisible) {
                        const canLoadNewTile = !isHighRes || (smoothedCameraSpeed < 0.015);

                        if (canLoadNewTile && !tile.loaded && !tile.loading && !tile.failed && activeRequests < MAX_CONCURRENT_REQUESTS) {
                            tile.loading = true;"""

loop_new = """                for (let tile of tileArray) {
                    const isMainVisible = (camera.position.z <= unloadZ) && (tile.xCenter >= minX && tile.xCenter <= maxX);
                    const isMagVisible = magActive && isHighRes && (tile.xCenter >= magMinX - actualMargin && tile.xCenter <= magMaxX + actualMargin);
                    const isVisible = isMainVisible || isMagVisible;
                    
                    if (isVisible) {
                        const canLoadNewTile = !isHighRes || (smoothedCameraSpeed < 0.015);

                        if (canLoadNewTile && !tile.loaded && !tile.loading && !tile.failed && activeRequests < MAX_CONCURRENT_REQUESTS) {
                            tile.loading = true;"""
content = content.replace(loop_old, loop_new)

else_old = """                    } else {
                        // Unload far away tiles
                        if (tile.loaded && Math.abs(tile.xCenter - camera.position.x) > actualMargin * 3) {
                            if (tile.mesh.material.map) {
                                tile.mesh.material.map.dispose();
                            }"""

else_new = """                    } else {
                        // Unload far away tiles smoothly. A large margin multiplier acts as a cache so tiles don't pop out immediately
                        if (tile.loaded && Math.abs(tile.xCenter - camera.position.x) > actualMargin * 5) {
                            if (tile.mesh.material.map) {
                                tile.mesh.material.map.dispose();
                            }"""
content = content.replace(else_old, else_new)

with open('index.html', 'w') as f:
    f.write(content)
