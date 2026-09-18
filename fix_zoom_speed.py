import sys

with open('index.html', 'r') as f:
    content = f.read()

# Mouse wheel
wheel_old = """            if (Math.abs(deltaY) > 0) {
                const zoomImpulse = (deltaY * 0.0005) * Math.max(1.0, camera.position.z * 0.1);
                velocityZ += zoomImpulse;
            }"""
wheel_new = """            if (Math.abs(deltaY) > 0) {
                const zoomImpulse = (deltaY * 0.0012) * Math.max(1.0, camera.position.z * 0.1);
                velocityZ += zoomImpulse;
            }"""
content = content.replace(wheel_old, wheel_new)

# Keyboard
key_old = """const fixedZoomAccel = 0.01;"""
key_new = """const fixedZoomAccel = 0.025;"""
content = content.replace(key_old, key_new)

with open('index.html', 'w') as f:
    f.write(content)
