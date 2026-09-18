import sys

with open('index.html', 'r') as f:
    content = f.read()

# Fix event listener at line 1050ish
title_old = """        const toggleSupertitles = document.getElementById('toggle-supertitles');
        if (toggleSupertitles) {
            // Toggle the visibility of all loaded English text meshes
            toggleSupertitles.addEventListener('change', (e) => {
                const container = document.getElementById('annotations-container');
                if (container) {
                    container.style.display = e.target.checked ? 'block' : 'none';
                }
            });
        }"""
title_new = """        const toggleSupertitles = document.getElementById('toggle-supertitles');
        let showSupertitles = true;
        if (toggleSupertitles) {
            // Toggle the visibility of all loaded English text meshes
            toggleSupertitles.addEventListener('click', (e) => {
                e.preventDefault();
                showSupertitles = !showSupertitles;
                toggleSupertitles.style.background = showSupertitles ? 'rgba(214,168,72,0.3)' : 'rgba(20,20,20,0.8)';
                const container = document.getElementById('annotations-container');
                if (container) {
                    container.style.display = showSupertitles ? 'block' : 'none';
                }
            });
        }"""
content = content.replace(title_old, title_new)

# Fix showSupertitles check in updateAnnotations (line 1705)
check_old = """            // Ensure UI checkbox sync
            const toggleSupertitles = document.getElementById('toggle-supertitles');
            const showSupertitles = toggleSupertitles ? toggleSupertitles.checked : true;"""
check_new = """            // UI button state controls visibility
            // (showSupertitles is now a global variable updated by the click listener)"""
content = content.replace(check_old, check_new)

with open('index.html', 'w') as f:
    f.write(content)
