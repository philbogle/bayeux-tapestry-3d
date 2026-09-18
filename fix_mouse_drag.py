import sys

with open('index.html', 'r') as f:
    content = f.read()

mousedown_old = """        let isMouseDragging = false;
        
        window.addEventListener('mousedown', (e) => {
            if (isTouch) return;
            isMouseDragging = false;"""
mousedown_new = """        let mouseStartX = 0;
        let mouseStartY = 0;
        
        window.addEventListener('mousedown', (e) => {
            if (isTouch) return;
            mouseStartX = e.clientX;
            mouseStartY = e.clientY;"""
content = content.replace(mousedown_old, mousedown_new)


mousemove_old = """        window.addEventListener('mousemove', (e) => {
            if (isTouch) return; 
            if (isMouseDown) isMouseDragging = true;"""
mousemove_new = """        window.addEventListener('mousemove', (e) => {
            if (isTouch) return; """
content = content.replace(mousemove_old, mousemove_new)


mouseup_old = """            if (!isTouch && isMouseDown) {
                isMouseDown = false;
                document.body.style.cursor = 'default';
                if (!isMouseDragging) {
                    handleAnnotationClick(e.clientX, e.clientY, e.target);
                }
            }"""
mouseup_new = """            if (!isTouch && isMouseDown) {
                isMouseDown = false;
                document.body.style.cursor = 'default';
                const dist = Math.hypot(e.clientX - mouseStartX, e.clientY - mouseStartY);
                if (dist < 5) {
                    handleAnnotationClick(e.clientX, e.clientY, e.target);
                }
            }"""
content = content.replace(mouseup_old, mouseup_new)

with open('index.html', 'w') as f:
    f.write(content)
