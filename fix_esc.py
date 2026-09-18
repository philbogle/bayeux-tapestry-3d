import sys

with open('index.html', 'r') as f:
    content = f.read()

keydown_old = """        window.addEventListener('keydown', (e) => {
            if (e.key.toLowerCase() === 'm' && !isPhone) {
                magActive = !magActive;
                if (magToggleBtn) magToggleBtn.style.background = magActive ? 'rgba(214,168,72,0.3)' : 'rgba(20,20,20,0.8)';
                if (!magActive) lensMesh.position.set(-9999, -9999, 0);
            }"""

keydown_new = """        window.addEventListener('keydown', (e) => {
            if (e.key.toLowerCase() === 'm' && !isPhone) {
                magActive = !magActive;
                if (magToggleBtn) magToggleBtn.style.background = magActive ? 'rgba(214,168,72,0.3)' : 'rgba(20,20,20,0.8)';
                if (!magActive) lensMesh.position.set(-9999, -9999, 0);
            }
            if (e.key === 'Escape' && magActive) {
                magActive = false;
                if (magToggleBtn) magToggleBtn.style.background = 'rgba(20,20,20,0.8)';
                lensMesh.position.set(-9999, -9999, 0);
            }"""

content = content.replace(keydown_old, keydown_new)

with open('index.html', 'w') as f:
    f.write(content)
