import re

with open('index.html', 'r') as f:
    content = f.read()

replacements = [
    # Functions
    (r'(function onYouTubeIframeAPIReady\(\))', 
     r'/**\n         * Callback triggered by the YouTube IFrame API when it is fully loaded.\n         * Initializes the hidden YouTube audio player.\n         */\n        \1'),
    
    (r'(function createOrganicTexture\(width, height, baseColor, isHighRes\))', 
     r'/**\n         * Generates a procedural noise texture for the floor, ceiling, and walls.\n         * @param {number} width - Canvas width\n         * @param {number} height - Canvas height\n         * @param {string} baseColor - Base fill color\n         * @param {boolean} isHighRes - Whether to generate finer grain noise\n         * @returns {THREE.CanvasTexture}\n         */\n        \1'),
    
    (r'(function createShadowTexture\(\))', 
     r'/**\n         * Creates a subtle linear gradient texture to simulate ambient occlusion / shadow\n         * beneath the 3D tapestry mesh.\n         * @returns {THREE.CanvasTexture}\n         */\n        \1'),
    
    (r'(function updateCamera\(\))', 
     r'/**\n         * Core physics loop for camera movement.\n         * Handles inertia, keyboard acceleration, boundary clamping, and the 3D tilt effect.\n         */\n        \1'),
    
    (r'(function updateTiles\(\))', 
     r'/**\n         * Main LOD (Level of Detail) manager.\n         * Calculates the visible frustum and queues texture loading/unloading for L16, L17, and L18 layers.\n         */\n        \1'),
    
    (r'(function animate\(\))', 
     r'/**\n         * Main WebGL render loop.\n         * Updates physics, animations, dynamic lighting, and triggers the renderer.\n         */\n        \1'),
    
    (r'(function createTextMesh\(text, isPlaced\))', 
     r'/**\n         * Renders English translation text to a 2D canvas and maps it onto a 3D PlaneGeometry.\n         * @param {string} text - The English string to render\n         * @param {boolean} isPlaced - In authoring mode, unplaced text is rendered in red\n         * @returns {THREE.Mesh}\n         */\n        \1'),
]

for old, new in replacements:
    content = re.sub(old, new, content)

# Event listeners
event_replacements = [
    (r'(window.addEventListener\(\'touchstart\', \(e\) => \{)', 
     r'// Initialize touch tracking, halt any existing momentum, and handle raycasting for Authoring mode drags.\n        \1'),
    
    (r'(window.addEventListener\(\'touchmove\', \(e\) => \{)', 
     r'// Handle 1-finger panning and 2-finger pinch-to-zoom for mobile devices.\n        \1'),
    
    (r'(window.addEventListener\(\'touchend\', \(e\) => \{)', 
     r'// Handle touch release to smoothly transition back to 1-finger drag or apply release momentum.\n        \1'),
    
    (r'(window.addEventListener\(\'mousedown\', \(e\) => \{)', 
     r'// Initialize mouse drag tracking, halt momentum, and handle raycasting for Authoring mode.\n        \1'),
    
    (r'(window.addEventListener\(\'mousemove\', \(e\) => \{)', 
     r'// Handle desktop mouse dragging (panning) and update normalized mouse coordinates for 3D hover detection.\n        \1'),
    
    (r'(const stop = \(e\) => \{)', 
     r'// Handle mouse release to apply panning momentum and reset drag states.\n        \1'),
    
    (r'(window.addEventListener\(\'keydown\', \(e\) => \{)', 
     r'// Handle keyboard navigation (arrow keys/WASD) and prevent default scrolling behavior.\n        \1'),
    
    (r'(window.addEventListener\(\'keyup\', \(e\) => \{)', 
     r'// Clear keyboard navigation states upon key release.\n        \1'),
    
    (r'(window.addEventListener\(\'wheel\', \(e\) => \{)', 
     r'// Handle trackpad / mouse wheel zooming and horizontal panning.\n        \1'),
    
    (r'(window.addEventListener\(\'resize\', \(\) => \{)', 
     r'// Update the Three.js camera projection matrix and WebGL renderer dimensions on window resize.\n        \1'),
]

for old, new in event_replacements:
    content = re.sub(old, new, content)

with open('index.html', 'w') as f:
    f.write(content)
