import sys

with open('index.html', 'r') as f:
    content = f.read()

# 1. Add to updateCamera
updateCamera_old = """            if (camera.position.z < 0.5) camera.position.z = 0.5;
            if (camera.position.z > 2000) camera.position.z = 2000;
        }"""
updateCamera_new = """            if (camera.position.z < 0.5) camera.position.z = 0.5;
            if (camera.position.z > 2000) camera.position.z = 2000;
            
            if (magActive) {
                magCamera.position.z = Math.max(0.3, camera.position.z * 0.25);
            }
        }"""
content = content.replace(updateCamera_old, updateCamera_new)

# 2. Remove from animate() (Actually, it's not currently in animate() because I haven't added it yet!)
# I didn't add it to animate yet.

with open('index.html', 'w') as f:
    f.write(content)
