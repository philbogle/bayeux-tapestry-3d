import sys

with open('index.html', 'r') as f:
    content = f.read()

func_old = """        function handleAnnotationClick(clientX, clientY, target) {
            if (target && target.closest && (target.closest('#ui') || target.closest('#authoring-panel') || target.closest('#about-dialog') || target.closest('#lighting-dialog') || target.closest('#help-dialog') || target.closest('#context-scroll'))) {
                return;
            }"""

func_new = """        function handleAnnotationClick(clientX, clientY, target) {
            if (isPhone) return; // Feature disabled on mobile devices
            if (target && target.closest && (target.closest('#ui') || target.closest('#authoring-panel') || target.closest('#about-dialog') || target.closest('#lighting-dialog') || target.closest('#help-dialog') || target.closest('#context-scroll'))) {
                return;
            }"""

content = content.replace(func_old, func_new)

with open('index.html', 'w') as f:
    f.write(content)
