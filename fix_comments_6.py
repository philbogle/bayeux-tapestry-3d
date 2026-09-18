import re

with open('index.html', 'r') as f:
    content = f.read()

content = content.replace(
    r"function createOrganicTexture(width = 256, height = 256, baseColor = '#181510', withSplotches = true) {",
    r"""/**
         * Generates a procedural noise texture for the floor, ceiling, and walls.
         * @param {number} width - Canvas width
         * @param {number} height - Canvas height
         * @param {string} baseColor - Base fill color
         * @param {boolean} withSplotches - Whether to add large dark organic splotches
         * @returns {THREE.CanvasTexture}
         */
        function createOrganicTexture(width = 256, height = 256, baseColor = '#181510', withSplotches = true) {"""
)

# And fix the single quote escape I accidentally introduced: `latinText = \'\')`
content = content.replace("latinText = \\'\\')", "latinText = '')")

with open('index.html', 'w') as f:
    f.write(content)
