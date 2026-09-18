import sys

with open('index.html', 'r') as f:
    content = f.read()

update_logic_old = """            // Prioritize processing based on zoom level to manage activeRequests cap
            if (camera.position.z <= 1.0) {
                processTiles(tilesL18, '18', true, 1.0);
                processTiles(tilesL17, '17', true, 2.0);
                processTiles(tiles, '16', false, 9999);
            } else if (camera.position.z <= 2.0) {
                processTiles(tilesL17, '17', true, 2.0);
                processTiles(tiles, '16', false, 9999);
                processTiles(tilesL18, '18', true, 1.0); // Fast unload
            } else {
                processTiles(tiles, '16', false, 9999);
                processTiles(tilesL17, '17', true, 2.0); // Fast unload
                processTiles(tilesL18, '18', true, 1.0); // Fast unload
            }"""
            
update_logic_new = """            // Prioritize processing based on zoom level to manage activeRequests cap
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
            
content = content.replace(update_logic_old, update_logic_new)

with open('index.html', 'w') as f:
    f.write(content)
