import sys

with open('index.html', 'r') as f:
    content = f.read()

func_old = """                const contextText = (annoData && annoData.context) ? annoData.context : `No historical context has been added for this scene yet. (Pending translation/context update for: "${annoData ? annoData.english : 'Unknown'}")`;
                document.getElementById('context-text').innerText = contextText;
                document.getElementById('context-title').innerText = "Scene Context";
                document.getElementById('context-scroll').style.display = 'block';"""

func_new = """                if (annoData) {
                    document.getElementById('context-title').innerText = `"${annoData.english}"`;
                    document.getElementById('context-title').style.fontStyle = 'italic'; // Add italic for quoted translation
                    document.getElementById('context-text').innerText = (annoData.latin || "").toUpperCase();
                    document.getElementById('context-scroll').style.display = 'block';
                }"""

content = content.replace(func_old, func_new)

with open('index.html', 'w') as f:
    f.write(content)
