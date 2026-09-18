import re

with open('index.html', 'r') as f:
    content = f.read()

content = content.replace(
    r"""/**
         * Renders English translation text to a 2D canvas and maps it onto a 3D PlaneGeometry.
         * @param {string} text - The English string to render
         * @param {boolean} isPlaced - In authoring mode, unplaced text is rendered in red
         * @param {string} latinText - The original Latin text, used to inherit authentic medieval punctuation
         * @returns {THREE.Mesh}
         */
        function createTextMesh(text, isPlaced, latinText = '') {""",
    r"""/**
         * Renders English translation text to a 2D canvas and maps it onto a 3D PlaneGeometry.
         * @param {string} text - The English string to render
         * @param {boolean} isPlaced - In authoring mode, unplaced text is rendered in red
         * @returns {THREE.Mesh}
         */
        function createTextMesh(text, isPlaced) {"""
)

with open('index.html', 'w') as f:
    f.write(content)
