import sys

with open('index.html', 'r') as f:
    content = f.read()

opacity_old = """                // Static opacity, no hover effect
                let opacity = 0.50 * scrollOpacityMult;
                if (isAuthoringMode) opacity = 1.0;
                
                ann.mesh.material.opacity = opacity;"""

opacity_new = """                // Smoothly transition opacity to 1.0 when hovered, 0.50 normally
                if (ann.currentOpacity === undefined) ann.currentOpacity = 0.50;
                
                const targetOpacity = (hoveredMesh === ann.mesh || isAuthoringMode) ? 1.0 : 0.50;
                ann.currentOpacity += (targetOpacity - ann.currentOpacity) * 0.2; // Smooth lerp
                
                ann.mesh.material.opacity = ann.currentOpacity * scrollOpacityMult;
                
                // Add a subtle scale effect on hover as well
                const targetScale = (hoveredMesh === ann.mesh) ? 1.05 : 1.0;
                if (ann.currentScale === undefined) ann.currentScale = 1.0;
                ann.currentScale += (targetScale - ann.currentScale) * 0.2;
                ann.mesh.scale.set(ann.currentScale, ann.currentScale, 1);"""

content = content.replace(opacity_old, opacity_new)

with open('index.html', 'w') as f:
    f.write(content)
