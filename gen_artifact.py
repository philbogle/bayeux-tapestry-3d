import json
import os

with open('tituli.json', 'r') as f:
    data = json.load(f)

md_content = "# Bayeux Tapestry Translations & Historical Context\n\n"

for index, item in enumerate(data):
    scene_num = item.get('scene', '?')
    english = item.get('english', '')
    context = item.get('context', 'No historical context added yet.')
    
    md_content += f"### {index + 1}. Scene {scene_num}\n"
    md_content += f"**Translation:** {english}\n\n"
    md_content += f"**Context:** {context}\n\n"
    md_content += "---\n\n"

out_path = '/Users/phil.bogle/.gemini/antigravity/brain/435a34d1-3721-46a3-bc56-48a2d14233e6/translations_and_context.md'
with open(out_path, 'w') as f:
    f.write(md_content)
print(f"Generated {out_path}")
