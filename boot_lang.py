import sys

with open('index.html', 'r') as f:
    content = f.read()

# Call changeLanguage immediately so UI matches localStorage on page load
content = content.replace("        initWebGL();", "        changeLanguage(currentLanguage);\n        initWebGL();")

with open('index.html', 'w') as f:
    f.write(content)
