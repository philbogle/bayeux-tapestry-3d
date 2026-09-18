import sys

with open('index.html', 'r') as f:
    content = f.read()

mag_old = """        const magToggleBtn = document.getElementById('mag-toggle');
        if (magToggleBtn) {"""
mag_new = """        const magToggleBtn = document.getElementById('mag-toggle');
        const isTouchDevice = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;
        if (magToggleBtn && (isPhone || isTouchDevice)) {
            magToggleBtn.style.display = 'none';
        } else if (magToggleBtn) {"""

content = content.replace(mag_old, mag_new)

with open('index.html', 'w') as f:
    f.write(content)
