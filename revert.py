with open('index.html', 'r') as f:
    content = f.read()

content = content.replace("const planeGeo = new THREE.PlaneGeometry(length, 120, Math.ceil(length / 10), 12);", "const planeGeo = new THREE.PlaneGeometry(length, 120);")
content = content.replace("const floorMat = new THREE.MeshPhongMaterial({ map: floorTexture, shininess: 60, specular: 0x554433 });", "const floorMat = new THREE.MeshPhongMaterial({ map: floorTexture, shininess: 5 });")
content = content.replace("const wallGeo = new THREE.PlaneGeometry(length, 120, Math.ceil(length / 10), 12);", "const wallGeo = new THREE.PlaneGeometry(length, 120);")

with open('index.html', 'w') as f:
    f.write(content)
