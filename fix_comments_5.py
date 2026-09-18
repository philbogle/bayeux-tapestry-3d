import re

with open('index.html', 'r') as f:
    content = f.read()

# Revert the bad stop() comment
content = content.replace(
    '// Handle mouse release to apply panning momentum and reset drag states.\n        const stop = (e) => { e.preventDefault(); keys[keyName] = false; };',
    'const stop = (e) => { e.preventDefault(); keys[keyName] = false; };'
)

# Add createOrganicTexture comment
content = re.sub(
    r'(function createOrganicTexture\(width = 512, height = 512, baseColor = \'\#1a1510\', isHighRes = false\))',
    r'/**\n         * Generates a procedural noise texture for the floor, ceiling, and walls.\n         * @param {number} width - Canvas width\n         * @param {number} height - Canvas height\n         * @param {string} baseColor - Base fill color\n         * @param {boolean} isHighRes - Whether to generate finer grain noise\n         * @returns {THREE.CanvasTexture}\n         */\n        \1',
    content
)

# Add createTextMesh comment properly (I missed the latinText parameter)
content = re.sub(
    r'(\/\*\*\n         \* Renders English translation text to a 2D canvas and maps it onto a 3D PlaneGeometry\.\n         \* @param \{string\} text - The English string to render\n         \* @param \{boolean\} isPlaced - In authoring mode, unplaced text is rendered in red\n         \* @returns \{THREE\.Mesh\}\n         \*\/\n        function createTextMesh\(text, isPlaced\))',
    r'/**\n         * Renders English translation text to a 2D canvas and maps it onto a 3D PlaneGeometry.\n         * @param {string} text - The English string to render\n         * @param {boolean} isPlaced - In authoring mode, unplaced text is rendered in red\n         * @param {string} latinText - The original Latin text, used to inherit authentic medieval punctuation\n         * @returns {THREE.Mesh}\n         */\n        function createTextMesh(text, isPlaced, latinText = \'\')',
    content
)

# Wait, createTextMesh definition in index.html already has latinText in the parameters!
# Let me just check how it's defined in the file.
with open('index.html', 'w') as f:
    f.write(content)
