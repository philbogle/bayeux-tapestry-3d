import sys

with open('index.html', 'r') as f:
    content = f.read()

func_old = """            if (intersects.length > 0) {
                const clickedMesh = intersects[0].object;
                const annoData = clickedMesh.userData.annotation;
                
                const contextText = (annoData && annoData.context) ? annoData.context : `No historical context has been added for this scene yet. (Pending translation/context update for: "${annoData.english}")`;
                document.getElementById('context-text').innerText = contextText;
                document.getElementById('context-title').innerText = "Scene Context";
                document.getElementById('context-scroll').style.display = 'block';
            }"""

func_new = """            if (intersects.length > 0) {
                const clickedMesh = intersects[0].object;
                const annoObj = clickedMesh.userData.annotation;
                const annoData = annoObj ? annoObj.data : null;
                
                const contextText = (annoData && annoData.context) ? annoData.context : `No historical context has been added for this scene yet. (Pending translation/context update for: "${annoData ? annoData.english : 'Unknown'}")`;
                document.getElementById('context-text').innerText = contextText;
                document.getElementById('context-title').innerText = "Scene Context";
                document.getElementById('context-scroll').style.display = 'block';
            }"""

content = content.replace(func_old, func_new)

with open('index.html', 'w') as f:
    f.write(content)
