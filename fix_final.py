import sys

with open('index.html', 'r') as f:
    content = f.read()

# 1. Don't initialize tilesL19 on mobile
tilesL19_init_old = """        const tilesL19 = [];
        const W19 = W * 8;
        const H19 = H * 8;"""
tilesL19_init_new = """        const tilesL19 = [];
        if (!isPhone) {
        const W19 = W * 8;
        const H19 = H * 8;"""
content = content.replace(tilesL19_init_old, tilesL19_init_new)

tilesL19_loop_end_old = """                        loading: false,
                        failed: false
                    });
                }
            }
        
        // Calculate the visible width at our starting Z distance to align the left edge of the tapestry with the left of the viewport"""
tilesL19_loop_end_new = """                        loading: false,
                        failed: false
                    });
                }
            }
        } // end !isPhone
        
        // Calculate the visible width at our starting Z distance to align the left edge of the tapestry with the left of the viewport"""
content = content.replace(tilesL19_loop_end_old, tilesL19_loop_end_new)


# 2. Main camera zoom limit
zoom_limit_old = "if (camera.position.z < 0.5) camera.position.z = 0.5;"
zoom_limit_new = "if (camera.position.z < 1.2) camera.position.z = 1.2; // Keep main camera back so magnifier is always useful"
content = content.replace(zoom_limit_old, zoom_limit_new)


# 3. Dynamic unload logic
unload_old = "if (isHighRes && camera.position.z > unloadZ && !magActive) {"
unload_new = "if (isHighRes && camera.position.z > unloadZ && (!magActive || magCamera.position.z > unloadZ)) {"
content = content.replace(unload_old, unload_new)


# 4. Effective Z logic for processTiles order
update_logic_old = """            // Prioritize processing based on zoom level to manage activeRequests cap
            if (magActive || camera.position.z <= 0.5) {
                processTiles(tilesL19, '19', true, 0.5);
                processTiles(tilesL18, '18', true, 1.0);
                processTiles(tilesL17, '17', true, 2.0);
                processTiles(tiles, '16', false, 9999);
            } else if (camera.position.z <= 1.0) {
                processTiles(tilesL18, '18', true, 1.0);
                processTiles(tilesL17, '17', true, 2.0);
                processTiles(tiles, '16', false, 9999);
                processTiles(tilesL19, '19', true, 0.5); // Fast unload
            } else if (camera.position.z <= 2.0) {
                processTiles(tilesL17, '17', true, 2.0);
                processTiles(tiles, '16', false, 9999);
                processTiles(tilesL18, '18', true, 1.0); // Fast unload
                processTiles(tilesL19, '19', true, 0.5); // Fast unload
            } else {
                processTiles(tiles, '16', false, 9999);
                processTiles(tilesL17, '17', true, 2.0); // Fast unload
                processTiles(tilesL18, '18', true, 1.0); // Fast unload
                processTiles(tilesL19, '19', true, 0.5); // Fast unload
            }"""

update_logic_new = """            // Prioritize processing based on zoom level to manage activeRequests cap
            const effectiveZ = magActive ? Math.min(camera.position.z, magCamera.position.z) : camera.position.z;
            
            if (!isPhone && effectiveZ <= 0.5) {
                processTiles(tilesL19, '19', true, 0.5);
                processTiles(tilesL18, '18', true, 1.0);
                processTiles(tilesL17, '17', true, 2.0);
                processTiles(tiles, '16', false, 9999);
            } else if (effectiveZ <= 1.0) {
                processTiles(tilesL18, '18', true, 1.0);
                processTiles(tilesL17, '17', true, 2.0);
                processTiles(tiles, '16', false, 9999);
                if (!isPhone) processTiles(tilesL19, '19', true, 0.5); // Fast unload
            } else if (effectiveZ <= 2.0) {
                processTiles(tilesL17, '17', true, 2.0);
                processTiles(tiles, '16', false, 9999);
                processTiles(tilesL18, '18', true, 1.0); // Fast unload
                if (!isPhone) processTiles(tilesL19, '19', true, 0.5); // Fast unload
            } else {
                processTiles(tiles, '16', false, 9999);
                processTiles(tilesL17, '17', true, 2.0); // Fast unload
                processTiles(tilesL18, '18', true, 1.0); // Fast unload
                if (!isPhone) processTiles(tilesL19, '19', true, 0.5); // Fast unload
            }"""
content = content.replace(update_logic_old, update_logic_new)

with open('index.html', 'w') as f:
    f.write(content)
