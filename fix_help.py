import sys

with open('index.html', 'r') as f:
    content = f.read()

html_old = """            <li><strong>Desktop:</strong> Left-click and drag anywhere to pan smoothly across the tapestry. Use your scroll wheel to zoom in and out. Keyboard arrows also work.</li>
            <li><strong>Mobile:</strong> Swipe to pan in any direction. Use a two-finger pinch to zoom in and out.</li>
            <li><strong>Details:</strong> Zoom in closely on a specific scene to automatically load ultra-high resolution textures.</li>"""

html_new = """            <li><strong>Desktop:</strong> Left-click and drag anywhere to pan smoothly across the tapestry. Use your scroll wheel to zoom in and out. Keyboard arrows also work.</li>
            <li><strong>Desktop:</strong> Click on any English translation floating in the scene to open an interactive historical context popup!</li>
            <li><strong>Mobile:</strong> Swipe to pan in any direction. Use a two-finger pinch to zoom in and out.</li>
            <li><strong>Details:</strong> Zoom in closely on a specific scene to automatically load ultra-high resolution textures.</li>"""

content = content.replace(html_old, html_new)

with open('index.html', 'w') as f:
    f.write(content)
