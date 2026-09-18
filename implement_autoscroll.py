import sys

with open('index.html', 'r') as f:
    content = f.read()

# Add autoScrollTargetX and smooth scrolling to animate
animate_old = """        function animate() {
            requestAnimationFrame(animate);"""
animate_new = """        let autoScrollTargetX = null;
        
        function animate() {
            requestAnimationFrame(animate);
            
            if (autoScrollTargetX !== null) {
                camera.position.x += (autoScrollTargetX - camera.position.x) * 0.1;
                if (Math.abs(camera.position.x - autoScrollTargetX) < 0.01) {
                    camera.position.x = autoScrollTargetX;
                    autoScrollTargetX = null;
                }
            }"""
content = content.replace(animate_old, animate_new)

# Cancel autoscroll on wheel
wheel_old = """        window.addEventListener('wheel', (e) => {
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#about-dialog') || e.target.closest('#lighting-dialog')) return;
            e.preventDefault();"""
wheel_new = """        window.addEventListener('wheel', (e) => {
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#about-dialog') || e.target.closest('#lighting-dialog')) return;
            e.preventDefault();
            autoScrollTargetX = null;"""
content = content.replace(wheel_old, wheel_new)

# Cancel autoscroll on mouse drag
mouse_old = """        window.addEventListener('mousemove', (e) => {
            if (isTouch) return; 
            if (isMouseDown) {"""
mouse_new = """        window.addEventListener('mousemove', (e) => {
            if (isTouch) return; 
            if (isMouseDown) {
                autoScrollTargetX = null;"""
content = content.replace(mouse_old, mouse_new)

# Cancel autoscroll on touch drag
touch_old = """        window.addEventListener('touchmove', (e) => {
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#about-dialog') || e.target.closest('#lighting-dialog') || e.target.closest('#help-dialog')) return;
            e.preventDefault();
            hasTouchDragged = true;"""
touch_new = """        window.addEventListener('touchmove', (e) => {
            if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#about-dialog') || e.target.closest('#lighting-dialog') || e.target.closest('#help-dialog')) return;
            e.preventDefault();
            hasTouchDragged = true;
            autoScrollTargetX = null;"""
content = content.replace(touch_old, touch_new)

# Wire up the UI and buttons
ui_old = """                if (annoData) {
                    document.getElementById('context-title').innerText = `"${annoData.english}"`;
                    document.getElementById('context-title').style.fontStyle = 'italic'; // Add italic for quoted translation
                    
                    const contextText = (annoData.context) ? annoData.context : "No historical context available for this scene.";
                    document.getElementById('context-text').innerText = contextText;
                    document.getElementById('context-scroll').style.display = 'block';
                }"""

ui_new = """                if (annoData) {
                    const index = tituliData.indexOf(annoData);
                    updatePopupUI(index);
                }"""
content = content.replace(ui_old, ui_new)

# Add updatePopupUI and event listeners for buttons
# I will append them inside the DOMContentLoaded block, or near handleAnnotationClick
buttons_js = """
        let currentPopupSceneIndex = 0;

        function updatePopupUI(index) {
            if (index < 0 || index >= tituliData.length) return;
            currentPopupSceneIndex = index;
            const annoData = tituliData[index];
            
            document.getElementById('context-title').innerText = `"${annoData.english}"`;
            document.getElementById('context-title').style.fontStyle = 'italic';
            
            const contextText = (annoData.context) ? annoData.context : "No historical context available for this scene.";
            document.getElementById('context-text').innerText = contextText;
            
            document.getElementById('prev-scene').style.opacity = (index === 0) ? '0.5' : '1.0';
            document.getElementById('prev-scene').style.pointerEvents = (index === 0) ? 'none' : 'auto';
            
            document.getElementById('next-scene').style.opacity = (index === tituliData.length - 1) ? '0.5' : '1.0';
            document.getElementById('next-scene').style.pointerEvents = (index === tituliData.length - 1) ? 'none' : 'auto';
            
            document.getElementById('context-scroll').style.display = 'block';
            
            if (annoData.x !== undefined) {
                autoScrollTargetX = annoData.x;
            }
        }

        document.getElementById('prev-scene').addEventListener('click', () => {
            updatePopupUI(currentPopupSceneIndex - 1);
        });

        document.getElementById('next-scene').addEventListener('click', () => {
            updatePopupUI(currentPopupSceneIndex + 1);
        });
"""

# inject right before handleAnnotationClick
content = content.replace("function handleAnnotationClick", buttons_js + "\n        function handleAnnotationClick")

with open('index.html', 'w') as f:
    f.write(content)
