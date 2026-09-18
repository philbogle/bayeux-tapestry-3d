import sys

with open('index.html', 'r') as f:
    content = f.read()

processTiles_old = """                    const inMainView = (tileRight >= minX - margin) && (tileLeft <= maxX + margin);
                    
                    if (inMainView) {"""
processTiles_new = """                    const inMainView = (tileRight >= minX - margin) && (tileLeft <= maxX + margin);
                    const inMagView = magActive && isHighRes && (tileRight >= magMinX - margin) && (tileLeft <= magMaxX + margin);
                    
                    if (inMainView || inMagView) {"""
content = content.replace(processTiles_old, processTiles_new)

with open('index.html', 'w') as f:
    f.write(content)
