import sys

with open('index.html', 'r') as f:
    content = f.read()

html_old = """        <ul style="padding-left: 20px; line-height: 1.6;">
            <li><strong>Desktop:</strong> Left-click and drag anywhere to pan smoothly across the tapestry. Use your scroll wheel to zoom in and out. Keyboard arrows also work.</li>
            <li><strong>Desktop:</strong> Click on any English translation floating in the scene to open an interactive historical context popup!</li>
            <li><strong>Mobile:</strong> Swipe to pan in any direction. Use a two-finger pinch to zoom in and out.</li>
            <li><strong>Details:</strong> Zoom in closely on a specific scene to automatically load ultra-high resolution textures.</li>
        </ul>"""

html_new = """        <ul style="padding-left: 20px; line-height: 1.6;">
            <li id="help-desktop-1">Left-click and drag anywhere to pan smoothly across the tapestry. Use your scroll wheel to zoom in and out. Keyboard arrows also work.</li>
            <li id="help-desktop-2">Click on any English translation floating in the scene to open an interactive historical context popup!</li>
            <li id="help-mobile-1" style="display: none;">Swipe to pan in any direction. Use a two-finger pinch to zoom in and out.</li>
            <li id="help-mobile-2" style="display: none;">Tap on any English translation to open an interactive historical context popup! (Tablet/iPad only)</li>
            <li>Zoom in closely on a specific scene to automatically load ultra-high resolution textures.</li>
        </ul>"""

content = content.replace(html_old, html_new)

script_old = """        const isTouchDevice = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;
        if (magToggleBtn && (isPhone || isTouchDevice)) {
            magToggleBtn.style.display = 'none';
        } else if (magToggleBtn) {"""

script_new = """        const isTouchDevice = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;
        
        // Dynamically toggle help dialog instructions based on device type
        if (isPhone || isTouchDevice) {
            document.getElementById('help-desktop-1').style.display = 'none';
            document.getElementById('help-desktop-2').style.display = 'none';
            document.getElementById('help-mobile-1').style.display = 'list-item';
            if (!isPhone) document.getElementById('help-mobile-2').style.display = 'list-item'; // iPad supports popups
        }
        
        if (magToggleBtn && (isPhone || isTouchDevice)) {
            magToggleBtn.style.display = 'none';
        } else if (magToggleBtn) {"""

content = content.replace(script_old, script_new)

with open('index.html', 'w') as f:
    f.write(content)
