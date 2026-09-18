import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace the isIOS and isMobile declaration
old_ua = """        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/.test(navigator.userAgent) || isIOS;"""

new_ua = """        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
        const isIPad = /iPad/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
        // Treat iPads and large tablets as desktop for full graphics/lighting, restrict simplified experience to phones
        const isPhone = (/iPhone|iPod|IEMobile|Opera Mini/.test(navigator.userAgent)) || 
                        (/Android/.test(navigator.userAgent) && /Mobile/.test(navigator.userAgent)) || 
                        (isIOS && !isIPad) ||
                        (window.innerWidth <= 600);"""

content = content.replace(old_ua, new_ua)

# Replace all isMobile with isPhone
content = content.replace('isMobile', 'isPhone')

# Brighten floor, ceiling, and walls on phones
old_floor = "const floorTexture = createOrganicTexture(512, 512, '#0a0806', false);"
new_floor = "const floorTexture = createOrganicTexture(512, 512, isPhone ? '#2a221a' : '#0a0806', false);"
content = content.replace(old_floor, new_floor)

old_ceiling = "const ceilingTexture = createOrganicTexture(512, 512, '#080706', false);"
new_ceiling = "const ceilingTexture = createOrganicTexture(512, 512, isPhone ? '#1c1815' : '#080706', false);"
content = content.replace(old_ceiling, new_ceiling)

old_wall = "const wallTexture = createOrganicTexture(512, 512, '#0c0a08', false);"
new_wall = "const wallTexture = createOrganicTexture(512, 512, isPhone ? '#2c221a' : '#0c0a08', false);"
content = content.replace(old_wall, new_wall)

with open('index.html', 'w') as f:
    f.write(content)
