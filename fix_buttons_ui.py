import sys

with open('index.html', 'r') as f:
    content = f.read()

# Desktop HTML
desk_old = """            <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                Titles
            </label>
            <button id="notes-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">☰ Notes</button>
                <button id="mag-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">🔍 Magnifier</button>"""
desk_new = """            <button id="toggle-supertitles" style="pointer-events: auto; background: rgba(214,168,72,0.3); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">T Titles</button>
            <button id="notes-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">☰ Notes</button>
            <button id="mag-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">🔍</button>"""
content = content.replace(desk_old, desk_new)

# Mobile HTML
mob_old = """                    <label style="color: #d6a848; font-family: serif; font-size: 14px; pointer-events: auto; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                        <input type="checkbox" id="toggle-supertitles" checked style="pointer-events: auto; cursor: pointer;">
                        Titles
                    </label>
                    <button id="notes-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">☰ Notes</button>
                    <button id="mag-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">🔍 Magnifier</button>"""
mob_new = """                    <button id="toggle-supertitles" style="pointer-events: auto; background: rgba(214,168,72,0.3); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">T Titles</button>
                    <button id="notes-btn" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">☰ Notes</button>
                    <button id="mag-toggle" style="pointer-events: auto; background: rgba(20,20,20,0.8); border: 1px solid #5a4a35; color: #d6a848; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-family: serif; font-size: 13px;">🔍</button>"""
# Wait, mobile HTML might not have mag-toggle if I previously hid it, but actually the HTML is identical, it's just hidden via JS later.
# Wait! In the previous mobile UI I didn't see mag-toggle in the block because I missed it, or maybe it WAS there?
# Let's check `fix_order.py`: the mobile HTML didn't have `mag-toggle` explicitly in the replacement because it wasn't matched?
# Actually it wasn't in `mob_old` of `fix_order.py`.
# Let's just do a blanket replace for `toggle-supertitles` first.

with open('index.html', 'w') as f:
    f.write(content)
