import sys

with open('index.html', 'r') as f:
    content = f.read()

func_old = """                const contextText = (annoData && annoData.context) ? annoData.context : "No historical context has been added for this scene yet. (Pending translation/context update)";"""
func_new = """                const contextText = (annoData && annoData.context) ? annoData.context : `No historical context has been added for this scene yet. (Pending translation/context update for: "${annoData.english}")`;"""
content = content.replace(func_old, func_new)

with open('index.html', 'w') as f:
    f.write(content)
