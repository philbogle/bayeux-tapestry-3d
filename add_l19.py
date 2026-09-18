import sys

with open('index.html', 'r') as f:
    content = f.read()

# 1. Add tilesL19 initialization
l18_block = """        const tilesL18 = [];
        const W18 = W * 4;
        const H18 = H * 4;
        const cols18 = Math.ceil(W18 / T);
        const rows18 = Math.ceil(H18 / T);

            for (let r = 0; r < rows18; r++) {
                for (let c = 0; c < cols18; c++) {
                    const x_topLeft = c === 0 ? 0 : c * T - 1;
                    const y_topLeft = r === 0 ? 0 : r * T - 1;

                    const w = (c === cols18 - 1) ? (W18 - x_topLeft) : (T + (c === 0 ? 0 : 1) + 1);
                    const h = (r === rows18 - 1) ? (H18 - y_topLeft) : (T + (r === 0 ? 0 : 1) + 1);

                    const widthUnits = (w / SCALE) / 4; 
                    const heightUnits = (h / SCALE) / 4;
                    
                    const xCenter = (x_topLeft + w / 2) / (SCALE * 4);
                    const yCenter = -(y_topLeft + h / 2) / (SCALE * 4) + tapestryElevation;

                    const zOffset = 0.02 + (c % 2) * 0.001 + (r % 2) * 0.002;

                    const mesh = new THREE.Mesh(baseGeometry, emptyMaterial);
                    mesh.scale.set(widthUnits, heightUnits, 1);
                    mesh.position.set(xCenter, yCenter, zOffset);
                    
                    scene.add(mesh);
                    
                    tilesL18.push({
                        c, r,
                        xCenter,
                        mesh: mesh,
                        loaded: false,
                        loading: false,
                        failed: false
                    });
                }
            }"""

l19_block = l18_block + """
        const tilesL19 = [];
        const W19 = W * 8;
        const H19 = H * 8;
        const cols19 = Math.ceil(W19 / T);
        const rows19 = Math.ceil(H19 / T);

            for (let r = 0; r < rows19; r++) {
                for (let c = 0; c < cols19; c++) {
                    const x_topLeft = c === 0 ? 0 : c * T - 1;
                    const y_topLeft = r === 0 ? 0 : r * T - 1;

                    const w = (c === cols19 - 1) ? (W19 - x_topLeft) : (T + (c === 0 ? 0 : 1) + 1);
                    const h = (r === rows19 - 1) ? (H19 - y_topLeft) : (T + (r === 0 ? 0 : 1) + 1);

                    const widthUnits = (w / SCALE) / 8; 
                    const heightUnits = (h / SCALE) / 8;
                    
                    const xCenter = (x_topLeft + w / 2) / (SCALE * 8);
                    const yCenter = -(y_topLeft + h / 2) / (SCALE * 8) + tapestryElevation;

                    const zOffset = 0.03 + (c % 2) * 0.001 + (r % 2) * 0.002;

                    const mesh = new THREE.Mesh(baseGeometry, emptyMaterial);
                    mesh.scale.set(widthUnits, heightUnits, 1);
                    mesh.position.set(xCenter, yCenter, zOffset);
                    
                    // Optional: only add to scene when mag is active to save 40k meshes in frustum culler?
                    // Frustum culling 40k invisible meshes is fast enough in ThreeJS.
                    scene.add(mesh);
                    
                    tilesL19.push({
                        c, r,
                        xCenter,
                        mesh: mesh,
                        loaded: false,
                        loading: false,
                        failed: false
                    });
                }
            }"""
            
content = content.replace(l18_block, l19_block)

with open('index.html', 'w') as f:
    f.write(content)
