import sys

with open('index.html', 'r') as f:
    content = f.read()

refresh = """
            const popup = document.getElementById('context-scroll');
            if (popup && popup.style.display !== 'none') {
                updatePopupUI(currentPopupSceneIndex, false);
            }
        }
"""
content = content.replace("scene.add(newMesh);\n            });\n        }", "scene.add(newMesh);\n            });" + refresh)

with open('index.html', 'w') as f:
    f.write(content)
