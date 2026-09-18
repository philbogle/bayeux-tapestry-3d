import sys

with open('index.html', 'r') as f:
    content = f.read()

# Desktop UI
desk_old = """            <a href="#" id="learn-more-link" style="color: #d6a848; text-decoration: none; pointer-events: auto;">About</a>
            <button id="music-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">♪ Sound</button>
            <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                Titles
            </label>
            <button id="notes-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">☰ Notes</button>
                <button id="mag-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">🔍 Magnifier</button>
            <a href="#" id="lighting-controls-link" style="display: none; color: #d6a848; text-decoration: none; pointer-events: auto;">⚙️ Lighting Controls</a>"""

desk_new = """            <a href="#" id="learn-more-link" style="color: #d6a848; text-decoration: none; pointer-events: auto;">About</a>
            <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                Titles
            </label>
            <button id="notes-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">☰ Notes</button>
                <button id="mag-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">🔍 Magnifier</button>
            <button id="music-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">♪ Sound</button>
            <a href="#" id="lighting-controls-link" style="display: none; color: #d6a848; text-decoration: none; pointer-events: auto;">⚙️ Lighting Controls</a>"""

content = content.replace(desk_old, desk_new)

# Mobile UI
mob_old = """                    <a href="#" id="learn-more-link" style="color: #d6a848; text-decoration: none; pointer-events: auto;">About</a>
                    <button id="music-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">♪ Sound</button>
                    <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                        <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                        Titles
                    </label>
                    <button id="notes-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">☰ Notes</button>
                    <a href="#" id="lighting-controls-link" style="display: none; color: #d6a848; text-decoration: none; pointer-events: auto;">⚙️ Lighting Controls</a>"""

mob_new = """                    <a href="#" id="learn-more-link" style="color: #d6a848; text-decoration: none; pointer-events: auto;">About</a>
                    <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                        <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                        Titles
                    </label>
                    <button id="notes-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">☰ Notes</button>
                    <button id="music-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">♪ Sound</button>
                    <a href="#" id="lighting-controls-link" style="display: none; color: #d6a848; text-decoration: none; pointer-events: auto;">⚙️ Lighting Controls</a>"""

content = content.replace(mob_old, mob_new)

with open('index.html', 'w') as f:
    f.write(content)
