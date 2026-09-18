import sys

with open('index.html', 'r') as f:
    content = f.read()

# Replace magnifier icon with SVG and increase padding
mag_old = """<button id="mag-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">⌕</button>"""
mag_new = """<button id="mag-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 25px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px; display: flex; align-items: center; justify-content: center;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="10" r="7"></circle><line x1="21" y1="21" x2="15" y2="15"></line></svg></button>"""
content = content.replace(mag_old, mag_new)

# Sound button increase padding
sound_old = """<button id="music-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">♪</button>"""
sound_new = """<button id="music-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 25px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 16px; display: flex; align-items: center; justify-content: center;">♪</button>"""
content = content.replace(sound_old, sound_new)

with open('index.html', 'w') as f:
    f.write(content)
