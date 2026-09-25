/**
 * Bayeux Tapestry 3D Explorer
 * ---------------------------
 * A highly optimized, WebGL-powered 3D visualization of the Bayeux Tapestry using Three.js.
 * 
 * Core Features:
 * - Tile-based Rendering: The massive 68-meter tapestry is split into chunks and dynamically culled/rendered to maintain 60fps.
 * - Cinematic Intro: A sweeping, math-driven (smoothstep) camera sequence with decoupled ambient lighting fade-ups.
 * - Multi-language Tour: Interactive POI (Point of Interest) tour system driven by a single `bayeux_data.json` payload.
 * - Custom Input Handling: Device-agnostic 2D navigation (mouse wheel, touch drag, pinch-to-zoom) with physical inertia.
 * - Scene Dwell: A slow, "breathing" zoom effect when the user rests on a specific historical scene.
 * - Authoring Mode: (Accessed via ?author=1) Hidden tools to reposition and align textual Latin inscriptions.
 *
 * Architecture Notes:
 * - `bayeux_data.json` contains both the UI localization strings and the 51 Scene POI markers.
 * - Overlaid HTML elements (in index.html) handle standard UI (menus, dialogs).
 * - A hidden YouTube IFrame API handles the looping medieval atmospheric soundtrack to save bandwidth.
 */

let ytPlayer;
/**
 * Callback triggered by the YouTube IFrame API when it is fully loaded.
 * Initializes the hidden YouTube audio player.
 */
function onYouTubeIframeAPIReady() {
    ytPlayer = new YT.Player('yt-player', {
        height: '1',
        width: '1',
        videoId: 'd6KTJpMLe1g',
        playerVars: {
            'playsinline': 1,
            'loop': 1,
            'playlist': 'd6KTJpMLe1g', // Required for loop to work
            'origin': window.location.origin
        }
    });
}

    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
const isIPad = /iPad/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
if (isIPad) document.body.classList.add('ipad-mode');
// Treat iPads and large tablets as desktop for full graphics/lighting, restrict simplified experience to phones
const isPhone = (/iPhone|iPod|IEMobile|Opera Mini/.test(navigator.userAgent)) ||
    (/Android/.test(navigator.userAgent) && /Mobile/.test(navigator.userAgent)) ||
    (isIOS && !isIPad) ||
    (window.innerWidth <= 600);

let useSimpleLighting = isPhone || isIPad;

let annotations = [];


let isTourActive = false;
let isTourPaused = false;
let tourSessionSeed = 0;

function isMobileMode() {
    return isPhone || (window.innerWidth <= 900 && !isIPad);
}

const uiContainer = document.getElementById('ui');
const hamburgerBtn = document.getElementById('hamburger-btn');
const mobileMenu = document.getElementById('mobile-menu');
const mobileMenuScrim = document.getElementById('mobile-menu-scrim');

function openMobileMenu() {
    if (!mobileMenu) return;
    mobileMenu.style.display = 'block';
    if (mobileMenuScrim) mobileMenuScrim.style.display = 'block';
    if (hamburgerBtn) {
        hamburgerBtn.innerText = '✕';
        hamburgerBtn.setAttribute('aria-expanded', 'true');
    }
}

function closeMobileMenu() {
    if (!mobileMenu) return;
    mobileMenu.style.display = 'none';
    if (mobileMenuScrim) mobileMenuScrim.style.display = 'none';
    if (hamburgerBtn) {
        hamburgerBtn.innerText = '☰';
        hamburgerBtn.setAttribute('aria-expanded', 'false');
    }
}

function toggleMobileMenu() {
    if (mobileMenu && window.getComputedStyle(mobileMenu).display !== 'none') {
        closeMobileMenu();
    } else {
        openMobileMenu();
    }
}

function updateLayoutMode() {
    const mobile = isMobileMode();
    if (hamburgerBtn) hamburgerBtn.style.display = mobile ? 'flex' : 'none';
    if (uiContainer) uiContainer.style.display = mobile ? 'none' : 'block';
}

updateLayoutMode();
window.addEventListener('resize', updateLayoutMode);

if (hamburgerBtn) {
    hamburgerBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMobileMenu();
    });
}

if (mobileMenuScrim) {
    mobileMenuScrim.addEventListener('click', (e) => {
        e.stopPropagation();
        closeMobileMenu();
    });
    mobileMenuScrim.addEventListener('touchstart', (e) => {
        e.stopPropagation();
        closeMobileMenu();
    }, { passive: true });
}

if (mobileMenu) {
    ['mousedown', 'touchstart', 'pointerdown', 'click'].forEach(evt => {
        mobileMenu.addEventListener(evt, (e) => {
            e.stopPropagation();
        });
    });
}

window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeMobileMenu();
    }
});

// Wire mobile menu action rows
const mTour = document.getElementById('m-menu-tour');
if (mTour) {
    mTour.addEventListener('click', () => {
        closeMobileMenu();
        const popup = document.getElementById('context-scroll');
        if (popup && window.getComputedStyle(popup).display !== 'none') {
            closeNotes();
        } else {
            openNotes(true);
        }
    });
}

const mNotes = document.getElementById('m-menu-notes');
if (mNotes) {
    mNotes.addEventListener('click', () => {
        closeMobileMenu();
        const popup = document.getElementById('context-scroll');
        if (popup && window.getComputedStyle(popup).display !== 'none') {
            closeNotes();
        } else {
            openNotes(true);
        }
    });
}

const mTitles = document.getElementById('m-menu-titles');
if (mTitles) {
    mTitles.addEventListener('click', () => {
        closeMobileMenu();
        showSupertitles = !showSupertitles;
        if (typeof updateTitlesUI === 'function') updateTitlesUI();
    });
}

const mLang = document.getElementById('m-menu-lang');
if (mLang) {
    mLang.addEventListener('click', () => {
        closeMobileMenu();
        document.querySelectorAll('.lang-option').forEach(opt => {
            if (opt.getAttribute('data-lang') === currentLanguage) {
                opt.style.background = '#8b7355';
                opt.style.border = '1px solid #f4e4bc';
            } else {
                opt.style.background = '#2c221a';
                opt.style.border = '1px solid #444';
            }
        });
        document.getElementById('lang-dialog').style.display = 'block';
    });
}

const mHelp = document.getElementById('m-menu-help');
if (mHelp) {
    mHelp.addEventListener('click', () => {
        closeMobileMenu();
        document.getElementById('help-dialog').style.display = 'block';
    });
}

const mAbout = document.getElementById('m-menu-about');
if (mAbout) {
    mAbout.addEventListener('click', () => {
        closeMobileMenu();
        document.getElementById('about-dialog').style.display = 'block';
    });
}

const mMusic = document.getElementById('m-menu-music');
if (mMusic) {
    mMusic.addEventListener('click', () => {
        closeMobileMenu();
        if (typeof toggleMusic === 'function') toggleMusic();
    });
}

const mFullscreen = document.getElementById('m-menu-fullscreen');
if (mFullscreen) {
    mFullscreen.addEventListener('click', () => {
        closeMobileMenu();
        if (typeof toggleFullscreen === 'function') toggleFullscreen();
    });
}

const mLighting = document.getElementById('m-menu-lighting');
if (mLighting) {
    if (new URLSearchParams(window.location.search).get('adv') === '1') {
        mLighting.style.display = 'flex';
        mLighting.addEventListener('click', () => {
            closeMobileMenu();
            document.getElementById('lighting-dialog').style.display = 'block';
        });
    }
}

if (new URLSearchParams(window.location.search).get('menu') === '1') {
    openMobileMenu();
    setTimeout(openMobileMenu, 250);
}

const T = 254; // Tile size without overlap
const LEVEL = 16; // 16 provides a very high resolution while being manageable
const W = 60262;
const H = 694;
const SCALE = 100; // 100 pixels = 1 Three.js unit
let currentLanguage = localStorage.getItem('bayeux_lang') || 'en';
let uiDict = {};


const cols = Math.ceil(W / T);
const rows = Math.ceil(H / T);

const scene = new THREE.Scene();
const canvasGroup = new THREE.Group();
canvasGroup.rotation.x = -0.08; // Tilt canvas backward by ~4.5 degrees
scene.add(canvasGroup);
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
// Magnifying Glass Setup
let magActive = false;
let showSupertitles = true;
const magRenderTarget = new THREE.WebGLRenderTarget(512, 512);
const magCamera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
magCamera.position.z = 2.5; // Zoomed in tight for maximum detail

const uiScene = new THREE.Scene();
const uiCamera = new THREE.OrthographicCamera(window.innerWidth / -2, window.innerWidth / 2, window.innerHeight / 2, window.innerHeight / -2, 1, 10);
uiCamera.position.z = 5;

const lensGeo = new THREE.CircleGeometry(150, 64);
const lensMat = new THREE.MeshBasicMaterial({ map: magRenderTarget.texture });
const lensMesh = new THREE.Mesh(lensGeo, lensMat);

const lensBorderGeo = new THREE.RingGeometry(150, 153, 64);
const lensBorderMat = new THREE.MeshBasicMaterial({ color: 0xd6a848 });
const lensBorder = new THREE.Mesh(lensBorderGeo, lensBorderMat);

lensMesh.add(lensBorder);
lensMesh.position.set(-9999, -9999, 0);
uiScene.add(lensMesh);


// Calculate the visible width at our starting Z distance to align the left edge of the tapestry with the left of the viewport
const isNarrowScreen = isPhone || (window.innerWidth <= 900 && !isIPad);
const initialZ = isNarrowScreen ? 10.0 : 12.0;
// Coordinate system layout
const floorY = -H / SCALE - 0.5;
const tapestryElevation = 2.0; // Tapestry lowered further
const cameraY = floorY + 6.0; // Viewpoint lowered by half a unit

// Initial setup to frame the start of the tapestry
const initialVFOV = THREE.MathUtils.degToRad(60);
const initialVisibleWidth = 2 * Math.tan(initialVFOV / 2) * initialZ * (window.innerWidth / window.innerHeight);

// Start near the beginning of the tapestry: on mobile, start further right (x=4.8) so Scene 1 is fully visible
const initialX = isNarrowScreen ? 4.8 : (initialVisibleWidth / 2 - 2.0);
camera.position.set(initialX, cameraY, initialZ);

// Disable antialiasing on mobile/tablets with high pixel ratios to save GPU fill rate
const isMobileOrTablet = isPhone || isIPad;
const useAntialias = !isMobileOrTablet || window.devicePixelRatio === 1;
const renderer = new THREE.WebGLRenderer({ antialias: useAntialias, alpha: false });

// Cap pixel ratio to 1.5 on mobile/tablet devices to ensure 60fps scrolling on Retina
const maxPixelRatio = isMobileOrTablet ? Math.min(window.devicePixelRatio, 1.5) : window.devicePixelRatio;
renderer.setPixelRatio(maxPixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const textureLoader = new THREE.TextureLoader();
textureLoader.setCrossOrigin('anonymous');
const tiles = [];

// Use visible: false instead of transparent/opacity to prevent mobile WebGL from trying to depth-sort 700 transparent planes
const emptyMaterial = new THREE.MeshLambertMaterial({ visible: false });

// Strict network queue to prevent Safari/iPad from stalling when requesting many tiles
let activeRequests = 0;
const MAX_CONCURRENT_REQUESTS = isPhone ? 8 : 32;

// Share a single base geometry across ALL tiles to massively reduce WebGL memory overhead (prevents mobile Chrome crashes)
const baseGeometry = new THREE.PlaneGeometry(1, 1);

// Create the meshes for all tiles, but don't load textures yet
for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
        const x_topLeft = c === 0 ? 0 : c * T - 1;
        const y_topLeft = r === 0 ? 0 : r * T - 1;

        const w = (c === cols - 1) ? (W - x_topLeft) : (T + (c === 0 ? 0 : 1) + 1);
        const h = (r === rows - 1) ? (H - y_topLeft) : (T + (r === 0 ? 0 : 1) + 1);

        const widthUnits = w / SCALE;
        const heightUnits = h / SCALE;

        const xCenter = (x_topLeft + w / 2) / SCALE;
        const yCenter = -(y_topLeft + h / 2) / SCALE + tapestryElevation;

        // Alternate Z slightly to prevent Z-fighting from the 1px overlap
        const zOffset = (c % 2) * 0.001 + (r % 2) * 0.002;

        // Use the shared empty material and scale the 1x1 geometry
        const mesh = new THREE.Mesh(baseGeometry, emptyMaterial);
        mesh.scale.set(widthUnits, heightUnits, 1);
        mesh.position.set(xCenter, yCenter, zOffset);
        canvasGroup.add(mesh);

        tiles.push({
            c, r,
            xCenter,
            mesh: mesh,
            loaded: false,
            loading: false,
            failed: false
        });
    }
}

const tilesL17 = [];
const W17 = W * 2;
const H17 = H * 2;
const cols17 = Math.ceil(W17 / T);
const rows17 = Math.ceil(H17 / T);

for (let r = 0; r < rows17; r++) {
    for (let c = 0; c < cols17; c++) {
        const x_topLeft = c === 0 ? 0 : c * T - 1;
        const y_topLeft = r === 0 ? 0 : r * T - 1;

        const w = (c === cols17 - 1) ? (W17 - x_topLeft) : (T + (c === 0 ? 0 : 1) + 1);
        const h = (r === rows17 - 1) ? (H17 - y_topLeft) : (T + (r === 0 ? 0 : 1) + 1);

        const widthUnits = (w / SCALE) / 2;
        const heightUnits = (h / SCALE) / 2;

        const xCenter = (x_topLeft + w / 2) / (SCALE * 2);
        const yCenter = -(y_topLeft + h / 2) / (SCALE * 2) + tapestryElevation;

        const zOffset = 0.01 + (c % 2) * 0.001 + (r % 2) * 0.002;

        const mesh = new THREE.Mesh(baseGeometry, emptyMaterial);
        mesh.scale.set(widthUnits, heightUnits, 1);
        mesh.position.set(xCenter, yCenter, zOffset);

        canvasGroup.add(mesh);

        tilesL17.push({
            c, r,
            xCenter,
            mesh: mesh,
            loaded: false,
            loading: false,
            failed: false
        });
    }
}

const tilesL18 = [];
const W18 = W * 4;
const H18 = H * 4;
const cols18 = Math.ceil(W18 / T);
const rows18 = Math.ceil(H18 / T);

for (let r = 0; r < rows18; r++) {
    for (let c = 0; c < cols18; c++) {
        const x_topLeft = c === 0 ? 0 : c * T - 1;
        const y_topLeft = r === 0 ? 0 : r * T - 1;

        const w = (c === cols18 - 1) ? (W18 - x_topLeft) : (T + (c === 0 ? 0 : 1) + 1);
        const h = (r === rows18 - 1) ? (H18 - y_topLeft) : (T + (r === 0 ? 0 : 1) + 1);

        const widthUnits = (w / SCALE) / 4;
        const heightUnits = (h / SCALE) / 4;

        const xCenter = (x_topLeft + w / 2) / (SCALE * 4);
        const yCenter = -(y_topLeft + h / 2) / (SCALE * 4) + tapestryElevation;

        const zOffset = 0.02 + (c % 2) * 0.001 + (r % 2) * 0.002;

        const mesh = new THREE.Mesh(baseGeometry, emptyMaterial);
        mesh.scale.set(widthUnits, heightUnits, 1);
        mesh.position.set(xCenter, yCenter, zOffset);

        canvasGroup.add(mesh);

        tilesL18.push({
            c, r,
            xCenter,
            mesh: mesh,
            loaded: false,
            loading: false,
            failed: false
        });
    }
}
const tilesL19 = [];
const W19 = W * 8;
const H19 = H * 8;
const cols19 = Math.ceil(W19 / T);
const rows19 = Math.ceil(H19 / T);

for (let r = 0; r < rows19; r++) {
    for (let c = 0; c < cols19; c++) {
        const x_topLeft = c === 0 ? 0 : c * T - 1;
        const y_topLeft = r === 0 ? 0 : r * T - 1;

        const w = (c === cols19 - 1) ? (W19 - x_topLeft) : (T + (c === 0 ? 0 : 1) + 1);
        const h = (r === rows19 - 1) ? (H19 - y_topLeft) : (T + (r === 0 ? 0 : 1) + 1);

        const widthUnits = (w / SCALE) / 8;
        const heightUnits = (h / SCALE) / 8;

        const xCenter = (x_topLeft + w / 2) / (SCALE * 8);
        const yCenter = -(y_topLeft + h / 2) / (SCALE * 8) + tapestryElevation;

        const zOffset = 0.03 + (c % 2) * 0.001 + (r % 2) * 0.002;

        const mesh = new THREE.Mesh(baseGeometry, emptyMaterial);
        mesh.scale.set(widthUnits, heightUnits, 1);
        mesh.position.set(xCenter, yCenter, zOffset);

        canvasGroup.add(mesh);

        tilesL19.push({
            c, r,
            xCenter,
            mesh: mesh,
            loaded: false,
            loading: false,
            failed: false
        });
    }
}
// Scene background and fog for depth (dark earthy tone)
const fogColor = new THREE.Color(0x161310);
scene.background = fogColor;
// Fog density calibrated so the tapestry remains visible at maximum zoom out distance
// scene.fog = new THREE.FogExp2(fogColor, 0.005);

// Add floor and ceiling for perspective
const ceilingY = (H / SCALE + 0.5) * 3.8; // 9.5-meter cathedral-style vault (35.7 units from floor plinth)
const length = W / SCALE + 100;

/**
 * Generates a procedural noise texture for the floor, ceiling, and walls.
 * @param {number} width - Canvas width
 * @param {number} height - Canvas height
 * @param {string} baseColor - Base fill color
 * @param {boolean} withSplotches - Whether to add large dark organic splotches
 * @returns {THREE.CanvasTexture}
 */
function createOrganicTexture(width = 256, height = 256, baseColor = '#181510', withSplotches = true) {
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = baseColor;
    ctx.fillRect(0, 0, width, height);

    // Add large, soft organic smudges (like old plaster or rough hewn stone)
    if (withSplotches) {
        for (let i = 0; i < 40; i++) {
            ctx.fillStyle = Math.random() > 0.5 ? 'rgba(255, 255, 255, 0.03)' : 'rgba(0, 0, 0, 0.08)';
            ctx.beginPath();
            ctx.arc(Math.random() * width, Math.random() * height, 10 + Math.random() * 60, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    // Grainy noise, increased density and opacity for visible texture
    const noiseCount = (width * height) * 0.8;
    for (let i = 0; i < noiseCount; i++) {
        const isLight = Math.random() > 0.80;
        ctx.fillStyle = isLight ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.4)';
        ctx.fillRect(Math.random() * width, Math.random() * height, 1, 1); // Strictly 1px
    }

    const texture = new THREE.CanvasTexture(canvas);
    return texture;
}

function createStoneTileTexture(width = 512, height = 512, baseColor = '#050403') {
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = baseColor;
    ctx.fillRect(0, 0, width, height);

    // Large Museum Tiles
    const gridSize = 4;
    const tileW = width / gridSize;
    const tileH = height / gridSize;

    for (let r = 0; r < gridSize; r++) {
        for (let c = 0; c < gridSize; c++) {
            // Random subtle brightness variation per tile for natural slate look
            const intensity = Math.random() * 0.015;
            ctx.fillStyle = `rgba(255, 255, 255, ${intensity})`;
            ctx.fillRect(c * tileW, r * tileH, tileW, tileH);
        }
    }

    // Draw Grout Lines
    ctx.fillStyle = 'rgba(0, 0, 0, 1.0)'; // Pitch black grout
    const groutThickness = 3;

    for (let i = 0; i <= gridSize; i++) {
        // Horizontal grout
        ctx.fillRect(0, i * tileH - groutThickness / 2, width, groutThickness);
        // Vertical grout
        ctx.fillRect(i * tileW - groutThickness / 2, 0, groutThickness, height);
    }

    // Subtle highlight edge on the tiles for 3D depth
    ctx.fillStyle = 'rgba(255, 255, 255, 0.03)';
    for (let i = 0; i < gridSize; i++) {
        // Top highlight
        ctx.fillRect(0, i * tileH + groutThickness / 2, width, 1);
        // Left highlight
        ctx.fillRect(i * tileW + groutThickness / 2, 0, 1, height);
    }

    // Grainy noise over everything
    const noiseCount = (width * height) * 0.3;
    for (let i = 0; i < noiseCount; i++) {
        ctx.fillStyle = Math.random() > 0.5 ? 'rgba(255,255,255,0.015)' : 'rgba(0,0,0,0.5)';
        ctx.fillRect(Math.random() * width, Math.random() * height, 1, 1);
    }

    return new THREE.CanvasTexture(canvas);
}

// Museum stone tile texture with a grid profile
const floorTexture = createStoneTileTexture(512, 512, '#0d0d0d');
floorTexture.wrapS = THREE.RepeatWrapping;
floorTexture.wrapT = THREE.RepeatWrapping;
floorTexture.repeat.set(length / 24, 120 / 24);

const ceilingTexture = createOrganicTexture(512, 512, '#121212', false);
ceilingTexture.wrapS = THREE.RepeatWrapping;
ceilingTexture.wrapT = THREE.RepeatWrapping;
ceilingTexture.repeat.set(length / 5, 120 / 5);

// Dark base wall color creates a dramatic contrast with the illuminated tapestry
const wallTexture = createOrganicTexture(512, 512, '#161616', true);
wallTexture.wrapS = THREE.RepeatWrapping;
wallTexture.wrapT = THREE.RepeatWrapping;
wallTexture.repeat.set(length / 50, 120 / 50);

// Depth set to 120 so the floor and ceiling don't clip when the camera zooms out to Z=40
const planeGeo = new THREE.PlaneGeometry(length, 120);

// Use MeshPhongMaterial (per-pixel lighting) instead of Lambert (per-vertex).
// Since these are massive planes with only 4 vertices at the corners, Lambert will ignore point lights in the middle!
const floorMat = new THREE.MeshPhongMaterial({ map: floorTexture, shininess: 5 });
const ceilingMat = new THREE.MeshPhongMaterial({ map: ceilingTexture, shininess: 4 });
const wallMat = new THREE.MeshPhongMaterial({ map: wallTexture, shininess: 12 });

const floor = new THREE.Mesh(planeGeo, floorMat);
floor.rotation.x = -Math.PI / 2;
floor.position.set((W / SCALE) / 2, floorY, 0);
scene.add(floor);

const ceiling = new THREE.Mesh(planeGeo, ceilingMat);
ceiling.rotation.x = Math.PI / 2;
ceiling.position.set((W / SCALE) / 2, ceilingY, 0);
scene.add(ceiling);

// Add stone wall just behind the tapestry
const wallGeo = new THREE.PlaneGeometry(length, 120);
const backWall = new THREE.Mesh(wallGeo, wallMat);
backWall.position.set((W / SCALE) / 2, tapestryElevation, -0.5); // 0.5 units (6 inches) behind the tapestry (which is at Z=0)
canvasGroup.add(backWall);

// Add a chamfered plinth course at the base of the wall
const plinthHeight = 0.4;
const plinthDepth = 0.2;
const chamferSize = 0.075;

const plinthShape = new THREE.Shape();
plinthShape.moveTo(0, 0);
plinthShape.lineTo(0, plinthHeight);
plinthShape.lineTo(-(plinthDepth - chamferSize), plinthHeight); // Flat top
plinthShape.lineTo(-plinthDepth, plinthHeight - chamferSize); // Chamfer slope
plinthShape.lineTo(-plinthDepth, 0); // Front face down
plinthShape.lineTo(0, 0);

const plinthGeo = new THREE.ExtrudeGeometry(plinthShape, {
    depth: length,
    bevelEnabled: false
});

// Clone the texture to fix the UV scaling on the small profile
const plinthTexture = wallTexture.clone();
plinthTexture.needsUpdate = true;
plinthTexture.repeat.set(length / 2, 2);
const plinthMat = new THREE.MeshLambertMaterial({ map: plinthTexture });

const plinth = new THREE.Mesh(plinthGeo, plinthMat);
// Rotate 90 degrees around Y so the extrusion goes along the X axis
plinth.rotation.y = Math.PI / 2;
// Position at the left edge of the wall, on the floor, flush with the wall
plinth.position.set((W / SCALE) / 2 - length / 2, floorY, -0.5);
canvasGroup.add(plinth);

// --- 3D ARCHITECTURAL TAPESTRY SUPPORTS (LEFT & RIGHT) ---
// Provides physical museum vitrine framing and cantilever wall supports along both edges
// Textured in realistic matte blackened steel and dark black-oxide architectural metal (no distracting brass)
function createBlackIronTexture(width = 256, height = 256) {
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');

    // Matte dark charcoal / graphite base (distinguishable from the #161616 wall)
    ctx.fillStyle = '#262422';
    ctx.fillRect(0, 0, width, height);

    // Directional brushed grain along extrusion axis
    for (let i = 0; i < 700; i++) {
        const x = Math.random() * width;
        const len = 15 + Math.random() * 70;
        const y = Math.random() * height;
        const isLight = Math.random() > 0.45;
        const alpha = isLight ? (0.02 + Math.random() * 0.04) : (0.04 + Math.random() * 0.06);
        ctx.strokeStyle = isLight ? ('rgba(255,255,255,' + alpha + ')') : ('rgba(0,0,0,' + alpha + ')');
        ctx.lineWidth = 1 + Math.random() * 1.5;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x, y + len);
        ctx.stroke();
    }

    // Fine cast-iron stippling / micro-pitting
    const count = (width * height) * 0.3;
    for (let i = 0; i < count; i++) {
        const val = Math.random() > 0.65 ? 'rgba(255,255,255,0.03)' : 'rgba(0,0,0,0.5)';
        ctx.fillStyle = val;
        ctx.fillRect(Math.random() * width, Math.random() * height, 1, 1);
    }

    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(1, 3);
    return tex;
}

function createIronBumpTexture(width = 256, height = 256) {
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#808080';
    ctx.fillRect(0, 0, width, height);

    // Striations for micro-relief
    for (let i = 0; i < 400; i++) {
        const x = Math.random() * width;
        const len = 15 + Math.random() * 60;
        const y = Math.random() * height;
        const shade = Math.random() > 0.5 ? 'rgba(255,255,255,0.07)' : 'rgba(0,0,0,0.09)';
        ctx.strokeStyle = shade;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x, y + len);
        ctx.stroke();
    }

    // Roughness noise
    for (let i = 0; i < (width * height) * 0.3; i++) {
        ctx.fillStyle = Math.random() > 0.5 ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)';
        ctx.fillRect(Math.random() * width, Math.random() * height, 1, 1);
    }

    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(1, 3);
    return tex;
}

const blackIronTexture = createBlackIronTexture();
const ironBumpTexture = createIronBumpTexture();

// Matte blackened structural steel with subtle satin response
const blackSteelMat = new THREE.MeshPhongMaterial({
    map: blackIronTexture,
    bumpMap: ironBumpTexture,
    bumpScale: 0.02,
    color: 0x2a2825,
    specular: 0x55504a,
    shininess: 30
});

// Subtle burnished graphite edge-highlight material for crisp architectural rim-lighting
const edgeHighlightMat = new THREE.MeshPhongMaterial({
    color: 0x2a2823,
    specular: 0x46423c,
    shininess: 45
});

// Dedicated bottom rail edge-highlight material (balanced brightness)
const bottomEdgeHighlightMat = new THREE.MeshPhongMaterial({
    color: 0x1d1c17,
    specular: 0x302d2a,
    shininess: 45
});

// Dark black oxide / gunmetal for hardware, bolts, flanges, and tie-rods
const blackOxideMat = new THREE.MeshPhongMaterial({
    map: blackIronTexture,
    bumpMap: ironBumpTexture,
    bumpScale: 0.015,
    color: 0x111111,
    specular: 0x4d4d4d,
    shininess: 45
});

// Architectural cantilever bracket and floor foundation under the bottom rail
// Simple, realistic design shared identically by the left, right, and intermediate supports
function createUnderSupport(xPos) {
    const group = new THREE.Group();
    const colWidth = 0.14;

    // 1. Horizontal shelf cradling the bottom edge of the tapestry
    const shelfDepth = 0.68;
    const shelfHeight = 0.14;
    const shelfGeo = new THREE.BoxGeometry(colWidth * 1.5, shelfHeight, shelfDepth);
    const shelfMesh = new THREE.Mesh(shelfGeo, blackSteelMat);
    shelfMesh.position.set(xPos, -5.01, -0.16);
    group.add(shelfMesh);

    // 2. Front lip on shelf preventing fabric board from sliding forward
    const frontLipGeo = new THREE.BoxGeometry(colWidth * 1.5, 0.20, 0.06);
    const frontLip = new THREE.Mesh(frontLipGeo, blackSteelMat);
    frontLip.position.set(xPos, -4.89, 0.15);
    group.add(frontLip);

    // Subtle edge highlight on the front lip
    const frontLipHlGeo = new THREE.BoxGeometry(colWidth * 1.52, 0.010, 0.010);
    const frontLipHl = new THREE.Mesh(frontLipHlGeo, bottomEdgeHighlightMat);
    frontLipHl.position.set(xPos, -4.79, 0.175);
    group.add(frontLipHl);

    // 3. Heavy diagonal knee-brace strut underneath the bottom shelf
    // Connects from back wall at Y = -5.85, Z = -0.48 to shelf front at Y = -5.08, Z = 0.08
    const strutLen = 0.98;
    const strutGeo = new THREE.CylinderGeometry(0.065, 0.065, strutLen, 16);
    const strutMesh = new THREE.Mesh(strutGeo, blackSteelMat);
    const angleKnee = Math.atan2(0.56, 0.77); // Angle between Y and Z
    strutMesh.rotation.x = angleKnee;
    strutMesh.position.set(xPos, -5.46, -0.20);
    group.add(strutMesh);

    // 4. Knee-brace wall anchor base plate
    const kneeBaseGeo = new THREE.BoxGeometry(colWidth * 1.4, 0.35, 0.05);
    const kneeBase = new THREE.Mesh(kneeBaseGeo, blackSteelMat);
    kneeBase.position.set(xPos, -5.85, -0.475);
    group.add(kneeBase);

    // Wall mounting flange disc and bolt
    const wallFlangeGeo = new THREE.CylinderGeometry(0.09, 0.09, 0.025, 16);
    const wallFlange = new THREE.Mesh(wallFlangeGeo, blackOxideMat);
    wallFlange.rotation.x = Math.PI / 2;
    wallFlange.position.set(xPos, -5.85, -0.485);
    group.add(wallFlange);

    const wallBoltGeo = new THREE.CylinderGeometry(0.02, 0.02, 0.02, 8);
    const wallBolt = new THREE.Mesh(wallBoltGeo, blackOxideMat);
    wallBolt.rotation.x = Math.PI / 2;
    wallBolt.position.set(xPos, -5.85, -0.47);
    group.add(wallBolt);

    // 5. Vertical Foundation Column extending down to the Floor/Plinth
    // Grounding the cantilever load into the museum floor plinth
    const postHeight = 1.60;
    const postGeo = new THREE.BoxGeometry(colWidth * 1.1, postHeight, 0.16);
    const postMesh = new THREE.Mesh(postGeo, blackSteelMat);
    postMesh.position.set(xPos, -6.65, -0.45);
    group.add(postMesh);

    // 6. Pedestal base plate on the floor
    const pedestalBaseGeo = new THREE.BoxGeometry(colWidth * 1.8, 0.08, 0.28);
    const pedestalBase = new THREE.Mesh(pedestalBaseGeo, blackSteelMat);
    pedestalBase.position.set(xPos, -7.40, -0.45);
    group.add(pedestalBase);

    return group;
}

function createSideSupport(isRightSide) {
    const supportGroup = new THREE.Group();
    const xEdge = isRightSide ? (W / SCALE) : 0;
    const dir = isRightSide ? 1 : -1; // Outward direction: +1 on right, -1 on left

    const colWidth = 0.14;
    const colHeight = 7.18; // Covers the full height plus top/bottom overlaps
    const colDepth = 0.58;  // Spans from back wall (Z = -0.50) to slightly past tapestry (Z = +0.08)
    const colCenterX = xEdge + dir * (colWidth / 2);
    const colCenterY = -1.47;
    const colCenterZ = -0.21; // Midpoint between -0.50 and +0.08

    // 1. Heavy Vertical Stanchion Channel (Side Beam)
    const colGeo = new THREE.BoxGeometry(colWidth, colHeight, colDepth);
    const colMesh = new THREE.Mesh(colGeo, blackSteelMat);
    colMesh.position.set(colCenterX, colCenterY, colCenterZ);
    supportGroup.add(colMesh);

    // 2. Front Retaining Bezel / Edge Clamp (physically overlaps front of tapestry)
    const bezelWidth = 0.09;
    const bezelHeight = colHeight;
    const bezelDepth = 0.05;
    const bezelGeo = new THREE.BoxGeometry(bezelWidth, bezelHeight, bezelDepth);
    const bezelMesh = new THREE.Mesh(bezelGeo, blackSteelMat);
    // Positions over the front edge of the tapestry
    bezelMesh.position.set(xEdge - dir * (bezelWidth / 2), colCenterY, 0.045);
    supportGroup.add(bezelMesh);

    // Subtle vertical edge highlight on the front bezel rim
    const sideBezelHighlightGeo = new THREE.BoxGeometry(0.014, bezelHeight, 0.014);
    const sideBezelHighlight = new THREE.Mesh(sideBezelHighlightGeo, edgeHighlightMat);
    sideBezelHighlight.position.set(xEdge, colCenterY, 0.07);
    supportGroup.add(sideBezelHighlight);

    // 3. Top Stanchion Cap & Corner Joint
    const topCapGeo = new THREE.BoxGeometry(colWidth * 1.35, 0.10, colDepth * 1.08);
    const topCap = new THREE.Mesh(topCapGeo, blackSteelMat);
    topCap.position.set(colCenterX, 2.16, colCenterZ);
    supportGroup.add(topCap);

    // Black oxide corner reinforcement block on top
    const topBlockGeo = new THREE.BoxGeometry(0.12, 0.12, 0.14);
    const topBlock = new THREE.Mesh(topBlockGeo, blackOxideMat);
    topBlock.position.set(colCenterX, 2.10, 0.04);
    supportGroup.add(topBlock);

    // 4. Bottom Load-Bearing Shelf & Cantilever Arm + Foundation Column
    supportGroup.add(createUnderSupport(colCenterX));

    // 5. Wall Standoff Flanges & Heavy Fastener Bolts
    const standoffHeights = [1.55, -1.47, -4.20];
    standoffHeights.forEach((posY) => {
        // Wall mounting flange (round black-oxide disc flush on stone wall)
        const flangeGeo = new THREE.CylinderGeometry(0.11, 0.11, 0.03, 16);
        const flange = new THREE.Mesh(flangeGeo, blackOxideMat);
        flange.rotation.x = Math.PI / 2;
        flange.position.set(colCenterX, posY, -0.485);
        supportGroup.add(flange);

        // Connecting standoff boss/hub
        const hubGeo = new THREE.CylinderGeometry(0.045, 0.045, 0.12, 12);
        const hub = new THREE.Mesh(hubGeo, blackSteelMat);
        hub.rotation.x = Math.PI / 2;
        hub.position.set(colCenterX, posY, -0.42);
        supportGroup.add(hub);

        // Outer side clamping bolts on the stanchion face
        const sideBoltGeo = new THREE.CylinderGeometry(0.022, 0.022, 0.03, 8);
        const sideBolt = new THREE.Mesh(sideBoltGeo, blackOxideMat);
        sideBolt.rotation.z = Math.PI / 2;
        sideBolt.position.set(xEdge + dir * (colWidth + 0.01), posY, -0.15);
        supportGroup.add(sideBolt);

        const sideBolt2 = new THREE.Mesh(sideBoltGeo, blackOxideMat);
        sideBolt2.rotation.z = Math.PI / 2;
        sideBolt2.position.set(xEdge + dir * (colWidth + 0.01), posY, -0.32);
        supportGroup.add(sideBolt2);
    });


    return supportGroup;
}

const leftSupport = createSideSupport(false);
canvasGroup.add(leftSupport);

const rightSupport = createSideSupport(true);
canvasGroup.add(rightSupport);

// --- CONTINUOUS TOP & BOTTOM VITRINE RAILS ---
// Spans the full 70m length of the tapestry, creating a cohesive blackened steel frame
const railLength = W / SCALE;
const railCenterX = (W / SCALE) / 2;

const railTex = blackIronTexture.clone();
railTex.needsUpdate = true;
railTex.repeat.set(railLength / 2, 1);

const railBump = ironBumpTexture.clone();
railBump.needsUpdate = true;
railBump.repeat.set(railLength / 2, 1);

const railMat = new THREE.MeshPhongMaterial({
    map: railTex,
    bumpMap: railBump,
    bumpScale: 0.02,
    color: 0x2a2825,
    specular: 0x55504a,
    shininess: 30
});

// 1. TOP RAIL (caps the top edge of the tapestry and meets the stone wall)
const topRailBeamGeo = new THREE.BoxGeometry(railLength, 0.10, 0.56);
const topRailBeam = new THREE.Mesh(topRailBeamGeo, railMat);
topRailBeam.position.set(railCenterX, 2.05, -0.22);
canvasGroup.add(topRailBeam);

const topRailLipGeo = new THREE.BoxGeometry(railLength, 0.06, 0.04);
const topRailLip = new THREE.Mesh(topRailLipGeo, railMat);
topRailLip.position.set(railCenterX, 1.98, 0.05);
canvasGroup.add(topRailLip);

// Top rail bottom edge highlight (delineates top edge of tapestry)
const topHighlightGeo = new THREE.BoxGeometry(railLength, 0.014, 0.014);
const topHighlight = new THREE.Mesh(topHighlightGeo, edgeHighlightMat);
topHighlight.position.set(railCenterX, 1.95, 0.07);
canvasGroup.add(topHighlight);

// 2. BOTTOM RAIL (load-bearing shelf cradling the tilted tapestry bottom with retaining lip)
const bottomRailShelfGeo = new THREE.BoxGeometry(railLength, 0.12, 0.60);
const bottomRailShelf = new THREE.Mesh(bottomRailShelfGeo, railMat);
bottomRailShelf.position.set(railCenterX, -5.00, -0.20);
canvasGroup.add(bottomRailShelf);

const bottomRailLipGeo = new THREE.BoxGeometry(railLength, 0.14, 0.05);
const bottomRailLip = new THREE.Mesh(bottomRailLipGeo, railMat);
bottomRailLip.position.set(railCenterX, -4.92, 0.09);
canvasGroup.add(bottomRailLip);

// Bottom rail top edge highlight (delineates bottom edge of tapestry where it rests on the shelf)
const bottomHighlightGeo = new THREE.BoxGeometry(railLength, 0.010, 0.010);
const bottomHighlight = new THREE.Mesh(bottomHighlightGeo, bottomEdgeHighlightMat);
bottomHighlight.position.set(railCenterX, -4.85, 0.115);
canvasGroup.add(bottomHighlight);

// Bottom rail shelf bottom edge highlight (delineates bottom rail from the wall drop shadow)
const bottomShelfHighlightGeo = new THREE.BoxGeometry(railLength, 0.010, 0.010);
const bottomShelfHighlight = new THREE.Mesh(bottomShelfHighlightGeo, bottomEdgeHighlightMat);
bottomShelfHighlight.position.set(railCenterX, -5.06, 0.10);
canvasGroup.add(bottomShelfHighlight);

// --- PERIODIC VERTICAL SUPPORTS UNDER THE TAPESTRY ---
// Architectural cantilever knee-brace stanchions (same design as left/right endcaps)

// Place periodic vertical supports every ~3.5 meters (~30.13 units) across the 70m tapestry
const tapestryLength = W / SCALE;
const numBays = 20; // 20 bays (~3.5 meters / ~11.5 ft spacing) for convincing structural rhythm
const supportSpacing = tapestryLength / numBays;

for (let i = 1; i < numBays; i++) {
    const xPos = i * supportSpacing;
    const underSupport = createUnderSupport(xPos);
    canvasGroup.add(underSupport);
}



// Lighting: Ambient light + Key Light
const ambientLight = new THREE.AmbientLight(0xffffff, 0.73);
scene.add(ambientLight);


const dirLight = new THREE.DirectionalLight(0xffffff, 0.0); // Start at 0 for cinematic reveal
scene.add(dirLight);

let revealLight = new THREE.SpotLight(0xffeeba, 0.0, 40, Math.PI / 12, 1.0, 2); // Cinematic intro spotlight

// Dedicated grazing light that follows the magnifying glass
// Dedicated grazing light that follows the magnifying glass
const magLight = new THREE.SpotLight(0xffb84d, 0.4, 10, 35 * Math.PI / 180, 1.0, 2);
magLight.visible = false;
scene.add(magLight);
scene.add(magLight.target); // Required for SpotLight target tracking




ambientLight.intensity = 0.02;
if (useSimpleLighting) {
    ambientLight.color.setHex(0xffffff);
}

// Sync initial UI slider value
const simpleLightToggle = document.getElementById('simple-lighting-toggle');
if (simpleLightToggle) simpleLightToggle.checked = useSimpleLighting;

document.getElementById('amb-int').value = ambientLight.intensity;
document.getElementById('val-amb-int').innerText = ambientLight.intensity.toFixed(2);
const ambColorInput = document.getElementById('amb-color');
if (ambColorInput) ambColorInput.value = '#' + ambientLight.color.getHexString();

const keyIntInput = document.getElementById('key-int');
if (keyIntInput) keyIntInput.value = dirLight.intensity;
const valKeyInt = document.getElementById('val-key-int');
if (valKeyInt) valKeyInt.innerText = dirLight.intensity.toFixed(2);
const keyColorInput = document.getElementById('key-color');
if (keyColorInput) keyColorInput.value = '#' + dirLight.color.getHexString();

// UI Listeners
if (simpleLightToggle) {
    simpleLightToggle.addEventListener('change', (e) => {
        useSimpleLighting = e.target.checked;

        // Update lighting setup
        ambientLight.intensity = 1.06;
        ambientLight.color.setHex(0xffffff);

        // Sync UI
        document.getElementById('amb-int').value = ambientLight.intensity;
        document.getElementById('val-amb-int').innerText = ambientLight.intensity.toFixed(2);
        if (ambColorInput) ambColorInput.value = '#' + ambientLight.color.getHexString();

        // Rebuild materials for all currently loaded tiles
        const allTileArrays = [tiles, tilesL17, tilesL18, tilesL19];
        allTileArrays.forEach(arr => {
            arr.forEach(t => {
                if (t.mesh && t.mesh.material && t.mesh.material.map) {
                    const matOpts = {
                        map: t.mesh.material.map,
                        transparent: true,
                        opacity: t.mesh.material.opacity
                    };
                    t.mesh.material.dispose(); // Important for memory!
                    if (useSimpleLighting) {
                        t.mesh.material = new THREE.MeshLambertMaterial(matOpts);
                    } else {
                        matOpts.roughness = 0.85;
                        matOpts.metalness = 0.0;
                        matOpts.bumpMap = t.mesh.material.map;
                        matOpts.bumpScale = parseFloat(document.getElementById('bump-scale').value);
                        t.mesh.material = new THREE.MeshStandardMaterial(matOpts);
                    }
                }
            });
        });
    });
}

// Update ambient light intensity in real-time from the lighting dev panel
document.getElementById('amb-int').addEventListener('input', (e) => {
    ambientLight.intensity = parseFloat(e.target.value);
    document.getElementById('val-amb-int').innerText = ambientLight.intensity.toFixed(2);
});

// Update ambient light color in real-time from the lighting dev panel

document.getElementById('bump-scale').addEventListener('input', (e) => {
    const val = parseFloat(e.target.value);
    document.getElementById('val-bump-scale').innerText = val.toFixed(3);
    const allTileArrays = [tiles, tilesL17, tilesL18, tilesL19];
    allTileArrays.forEach(arr => {
        arr.forEach(t => {
            if (t.mesh && t.mesh.material && t.mesh.material.bumpScale !== undefined) {
                t.mesh.material.bumpScale = val;
                t.mesh.material.needsUpdate = true;
            }
        });
    });
});

document.getElementById('amb-color').addEventListener('input', (e) => {
    ambientLight.color.set(e.target.value);
});

if (keyIntInput) keyIntInput.addEventListener('input', e => {
    dirLight.intensity = parseFloat(e.target.value);
    if (valKeyInt) valKeyInt.innerText = dirLight.intensity.toFixed(2);
});
if (keyColorInput) keyColorInput.addEventListener('input', e => {
    dirLight.color.set(e.target.value);
});

/**
 * Creates a subtle linear gradient texture to simulate ambient occlusion / shadow
 * beneath the 3D tapestry mesh.
 * @returns {THREE.CanvasTexture}
 */
function createShadowTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');

    const gradient = ctx.createLinearGradient(0, 0, 0, 64);
    gradient.addColorStop(0, 'rgba(0,0,0,0.6)'); // Much darker core shadow to anchor it
    gradient.addColorStop(0.2, 'rgba(0,0,0,0.6)');
    gradient.addColorStop(1, 'rgba(0,0,0,0)');

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 1, 64);

    return new THREE.CanvasTexture(canvas);
}

const shadowHeight = 1.1; // Reduced drop shadow height slightly
const shadowGeo = new THREE.PlaneGeometry(W / SCALE, shadowHeight);
const shadowMat = new THREE.MeshBasicMaterial({
    map: createShadowTexture(),
    transparent: true,
    depthWrite: false
});
const shadowMesh = new THREE.Mesh(shadowGeo, shadowMat);
// Position it so its top edge touches the bottom of the tapestry, but pushed back onto the wall
shadowMesh.position.set((W / SCALE) / 2, -H / SCALE - (shadowHeight / 2) + tapestryElevation, -0.48);
canvasGroup.add(shadowMesh);

// Add a top shadow to simulate ambient occlusion / thickness where it meets the wall
const topShadowMesh = new THREE.Mesh(shadowGeo, shadowMat);
topShadowMesh.rotation.z = Math.PI; // Flip it upside down
topShadowMesh.scale.y = 0.33; // Significantly reduce the size of the top shadow
topShadowMesh.position.set((W / SCALE) / 2, 0 + (shadowHeight * 0.33 / 2) + tapestryElevation, -0.48);
canvasGroup.add(topShadowMesh);

// Input state
const keys = {
    left: false, right: false,
    up: false, down: false
};
let mouseScrollDir = 0;
let isTouch = false;

let lastTouchX = 0;
let lastTouchY = 0;
let isDragging = false;
let initialPinchDistance = 0;
let initialPinchCamZ = 0;
let lastPinchMidX = 0;
let lastPinchMidY = 0;

let hasTouchDragged = false;

// Initialize touch tracking, halt any existing momentum, and handle raycasting for Authoring mode drags.
window.addEventListener('touchstart', (e) => {
    if (e.target.closest('#ui') || e.target.closest('#lighting-dialog') || e.target.closest('#about-dialog') || e.target.closest('#context-scroll') || e.target.closest('#tour-control-bar') || e.target.closest('#mobile-tour-btn') || e.target.closest('#mobile-menu') || e.target.closest('#mobile-menu-scrim') || e.target.closest('#hamburger-btn')) return;
    isTouch = true;
    hasTouchDragged = false;
    mouseScrollDir = 0;
    autoScrollTargetX = null;
    autoScrollTargetZ = null; autoScrollTargetY = null;

    if (e.touches.length === 1) {
        if (isAuthoringMode) {
            mouseCoords.x = (e.touches[0].clientX / window.innerWidth) * 2 - 1;
            mouseCoords.y = -(e.touches[0].clientY / window.innerHeight) * 2 + 1;
            dragRaycaster.setFromCamera(mouseCoords, camera);
            const annMeshes = annotations.map(a => a.mesh).filter(m => m && m.visible);
            const intersects = dragRaycaster.intersectObjects(annMeshes, false);
            if (intersects.length > 0) {
                draggedAnnotation = intersects[0].object.userData.annotation;
                return; // Prevent panning
            }
        }
        isDragging = true;
        lastTouchX = e.touches[0].clientX;
        lastTouchY = e.touches[0].clientY;
        velocityX = 0; // Halt existing momentum
        velocityY = 0;
    } else if (e.touches.length === 2) {
        isDragging = false;
        const dx = e.touches[0].clientX - e.touches[1].clientX;
        const dy = e.touches[0].clientY - e.touches[1].clientY;
        initialPinchDistance = Math.sqrt(dx * dx + dy * dy);
        initialPinchCamZ = camera.position.z;
        lastPinchMidX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        lastPinchMidY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
        velocityZ = 0;
        velocityY = 0;
    }
}, { passive: false });

// Handle 1-finger panning and 2-finger pinch-to-zoom for mobile devices.
window.addEventListener('touchmove', (e) => {
    if (e.target.closest('#ui') || e.target.closest('#lighting-dialog') || e.target.closest('#about-dialog') || e.target.closest('#context-scroll') || e.target.closest('#tour-control-bar') || e.target.closest('#mobile-tour-btn') || e.target.closest('#mobile-menu') || e.target.closest('#mobile-menu-scrim') || e.target.closest('#hamburger-btn')) return;
    hasTouchDragged = true;
    if (!isTouch) return;

    if (draggedAnnotation && e.touches.length === 1) {
        e.preventDefault();
        mouseCoords.x = (e.touches[0].clientX / window.innerWidth) * 2 - 1;
        mouseCoords.y = -(e.touches[0].clientY / window.innerHeight) * 2 + 1;
        dragRaycaster.setFromCamera(mouseCoords, camera);
        const intersects = dragRaycaster.intersectObjects(scene.children, true);
        if (intersects.length > 0) {
            const localPoint = canvasGroup.worldToLocal(intersects[0].point.clone());
            draggedAnnotation.data.x = localPoint.x;
            draggedAnnotation.data.y = localPoint.y;
            if (typeof updateAnnotations === 'function') updateAnnotations();
        }
        return;
    }

    if (e.touches.length === 1 && isDragging) {
        e.preventDefault(); // Prevent native browser scrolling/bounce

        const currentTouchX = e.touches[0].clientX;
        const currentTouchY = e.touches[0].clientY;
        const dx = currentTouchX - lastTouchX;
        const dy = currentTouchY - lastTouchY;
        if (Math.abs(dx) > 6) {
            isSceneDwell = false; // Cancel dwell on user interaction
        }

        // 1:1 pixel-to-world drag ratio based on current camera Z distance and 45deg FOV
        const pixelToWorld = (0.828 * camera.position.z) / window.innerHeight;
        const moveWorldX = -dx * pixelToWorld;

        // Vertical dragging is disabled on mobile devices for stability
        camera.position.x += moveWorldX;

        // Store recent movement as velocity for native-feeling momentum on release
        // Apply heavy smoothing (0.5 blend) to prevent touch-polling rate jitter from causing twitchy spikes
        velocityX = velocityX * 0.5 + (moveWorldX * 0.8) * 0.5;
        velocityY = 0; // No vertical velocity on mobile

        lastTouchX = currentTouchX;
        lastTouchY = currentTouchY;
    } else if (e.touches.length === 2) {
        e.preventDefault(); // Prevent native browser pinch-to-zoom
        isSceneDwell = false;

        const dx = e.touches[0].clientX - e.touches[1].clientX;
        const dy = e.touches[0].clientY - e.touches[1].clientY;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (initialPinchDistance > 0) {
            const scale = initialPinchDistance / dist;
            camera.position.z = initialPinchCamZ * scale;
            // Keep camera Z bounded between 0.8 and 60 to prevent zooming out past the floor
            camera.position.z = Math.max(0.9, Math.min(60, camera.position.z));
        }

        // 2-finger omnidirectional panning
        const currentMidX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        const currentMidY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
        if (lastPinchMidX > 0 && lastPinchMidY > 0) {
            const dxMid = currentMidX - lastPinchMidX;
            const dyMid = currentMidY - lastPinchMidY;
            const pixelToWorld = (0.828 * camera.position.z) / window.innerHeight;

            const moveWorldX = -dxMid * pixelToWorld;
            const moveWorldY = dyMid * pixelToWorld;

            camera.position.x += moveWorldX;
            camera.position.y += moveWorldY;

            // Add smooth inertia for omnidirectional panning
            velocityX = velocityX * 0.5 + (moveWorldX * 0.8) * 0.5;
            velocityY = velocityY * 0.5 + (moveWorldY * 0.8) * 0.5;
        }
        lastPinchMidX = currentMidX;
        lastPinchMidY = currentMidY;
    }
}, { passive: false });

// Handle touch release to smoothly transition back to 1-finger drag or apply release momentum.
window.addEventListener('touchend', (e) => {
    if (draggedAnnotation) {
        draggedAnnotation = null;
        localStorage.setItem('bayeux-tituli', JSON.stringify(annotations.map(a => a.data)));
        return;
    }
    mouseScrollDir = 0;
    if (e.touches.length < 2) {
        initialPinchDistance = 0;
        lastPinchMidX = 0;
        lastPinchMidY = 0;
    }
    if (e.touches.length === 1) {
        // If they lift one finger, seamlessly transition back to 1-finger horizontal drag
        isDragging = true;
        lastTouchX = e.touches[0].clientX;
        lastTouchY = e.touches[0].clientY;
    }
    if (e.touches.length === 0) {
        isDragging = false;
        if (!hasTouchDragged && e.changedTouches.length > 0) {
            handleAnnotationClick(e.changedTouches[0].clientX, e.changedTouches[0].clientY, e.target);
        }
    }
});

// Reset touch states if the browser cancels the touch event (e.g., system swipe gesture)
window.addEventListener('touchcancel', () => {
    isDragging = false;
    initialPinchDistance = 0;
});

let isMouseDown = false;
let draggedAnnotation = null;
const dragRaycaster = new THREE.Raycaster();

// Initialize mouse drag tracking, halt momentum, and handle raycasting for Authoring mode.
let mouseStartX = 0;
let mouseStartY = 0;

window.addEventListener('mousedown', (e) => {
    if (isTouch) return;
    mouseStartX = e.clientX;
    mouseStartY = e.clientY;
    autoScrollTargetX = null;
    autoScrollTargetZ = null; autoScrollTargetY = null;
    if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#title') || e.target.closest('#lighting-dialog') || e.target.closest('#about-dialog') || e.target.closest('#context-scroll') || e.target.closest('#tour-control-bar') || e.target.closest('#mobile-tour-btn') || e.target.closest('#mobile-menu') || e.target.closest('#mobile-menu-scrim') || e.target.closest('#hamburger-btn')) return;

    if (isAuthoringMode) {
        mouseCoords.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouseCoords.y = -(e.clientY / window.innerHeight) * 2 + 1;
        dragRaycaster.setFromCamera(mouseCoords, camera);
        const annMeshes = annotations.map(a => a.mesh).filter(m => m && m.visible);
        const intersects = dragRaycaster.intersectObjects(annMeshes, false);
        if (intersects.length > 0) {
            draggedAnnotation = intersects[0].object.userData.annotation;
            document.body.style.cursor = 'grabbing';
            return; // Prevent camera panning
        }
    }
    isMouseDown = true;
    lastTouchX = e.clientX;
    lastTouchY = e.clientY;
    velocityX = 0;
    velocityY = 0;
    document.body.style.cursor = 'grabbing';
});

// Reset mouse dragging state when the mouse button is released anywhere on screen
window.addEventListener('mouseup', (e) => {
    if (draggedAnnotation) {
        draggedAnnotation = null;
        document.body.style.cursor = 'default';
        localStorage.setItem('bayeux-tituli', JSON.stringify(annotations.map(a => a.data)));
        return;
    }
    if (!isTouch && isMouseDown) {
        isMouseDown = false;
        document.body.style.cursor = 'default';
        const dist = Math.hypot(e.clientX - mouseStartX, e.clientY - mouseStartY);
        if (dist < 5) {
            handleAnnotationClick(e.clientX, e.clientY, e.target);
        }
    }
});

// Reset mouse dragging state if the cursor leaves the browser window entirely
window.addEventListener('mouseleave', () => {
    if (!isTouch && isMouseDown) {
        isMouseDown = false;
        document.body.style.cursor = 'default';
    }
});

const mouseCoords = new THREE.Vector2(-9999, -9999);

// Handle desktop mouse dragging (panning) and update normalized mouse coordinates for 3D hover detection.
window.addEventListener('mousemove', (e) => {
    if (isTouch) return;

    // Normalized Device Coordinates (-1 to +1) required by Three.js Raycaster to map 2D screen touches into the 3D scene
    mouseCoords.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouseCoords.y = -(e.clientY / window.innerHeight) * 2 + 1;

    // Update magnifying glass position and camera
    if (magActive) {
        lensMesh.position.x = e.clientX - window.innerWidth / 2;
        lensMesh.position.y = - (e.clientY - window.innerHeight / 2);

        dragRaycaster.setFromCamera(mouseCoords, camera);
        const planeNormal = new THREE.Vector3(0, 0, 1).applyEuler(canvasGroup.rotation);
        const planeZ0 = new THREE.Plane(planeNormal, 0);
        const target = new THREE.Vector3();
        if (dragRaycaster.ray.intersectPlane(planeZ0, target)) {
            magCamera.position.x = target.x;
            magCamera.position.y = target.y;
        }
    }

    if (draggedAnnotation) {
        dragRaycaster.setFromCamera(mouseCoords, camera);
        const intersects = dragRaycaster.intersectObjects(scene.children, true);
        if (intersects.length > 0) {
            const localPoint = canvasGroup.worldToLocal(intersects[0].point.clone());
            draggedAnnotation.data.x = localPoint.x;
            draggedAnnotation.data.y = localPoint.y;
            if (typeof updateAnnotations === 'function') updateAnnotations();
        }
        return;
    }

    if (isMouseDown) {
        e.preventDefault();
        const dx = e.clientX - lastTouchX;
        const dy = e.clientY - lastTouchY;
        if (Math.abs(dx) > 6) {
            isSceneDwell = false; // Cancel dwell on user interaction
        }

        const pixelToWorld = (0.828 * camera.position.z) / window.innerHeight;
        const moveWorldX = -dx * pixelToWorld;
        const moveWorldY = dy * pixelToWorld;

        camera.position.x += moveWorldX;
        camera.position.y += moveWorldY;

        velocityX = moveWorldX * 1.5;
        velocityY = moveWorldY * 1.5;

        lastTouchX = e.clientX;
        lastTouchY = e.clientY;
        mouseScrollDir = 0;
        return;
    }

    // Prevent edge-scroll if hovering over UI elements
    if (e.target.closest('#ui') || e.target.closest('#title') || e.target.closest('#lighting-dialog') || e.target.closest('#about-dialog') || e.target.closest('#tour-control-bar') || e.target.closest('#mobile-tour-btn') || e.target.closest('#mobile-menu') || e.target.closest('#mobile-menu-scrim') || e.target.closest('#hamburger-btn')) {
        mouseScrollDir = 0;
        return;
    }

    const edgeThreshold = window.innerWidth * 0.15; // 15% of screen edge triggers scroll
    if (e.clientX < edgeThreshold) {
        const intensity = 1 - (e.clientX / edgeThreshold);
        mouseScrollDir = -intensity;
    } else if (e.clientX > window.innerWidth - edgeThreshold) {
        const intensity = 1 - ((window.innerWidth - e.clientX) / edgeThreshold);
        mouseScrollDir = intensity;
    } else {
        mouseScrollDir = 0;
    }
});

// Halt edge-scrolling if the mouse leaves the viewport completely
window.addEventListener('mouseout', (e) => {
    if (e.relatedTarget === null) {
        mouseScrollDir = 0;
    }
});

// Fallback to halt edge-scrolling if mouseleave fires on the window
window.addEventListener('mouseleave', () => { mouseScrollDir = 0; });

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
            console.log(`Error attempting to enable fullscreen: ${err.message}`);
        });
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

const fullscreenBtn = document.getElementById('fullscreen-toggle');
if (fullscreenBtn) {
    fullscreenBtn.addEventListener('click', toggleFullscreen);
    document.addEventListener('fullscreenchange', () => {
        if (document.fullscreenElement) {
            fullscreenBtn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"></path></svg>';
        } else {
            fullscreenBtn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg>';
        }
    });
}

const magToggleBtn = document.getElementById('mag-toggle');
const isTouchDevice = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;

// Dynamically toggle help dialog instructions based on device type
if (isPhone || isTouchDevice) {
    document.getElementById('help-desktop-1').style.display = 'none';
    document.getElementById('help-desktop-2').style.display = 'none';
    document.getElementById('help-mobile-1').style.display = 'list-item';
    if (!isPhone) document.getElementById('help-mobile-2').style.display = 'list-item'; // iPad supports popups
}

if (magToggleBtn && (isPhone || isTouchDevice)) {
    magToggleBtn.style.display = 'none';
} else if (magToggleBtn) {
    magToggleBtn.addEventListener('click', () => {
        magActive = !magActive;
        magToggleBtn.style.background = magActive ? 'rgba(214,168,72,0.3)' : 'rgba(20,20,20,0.8)';
        if (!magActive) lensMesh.position.set(-9999, -9999, 0);
    });
}

// Handle keyboard navigation (arrow keys/WASD) and prevent default scrolling behavior.
window.addEventListener('keydown', (e) => {
    if (e.key.toLowerCase() === 'm' && !isPhone) {
        magActive = !magActive;
        if (magToggleBtn) magToggleBtn.style.background = magActive ? 'rgba(214,168,72,0.3)' : 'rgba(20,20,20,0.8)';
        if (!magActive) lensMesh.position.set(-9999, -9999, 0);
    }
    if (e.key === 'Escape' && magActive) {
        magActive = false;
        if (magToggleBtn) magToggleBtn.style.background = 'rgba(20,20,20,0.8)';
        lensMesh.position.set(-9999, -9999, 0);
    }
    if (e.key.toLowerCase() === 'h') {
        const ui = document.getElementById('ui');
        const isHidden = window.getComputedStyle(ui).display === 'none';
        ui.style.display = isHidden ? 'block' : 'none';
    }
    mouseScrollDir = 0; // Prevent mouse edge-scroll from hijacking when releasing keys
    if (e.key === 'ArrowLeft') {
        keys.left = true;
        isSceneDwell = false; // Cancel dwell on user interaction
    }
    if (e.key === 'ArrowRight') {
        keys.right = true;
        isSceneDwell = false; // Cancel dwell on user interaction
    }
    if (e.key === 'ArrowUp') keys.up = true;
    if (e.key === 'ArrowDown') keys.down = true;
});

// Clear keyboard navigation states upon key release.
window.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowLeft') keys.left = false;
    if (e.key === 'ArrowRight') keys.right = false;
    if (e.key === 'ArrowUp') keys.up = false;
    if (e.key === 'ArrowDown') keys.down = false;
});

// UI Button Controls
const setupButton = (id, keyName) => {
    const btn = document.getElementById(id);
    if (!btn) return;
    const start = (e) => { e.preventDefault(); keys[keyName] = true; };
    const stop = (e) => { e.preventDefault(); keys[keyName] = false; };

    // Bind mouse/touch events to trigger the directional navigation impulse
    btn.addEventListener('mousedown', start);
    btn.addEventListener('touchstart', start, { passive: false });

    window.addEventListener('mouseup', stop); // Use window so it stops even if mouse is released outside
    btn.addEventListener('mouseleave', stop);
    btn.addEventListener('touchend', stop);
    btn.addEventListener('touchcancel', stop);
};

setupButton('btn-left', 'left');
setupButton('btn-right', 'right');
setupButton('btn-up', 'up');
setupButton('btn-down', 'down');

function updateTitlesUI() {
    const toggleSupertitles = document.getElementById('toggle-supertitles');
    if (toggleSupertitles) {
        toggleSupertitles.style.background = showSupertitles ? 'rgba(214,168,72,0.3)' : 'rgba(20,20,20,0.8)';
    }
    const badge = document.getElementById('m-badge-titles');
    if (badge) {
        badge.innerText = showSupertitles ? 'ON' : 'OFF';
        badge.style.color = showSupertitles ? '#d6a848' : '#888';
        badge.style.borderColor = showSupertitles ? 'rgba(214,168,72,0.35)' : 'rgba(255,255,255,0.15)';
        badge.style.background = showSupertitles ? 'rgba(214,168,72,0.18)' : 'rgba(255,255,255,0.05)';
    }
    const container = document.getElementById('annotations-container');
    if (container) {
        container.style.display = showSupertitles ? 'block' : 'none';
    }
}

const toggleSupertitles = document.getElementById('toggle-supertitles');

if (toggleSupertitles) {
    // Toggle the visibility of all loaded English text meshes
    toggleSupertitles.addEventListener('click', (e) => {
        e.preventDefault();
        showSupertitles = !showSupertitles;
        updateTitlesUI();
    });
}

// --- DRONE TOUR MODE LOGIC (POINTS OF INTEREST) ---
// Level 14 tiles: W14 ≈ 15065.5, tile col c width = 254 * 4 / 100 = 10.16 Three.js units.
// Tapestry height = 6.94 units, top = 2.0, bottom = -4.94.
let poiBoundingBoxesGroup = null;
let isPOIVisibleOnScreen = true;

function createPOIBoundingBox(poi, index) {
    const group = new THREE.Group();
    const b = poi.bounds;
    const w = Math.max(0.6, b.xMax - b.xMin) + 0.50; // expanded by 0.25 on each side
    const h = Math.max(0.6, b.yMax - b.yMin) + 0.50; // expanded by 0.25 on each side
    const cx = (b.xMin + b.xMax) / 2;
    const cy = (b.yMin + b.yMax) / 2;
    group.position.set(cx, cy, 0.042);

    const thickness = 0.04; // Half thickness picture frame border

    // Shared material for the frame
    const frameMat = new THREE.MeshBasicMaterial({
        color: 0x221100, // Dark wood / dark brown frame
        transparent: true,
        opacity: 0.85,
        depthWrite: false,
        depthTest: false
    });

    // Top edge
    const topMesh = new THREE.Mesh(new THREE.PlaneGeometry(w + thickness * 2, thickness), frameMat);
    topMesh.position.set(0, h / 2 + thickness / 2, 0);
    topMesh.renderOrder = 500;
    group.add(topMesh);

    // Bottom edge
    const bottomMesh = new THREE.Mesh(new THREE.PlaneGeometry(w + thickness * 2, thickness), frameMat);
    bottomMesh.position.set(0, -h / 2 - thickness / 2, 0);
    bottomMesh.renderOrder = 500;
    group.add(bottomMesh);

    // Left edge
    const leftMesh = new THREE.Mesh(new THREE.PlaneGeometry(thickness, h), frameMat);
    leftMesh.position.set(-w / 2 - thickness / 2, 0, 0);
    leftMesh.renderOrder = 500;
    group.add(leftMesh);

    // Right edge
    const rightMesh = new THREE.Mesh(new THREE.PlaneGeometry(thickness, h), frameMat);
    rightMesh.position.set(w / 2 + thickness / 2, 0, 0);
    rightMesh.renderOrder = 500;
    group.add(rightMesh);

    // Subtle amber tint plane fill (also acts as raycast target for clicks)
    const fillGeo = new THREE.PlaneGeometry(w, h);
    const fillMat = new THREE.MeshBasicMaterial({
        color: 0xd6a848,
        transparent: true,
        opacity: 0.02,
        depthWrite: false,
        depthTest: false
    });
    const fillMesh = new THREE.Mesh(fillGeo, fillMat);
    fillMesh.position.z = -0.001;
    fillMesh.renderOrder = 499;
    fillMesh.userData = { poiIndex: index };
    group.add(fillMesh);

    group.updateHighlight = function (isActive, isVisible) {
        if (isActive) {
            frameMat.color.setHex(0x654321); // Brown when active
            frameMat.opacity = 1.0;
            fillMat.opacity = 0.08;
        } else {
            frameMat.color.setHex(0x221100); // Dark when inactive
            frameMat.opacity = 0.85;
            fillMat.opacity = 0.02;
        }
    };

    return group;
}

function rebuildPOIBoundingBoxes() {
    if (!poiBoundingBoxesGroup) {
        poiBoundingBoxesGroup = new THREE.Group();
        canvasGroup.add(poiBoundingBoxesGroup);
    }
    while (poiBoundingBoxesGroup.children.length > 0) {
        const child = poiBoundingBoxesGroup.children.pop();
        child.traverse(obj => {
            if (obj.geometry) obj.geometry.dispose();
            if (obj.material) obj.material.dispose();
        });
    }
    tourPOIs.forEach((poi, idx) => {
        if (!poi.bounds) return;
        const box = createPOIBoundingBox(poi, idx);
        box.visible = false;
        poi.boxMesh = box;
        poiBoundingBoxesGroup.add(box);
    });
    poiBoundingBoxesGroup.visible = true;
}

function buildTourPOIs(data) {
    if (!data || !Array.isArray(data) || data.length === 0) return;
    // Sort strictly monotonically by x so the camera only flows forward from west to east
    const sorted = [...data].sort((a, b) => a.x - b.x);

    const list = [];

    sorted.forEach((t, i) => {
        const num = i + 1; // Number starts at 1
        const tileIdx = Math.max(0, Math.floor(t.x / 10.25));
        const tileNext = tileIdx + 1;
        const tileStr = `${tileIdx}_0.webp`;
        const tileStrNext = `${tileNext}_0.webp`;

        const locText = (t.translations && t.translations[currentLanguage]) ? t.translations[currentLanguage].text : (t.translations && t.translations.en ? t.translations.en.text : t.latin);
        let locDesc = (t.translations && t.translations[currentLanguage]) ? t.translations[currentLanguage].context : (t.translations && t.translations.en ? t.translations.en.context : "");

        const prevPOI = list[list.length - 1];
        const nextScene = sorted[i + 1];

        // Latin inscription text width: ~0.175 Three.js units per char (80px font * 0.004433 scale)
        const textW = (t.latin && t.latin.length) ? (t.latin.length * 0.175) : 5.0;
        const desiredW = Math.max(5.5, textW + 1.2);
        const spanToNext = nextScene ? (nextScene.x - t.x) : 12.0;

        // Box starts slightly before the inscription / scene figures
        let xMin = t.x - 0.4;
        if (prevPOI && prevPOI.bounds && xMin < prevPOI.bounds.xMax + 0.15) {
            xMin = prevPOI.bounds.xMax + 0.15;
        }

        // Box extends across the scene, bounded so it never collides with next scene
        let xMax = xMin + Math.min(desiredW, Math.max(3.0, spanToNext * 0.88));
        if (nextScene && xMax > nextScene.x - 0.4) {
            xMax = Math.max(xMin + 2.5, nextScene.x - 0.4);
        }
        const cx = (xMin + xMax) / 2;

        const item = {
            id: `scene_${t.scene}`,
            scene: t.scene,
            latin: t.latin,
            title: locText ? `${num}. ${locText}` : `${num}`,
            tiles: [tileStr, tileStrNext],
            bounds: { xMin: +xMin.toFixed(2), xMax: +xMax.toFixed(2), yMin: -3.90, yMax: -0.43 },
            centerX: +cx.toFixed(2),
            centerY: -2.16,
            targetZ: 3.35,
            inspectDuration: 7.5,
            description: locDesc,
            translations: t.translations
        };
        
        // Preserve cinematic overrides for the massive opening scene
        if (t.scene === "1") {
            item.bounds = { xMin: 0.4, xMax: 7.0, yMin: -3.90, yMax: -0.43 };
            item.centerX = 3.7;
            item.centerY = -1.76;
            item.targetZ = 3.35;
            item.inspectDuration = 8.0;
        }

        list.push(item);
    });

    tourPOIs = list;
    rebuildPOIBoundingBoxes();
}

let currentPOIIndex = 0;
let isPoiDwell = false;
let poiDwellTimer = 0;
tourSessionSeed = Math.random() * 1000;

// Ken Burns framing ranges
const tourZoomRange = 1.4;   // ± zoom variation from base Z
const tourYRange = 0.25;     // ± vertical offset from center
const tourTiltRange = 0.08;  // ± subtle yaw tilt (radians)
const tourCamLerpRate = 0.035; // Smoothing rate for camera transitions

function sceneHash(index, seed) {
    const n = Math.sin(index * 127.1 + (seed || 0) * 311.7) * 43758.5453;
    return n - Math.floor(n);
}

function getSceneKenBurns(index, baseZ, zoomRange) {
    const zHash = sceneHash(index, 1 + tourSessionSeed);
    const yHash = sceneHash(index, 2 + tourSessionSeed);
    const tiltHash = sceneHash(index, 3 + tourSessionSeed);
    return {
        targetZ: baseZ + (zHash - 0.5) * 2 * zoomRange,
        targetY: -2.16 + (yHash - 0.5) * 2 * tourYRange,
        targetTilt: (tiltHash - 0.5) * 2 * tourTiltRange
    };
}

function jumpToPOI(index) {
    if (!tourPOIs || tourPOIs.length === 0) return;
    currentPOIIndex = (index + tourPOIs.length) % tourPOIs.length;
    const targetPOI = tourPOIs[currentPOIIndex];
    if (!targetPOI) return;
    camera.position.x = targetPOI.centerX;
    isPoiDwell = true;
    poiDwellTimer = 0;
    isPOIVisibleOnScreen = true;
}



function closeNotes() {
    const popup = document.getElementById('context-scroll');
    const notesBtnTop = document.getElementById('notes-btn-top');
    const tourBtn = document.getElementById('tour-btn');
    if (popup) popup.style.display = 'none';
    if (notesBtnTop) notesBtnTop.style.display = 'flex';
    if (tourBtn) tourBtn.style.display = 'flex';

    const baseZ = 6.5;
    autoScrollTargetZ = baseZ;
    autoScrollTargetX = camera.position.x;
    isSceneDwell = false;
}

function openNotes(shouldAutoScroll = false) {
    const popup = document.getElementById('context-scroll');
    const notesBtnTop = document.getElementById('notes-btn-top');
    const tourBtn = document.getElementById('tour-btn');
    if (popup) popup.style.display = 'block';
    if (notesBtnTop) notesBtnTop.style.display = 'none';
    if (tourBtn) tourBtn.style.display = 'none';

    if (tituliData && tituliData.length > 0) {
        let nearestIndex = 0;
        let minDistance = Infinity;
        for (let i = 0; i < tituliData.length; i++) {
            if (tituliData[i].x !== undefined) {
                const dist = Math.abs(tituliData[i].x - camera.position.x);
                if (dist < minDistance) {
                    minDistance = dist;
                    nearestIndex = i;
                }
            }
        }
        updatePopupUI(nearestIndex, shouldAutoScroll);
    }
}







const mobileTourBtn = document.getElementById('mobile-tour-btn');
if (mobileTourBtn) {
    mobileTourBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openNotes(true);
    });
}








const uiElementsToIsolate = ['#ui', '#lighting-dialog', '#about-dialog', '#context-scroll', '#tour-control-bar', '#mobile-menu', '#mobile-tour-btn', '#hamburger-btn', '#authoring-panel'];
uiElementsToIsolate.forEach(selector => {
    const el = document.querySelector(selector);
    if (el) {
        ['mousedown', 'touchstart', 'pointerdown', 'touchmove', 'pointermove', 'mousemove', 'wheel', 'click'].forEach(evt => {
            el.addEventListener(evt, (e) => {
                // Allow internal scrolling inside dialogs, but stop propagation so camera doesn't pan/zoom
                e.stopPropagation();
            }, { passive: false });
        });
    }
});




let currentPopupSceneIndex = 0;

function updatePopupUI(index, shouldAutoScroll = true) {
    index = parseInt(index, 10);
    if (index < 0 || index >= tituliData.length) return;
    // Cancel any active scene dwell when navigating to a new scene
    isSceneDwell = false;
    sceneDwellTimer = 0;
    sceneDwellPOI = null;
    camera.rotation.x = 0;
    currentPopupSceneIndex = index;
    const annoData = tituliData[index];

    const localizedText = (annoData.translations && annoData.translations[currentLanguage]) ? annoData.translations[currentLanguage].text : annoData.translations['en'].text;
    
    if (localizedText) {
        document.getElementById('context-title').innerText = `"${localizedText}"`;
        document.getElementById('context-title').style.display = 'block';
    } else {
        document.getElementById('context-title').style.display = 'none';
    }
    
    document.getElementById('context-title').style.fontStyle = 'italic';

    let contextText = "No historical context available for this scene.";
    if (annoData.translations && annoData.translations[currentLanguage] && annoData.translations[currentLanguage].context) {
        contextText = annoData.translations[currentLanguage].context;
    } else if (annoData.translations && annoData.translations['en'].context) {
        contextText = annoData.translations['en'].context;
    }
    document.getElementById('context-text').innerText = contextText;

    document.getElementById('prev-scene').style.opacity = (index === 0) ? '0.5' : '1.0';
    document.getElementById('prev-scene').style.pointerEvents = (index === 0) ? 'none' : 'auto';

    document.getElementById('next-scene').style.opacity = (index === tituliData.length - 1) ? '0.5' : '1.0';
    document.getElementById('next-scene').style.pointerEvents = (index === tituliData.length - 1) ? 'none' : 'auto';

    // Restore static center positioning
    const popup = document.getElementById('context-scroll');
    popup.style.left = '50%';
    popup.style.transform = 'translateX(-50%)';
    popup.style.display = 'block';
    
    const notesBtnTop = document.getElementById('notes-btn-top');
    const tourBtn = document.getElementById('tour-btn');
    if (notesBtnTop) notesBtnTop.style.display = 'none';
    if (tourBtn) tourBtn.style.display = 'none';

    if (shouldAutoScroll && annoData.x !== undefined) {
        // Find the mesh to calculate its width so we can center on it perfectly
        const annObj = annotations.find(a => a.data === annoData);
        if (annObj && annObj.mesh) {
            const width = annObj.mesh.geometry.parameters.width;
            autoScrollTargetX = annoData.x + (width / 2.0);
        } else {
            autoScrollTargetX = annoData.x;
        }

        // Calculate target zoom based on bounding box
        autoScrollTargetY = camera.position.y;
        autoScrollTargetZ = 6.5; // fallback baseZ
        if (typeof tourPOIs !== 'undefined' && tourPOIs) {
            const targetPOI = tourPOIs.find(p => p.scene === annoData.scene);
            if (targetPOI && targetPOI.bounds) {
                const padding = 1.25;
                const w = Math.max(0.6, targetPOI.bounds.xMax - targetPOI.bounds.xMin) + 0.50;
                const h = Math.max(0.6, targetPOI.bounds.yMax - targetPOI.bounds.yMin) + 0.50;

                autoScrollTargetX = (targetPOI.bounds.xMin + targetPOI.bounds.xMax) / 2;
                autoScrollTargetY = (targetPOI.bounds.yMin + targetPOI.bounds.yMax) / 2;

                const zFov = Math.tan((camera.fov * Math.PI) / 360);
                const zHeight = (h * padding / 2) / zFov;
                const zWidth = (w * padding / 2) / (zFov * camera.aspect);

                autoScrollTargetZ = Math.max(zHeight, zWidth, 2.5); // Clamp closest zoom

                // For mobile phones, get close enough to the canvas so that the canvas at least fills the vertical viewport
                if (isPhone || (window.innerWidth <= 900 && !isIPad)) {
                    const maxMobileZ = (6.94 / 2) / zFov;
                    if (autoScrollTargetZ > maxMobileZ) {
                        autoScrollTargetZ = maxMobileZ;
                    }
                }

                // Shift the viewport up by 0.1 world units per user request
                autoScrollTargetY += 0.4;

                // Prevent Y from exceeding bounds, which would cause an infinite auto-scroll lock
                if (autoScrollTargetY > 2.0) autoScrollTargetY = 2.0;
                if (autoScrollTargetY < -4.94) autoScrollTargetY = -4.94;
            }
        }
    }
}

document.getElementById('prev-scene').addEventListener('click', () => {
    updatePopupUI(currentPopupSceneIndex - 1);
});

document.getElementById('next-scene').addEventListener('click', () => {
    updatePopupUI(currentPopupSceneIndex + 1);
});

function handleAnnotationClick(clientX, clientY, target) {
    if (isPhone) return; // Feature disabled on mobile devices
    if (target && target.closest && (target.closest('#ui') || target.closest('#authoring-panel') || target.closest('#about-dialog') || target.closest('#lighting-dialog') || target.closest('#help-dialog') || target.closest('#context-scroll') || target.closest('#mobile-menu') || target.closest('#mobile-menu-scrim') || target.closest('#hamburger-btn') || target.closest('#mobile-tour-btn') || target.closest('#tour-control-bar'))) {
        return;
    }

    mouseCoords.x = (clientX / window.innerWidth) * 2 - 1;
    mouseCoords.y = -(clientY / window.innerHeight) * 2 + 1;
    dragRaycaster.setFromCamera(mouseCoords, camera);

    // If drone tour is active, check if user clicked on a POI bounding box
    if (typeof isTourActive !== 'undefined' && isTourActive && poiBoundingBoxesGroup && poiBoundingBoxesGroup.visible) {
        const boxFills = [];
        poiBoundingBoxesGroup.traverse(child => {
            if (child.isMesh && child.userData && child.userData.poiIndex !== undefined) {
                boxFills.push(child);
            }
        });
        const boxIntersects = dragRaycaster.intersectObjects(boxFills, false);
        if (boxIntersects.length > 0) {
            const hitIdx = boxIntersects[0].object.userData.poiIndex;
            if (hitIdx !== undefined) {
                jumpToPOI(hitIdx);
                return;
            }
        }
    }

    // Raycast against all visible annotations
    const annMeshes = annotations.map(a => a.mesh).filter(m => m && m.visible);

    const intersects = dragRaycaster.intersectObjects(annMeshes, false);

    if (intersects.length > 0) {
        const clickedMesh = intersects[0].object;
        const annoObj = clickedMesh.userData.annotation;
        const annoData = annoObj ? annoObj.data : null;

        if (annoData) {
            const index = tituliData.indexOf(annoData);
            updatePopupUI(index);
        }
    }
}
let lastWheelTime = 0;
// Handle trackpad / mouse wheel zooming and horizontal panning.
window.addEventListener('wheel', (e) => {
    if (e.target.closest('#ui') || e.target.closest('#authoring-panel') || e.target.closest('#about-dialog') || e.target.closest('#lighting-dialog') || e.target.closest('#tour-control-bar') || e.target.closest('#mobile-menu') || e.target.closest('#hamburger-btn') || e.target.closest('#mobile-tour-btn')) return;
    e.preventDefault();
    autoScrollTargetX = null; autoScrollTargetZ = null; autoScrollTargetY = null;
    isSceneDwell = false;
    lastWheelTime = Date.now();

    // Normalize scroll distance
    let deltaY = e.deltaY;
    let deltaX = e.deltaX;
    if (e.deltaMode === 1) { deltaY *= 33; deltaX *= 33; } // Line mode
    else if (e.deltaMode === 2) { deltaY *= window.innerHeight; deltaX *= window.innerWidth; } // Page mode

    // Apply zoom impulse (scales with distance so zooming is consistent at all depths)
    if (Math.abs(deltaY) > 0) {
        const distanceMultiplier = Math.max(0.02, Math.pow(camera.position.z / 10, 1.5));
        const zoomImpulse = (deltaY * 0.0012) * distanceMultiplier;
        velocityZ += zoomImpulse;
    }

    // Apply horizontal pan impulse (scales with distance so panning feels consistent)
    if (Math.abs(deltaX) > 0) {
        // Panning sensitivity multiplier tuned for typical mouse wheel / trackpad gestures
        const panImpulse = (deltaX * 0.0003) * Math.max(0.1, camera.position.z * 0.1);
        velocityX += panImpulse;
    }
}, { passive: false });

// Update the Three.js camera projection matrix and WebGL renderer dimensions on window resize.
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    uiCamera.left = window.innerWidth / -2;
    uiCamera.right = window.innerWidth / 2;
    uiCamera.top = window.innerHeight / 2;
    uiCamera.bottom = window.innerHeight / -2;
    uiCamera.updateProjectionMatrix();
});

// Camera physics/smoothing
let velocityX = 0;
let velocityY = 0;
let velocityZ = 0;
const maxVelocityX = 0.125; // Maximum permitted horizontal pan velocity
const maxVelocityY = 0.125;
const maxVelocityZ = 0.1;
const fixedZoomAccel = 0.025;
const friction = 0.92;

let targetRotationY = 0;
const maxTilt = (35 * Math.PI / 180) * 1.25; // Max tilt angle (~28.1 degrees)
const tiltSmoothing = 0.006; // Controls the easing speed of the 3D camera tilt effect

let moveHoldTime = 0;
let zoomHoldTime = 0;

/**
 * Core physics loop for camera movement.
 * Handles inertia, keyboard acceleration, boundary clamping, and the 3D tilt effect.
 */
function updateCamera() {
    let currentAccel = 0;

    const isActivelyPanning = keys.right || keys.left || mouseScrollDir !== 0 || isDragging || isMouseDown || (Date.now() - lastWheelTime < 100);

    if (isActivelyPanning) {
        moveHoldTime += 1;
    } else {
        moveHoldTime = 0;
    }

    if (keys.right || keys.left || mouseScrollDir !== 0) {
        // Smooth exponential acceleration curve for keyboard navigation
        currentAccel = 0.0005 + Math.min(1, moveHoldTime / 300) * 0.012;
    }

    if (keys.right) {
        velocityX += currentAccel;
    } else if (keys.left) {
        velocityX -= currentAccel;
    } else if (mouseScrollDir !== 0) {
        velocityX += currentAccel * mouseScrollDir;
    }

    // Wait 2 seconds (120 frames at 60fps) of CONTINUOUS active panning before allowing the camera to tilt
    const tiltFactor = Math.max(0, Math.min(1, (moveHoldTime - 120) / 60)); // Fades in smoothly over 1 second after the wait

    // Unify tilt logic: tilt is purely based on current horizontal velocity.
    if (typeof isTourActive === 'undefined' || !isTourActive) {
        const speedRatio = Math.max(-1, Math.min(1, velocityX / 0.15));
        targetRotationY = -maxTilt * speedRatio * tiltFactor;
    }

    // Cinematic initial sequence: tilt right to reveal expanse, pause, then gracefully fly in with ease-in
    if (initialSlowZoom) {
        if (autoScrollTargetZ === null || autoScrollTargetX !== null) {
            initialSlowZoom = false; // User interrupted
            const uiEl = document.getElementById('ui');
            if (uiEl) { uiEl.style.opacity = '1'; uiEl.style.pointerEvents = 'auto'; }
            const hamEl = document.getElementById('hamburger-btn');
            if (hamEl) { hamEl.style.opacity = '1'; hamEl.style.pointerEvents = 'auto'; }
            const notesEl = document.getElementById('notes-btn-top');
            if (notesEl) { 
                notesEl.style.opacity = '1'; 
                notesEl.style.pointerEvents = 'auto'; 
                notesEl.classList.add('pulse-attention');
            }
            const mTourBtn = document.getElementById('m-menu-notes');
            if (mTourBtn) {
                mTourBtn.classList.add('pulse-attention');
            }
            ambientLight.intensity = 1.06;
            dirLight.intensity = 1.0;
            if (revealLight && revealLight.parent) {
                scene.remove(revealLight);
                scene.remove(revealLight.target);
                revealLight = null;
            }
        } else {
            if (cinematicStartTime === null) {
                cinematicStartTime = Date.now();
            }
            const elapsed = Date.now() - cinematicStartTime;
            // Mild tilt down the tapestry to convey length (steeper on mobile to compensate for narrow screen)
            const targetTilt = (isPhone || window.innerWidth <= 900) ? -0.80 : -0.55;
            
            if (revealLight) {
                if (!revealLight.parent) {
                    scene.add(revealLight);
                    scene.add(revealLight.target);
                }
                revealLight.position.copy(camera.position);
                const forward = new THREE.Vector3(0, 0, -1);
                forward.applyEuler(camera.rotation);
                revealLight.target.position.copy(camera.position).add(forward);
            }
            
            // --- LIGHTING TIMELINE ---
            // 1. Spotlight (swells 0-2.5s, fades out 2.5s-11.5s)
            if (elapsed < 2500) {
                const lightFactor = elapsed / 2500.0;
                if (revealLight) {
                    revealLight.intensity = 0.85 * (lightFactor * lightFactor);
                    revealLight.angle = 0.05 + (Math.PI / 8) * lightFactor;
                }
            } else if (elapsed < 11500) {
                const fadeFactor = (elapsed - 2500) / 9000.0;
                if (revealLight) {
                    revealLight.intensity = 0.85 * (1.0 - fadeFactor);
                    revealLight.angle = 0.05 + (Math.PI / 8) + (Math.PI / 4) * fadeFactor;
                }
            } else {
                if (revealLight) revealLight.intensity = 0.0;
            }

            // 2. Ambient Light (holds 0-1.5s, fades up 1.5s-11.5s)
            if (elapsed < 1500) {
                ambientLight.intensity = 0.02;
                dirLight.intensity = 0.0;
            } else if (elapsed < 11500) {
                const lightFactor = (elapsed - 1500) / 10000.0; // 10-second sunrise
                const dramaticFade = Math.pow(lightFactor, 1.2); 
                ambientLight.intensity = 0.02 + (1.04 * dramaticFade);
                dirLight.intensity = 1.0 * dramaticFade;
            } else {
                ambientLight.intensity = 1.06;
                dirLight.intensity = 1.0;
            }

            // --- CAMERA TIMELINE ---
            if (elapsed < 2500) {
                // Phase 1: Hold still
                targetRotationY = 0;
                cinematicRate = 0;
            } else if (elapsed < 7500) {
                // Phase 2: Tilt and track (5 seconds)
                const t = Math.min(1.0, (elapsed - 2500) / 5000.0);
                const smoothT = t * t * (3 - 2 * t);
                targetRotationY = targetTilt * smoothT;
                cinematicRate = 0.1; 
                
                const trackSpeed = 6 * (t - t * t);
                camera.position.x += 0.012 * trackSpeed;
            } else if (elapsed < 9000) {
                // Phase 3: Pause
                targetRotationY = targetTilt;
                cinematicRate = 0.1; 
                camera.position.x += 0.002;
            } else {
                // Phase 4: Untilt and Zoom
                targetRotationY = 0;
                const phase4Elapsed = Math.max(0, elapsed - 9000);
                const rawFactor = Math.min(1.0, phase4Elapsed / 3000.0);
                const accelFactor = rawFactor * rawFactor;
                
                cinematicRate = 0.0005 + (0.015 * accelFactor); 
                camera.position.z += (autoScrollTargetZ - camera.position.z) * cinematicRate;
                camera.position.x += 0.002 * (1.0 - rawFactor);
                
                if (Math.abs(camera.position.z - autoScrollTargetZ) < 0.02 && Math.abs(camera.rotation.y) < 0.02) {
                    camera.position.z = autoScrollTargetZ;
                    camera.rotation.y = 0;
                    autoScrollTargetZ = null;
                    initialSlowZoom = false;
                    
                    const uiEl = document.getElementById('ui');
                    if (uiEl) { uiEl.style.opacity = '1'; uiEl.style.pointerEvents = 'auto'; }
                    const hamEl = document.getElementById('hamburger-btn');
                    if (hamEl) { hamEl.style.opacity = '1'; hamEl.style.pointerEvents = 'auto'; }
                    const notesEl = document.getElementById('notes-btn-top');
                    if (notesEl) { 
                        notesEl.style.opacity = '1'; 
                        notesEl.style.pointerEvents = 'auto'; 
                        notesEl.classList.add('pulse-attention');
                    }
                    const mTourBtn = document.getElementById('m-menu-notes');
                    if (mTourBtn) {
                        mTourBtn.classList.add('pulse-attention');
                    }
                }
            }
        }
    }

    if (keys.up || keys.down) {
        zoomHoldTime += 1;
    } else {
        zoomHoldTime = 0;
    }

    // Modest acceleration curve: start at base speed and gradually double it over 2 seconds
    let currentZoomAccel = fixedZoomAccel * (1.0 + Math.min(1.0, zoomHoldTime / 120) * 1.0);

    // Further scale zoom acceleration by current Z distance so it doesn't crawl when fully zoomed out
    currentZoomAccel *= Math.max(0.02, Math.pow(camera.position.z / 10, 1.5));

    if (keys.up) velocityZ -= currentZoomAccel;
    if (keys.down) velocityZ += currentZoomAccel;

    const currentFriction = isTouch ? 0.95 : friction;
    velocityX *= currentFriction;
    velocityY *= currentFriction;
    velocityZ *= currentFriction;

    // Clamp velocity
    velocityX = Math.max(-maxVelocityX, Math.min(maxVelocityX, velocityX));
    velocityY = Math.max(-maxVelocityY, Math.min(maxVelocityY, velocityY));
    velocityZ = Math.max(-maxVelocityZ, Math.min(maxVelocityZ, velocityZ));

    camera.position.x += velocityX;
    camera.position.y += velocityY;
    camera.position.z += velocityZ;

    // Prevent the view from drifting backwards when the camera straightens out (untilt compensation)
    const previousRotationY = camera.rotation.y;
    const isUntilting = Math.abs(targetRotationY) < Math.abs(previousRotationY);

    // Use a 2.0x multiplier for returning to straight-on view to balance snappiness with smooth easing
    let currentSmoothing = isUntilting ? tiltSmoothing * 2.0 : tiltSmoothing;
    if (initialSlowZoom) currentSmoothing = cinematicRate; // Use dynamic cinematic rate to ease-in the untiliting
    camera.rotation.y += (targetRotationY - camera.rotation.y) * currentSmoothing;

    if (!initialSlowZoom || (typeof cinematicStartTime !== 'undefined' && cinematicStartTime !== null && Date.now() - cinematicStartTime > 7500)) {
        const ct = document.getElementById('cinematic-title');
        if (ct && ct.style.opacity !== '0') ct.style.opacity = '0';
    }

    if (isUntilting && (typeof isTourActive === 'undefined' || !isTourActive) && !initialSlowZoom) {
        const focalXBefore = camera.position.x - camera.position.z * Math.tan(previousRotationY);
        camera.position.x = focalXBefore + camera.position.z * Math.tan(camera.rotation.y);
    }

    // Bounds
    if (camera.position.x < 0) camera.position.x = 0;
    const maxX = W / SCALE;
    if (camera.position.x > maxX) camera.position.x = maxX;

    // Vertical bounds: tapestry is between y=2.0 and y=-4.94
    const maxY = 2.0;
    const minY = -4.94;
    if (camera.position.y > maxY) {
        camera.position.y = maxY;
        velocityY = 0;
    }
    if (camera.position.y < minY) {
        camera.position.y = minY;
        velocityY = 0;
    }

    if (camera.position.z < 0.9) camera.position.z = 0.9; // Allow close inspection for max L19 LOD detail
    if (camera.position.z > 60) camera.position.z = 60;

    if (magActive) {
        magCamera.position.z = Math.max(0.3, camera.position.z * 0.25);
    }
}

/**
 * Main LOD (Level of Detail) manager.
 * Calculates the visible frustum and queues texture loading/unloading for L16, L17, and L18 layers.
 */
function updateTiles() {
    // Calculate visible width based on camera Z and FOV
    const vFOV = THREE.MathUtils.degToRad(camera.fov);
    const height = 2 * Math.tan(vFOV / 2) * camera.position.z;
    const baseWidth = height * camera.aspect;
    
    // Adjust center and width for camera rotation (looking down the tapestry)
    const viewCenterX = camera.position.x - camera.position.z * Math.tan(camera.rotation.y);
    const viewWidth = baseWidth / Math.max(0.15, Math.cos(camera.rotation.y));

    // The margin acts as an off-screen buffer, forcing tiles to load just outside the camera's field of view
    const margin = isPhone ? 6 : 60; // Reasonable buffer for phones, generous for desktop

    let magMinX = 0, magMaxX = 0;
    if (magActive) {
        const magVisibleHeight = 2 * Math.tan(vFOV / 2) * magCamera.position.z;
        const magVisibleWidth = magVisibleHeight * magCamera.aspect;
        magMinX = magCamera.position.x - magVisibleWidth / 2;
        magMaxX = magCamera.position.x + magVisibleWidth / 2;
    }

    // LOD Tile Manager: Evaluates which tiles intersect the camera frustum and handles async texture loading/unloading to preserve memory
    const processTiles = (tileArray, levelStr, isHighRes, unloadZ) => {
        // For high-res tiles, we use a tighter margin so we don't spam requests for tiles slightly off screen
        // Tight culling margins for L18 (high-res) prevent mobile devices from exhausting their network request pool
        // Base layer (L16) is small enough to keep fully loaded in memory (approx 60MB), 
        // ensuring we can always see to infinity down the hall without clipping.
        const actualMargin = isHighRes ? (levelStr === '19' ? 1 : (levelStr === '18' ? 2 : 4)) : 99999;
        
        const minX = viewCenterX - viewWidth / 2 - actualMargin;
        const maxX = viewCenterX + viewWidth / 2 + actualMargin;

        for (let tile of tileArray) {
            // Calculate true distance to tile for high-res culling down the hall
            const distToCameraX = Math.abs(tile.xCenter - camera.position.x);
            // High-res tiles should only load if they are close to the camera, even if they are in the frustum
            const meetsDistanceRequirement = !isHighRes || (distToCameraX <= unloadZ * 2.5);
            
            const isMainVisible = (camera.position.z <= unloadZ) && meetsDistanceRequirement && (tile.xCenter >= minX && tile.xCenter <= maxX);
            const isMagVisible = magActive && isHighRes && (tile.xCenter >= magMinX - actualMargin && tile.xCenter <= magMaxX + actualMargin);
            const isVisible = isMainVisible || isMagVisible;

            if (isVisible) {
                const canLoadNewTile = !isHighRes || (smoothedCameraSpeed < 0.015);

                if (canLoadNewTile && !tile.loaded && !tile.loading && !tile.failed && activeRequests < MAX_CONCURRENT_REQUESTS) {
                    tile.loading = true;
                    activeRequests++;

                    const baseUrl = `btstorage.britishmuseum.org/bayeux-tapestry/image_files/${levelStr}/${tile.c}_${tile.r}.webp`;
                    const url = `https://images.weserv.nl/?url=${encodeURIComponent(baseUrl)}`;

                    textureLoader.load(url, (texture) => {
                        activeRequests--;
                        texture.generateMipmaps = true;
                        texture.minFilter = THREE.LinearMipmapLinearFilter;
                        texture.magFilter = THREE.LinearFilter;
                        texture.anisotropy = renderer.capabilities.getMaxAnisotropy();

                        const matOpts = {
                            map: texture,
                            transparent: true,
                            opacity: isHighRes ? 1.0 : 0 // Pop in instantly for high-res to prevent fade artifacts over base
                        };

                        if (useSimpleLighting) {
                            tile.mesh.material = new THREE.MeshLambertMaterial(matOpts);
                        } else {
                            matOpts.roughness = 0.85;
                            matOpts.metalness = 0.0;
                            matOpts.bumpMap = texture;
                            matOpts.bumpScale = -0.006;
                            tile.mesh.material = new THREE.MeshStandardMaterial(matOpts);
                        }
                        tile.loaded = true;

                        if (!isHighRes) {
                            let op = 0;
                            const fade = setInterval(() => {
                                op += 0.1;
                                if (op >= 1) {
                                    op = 1;
                                    clearInterval(fade);
                                }
                                if (tile.loaded) {
                                    tile.mesh.material.opacity = op;
                                }
                            }, 50);
                        }
                    }, undefined, (err) => {
                        activeRequests--;
                        tile.loading = false;
                        tile.failed = true;
                    });
                }
            } else {
                // Unload far away tiles smoothly. A large margin multiplier acts as a cache so tiles don't pop out immediately
                if (tile.loaded && Math.abs(tile.xCenter - camera.position.x) > actualMargin * 5) {
                    if (tile.mesh.material.map) {
                        tile.mesh.material.map.dispose();
                    }
                    if (tile.mesh.material !== emptyMaterial) {
                        tile.mesh.material.dispose();
                    }
                    tile.mesh.material = emptyMaterial;
                    tile.loaded = false;
                    tile.loading = false;
                }
            }
        }
    };

    // Prioritize processing based on zoom level to manage activeRequests cap
    const effectiveZ = magActive ? Math.min(camera.position.z, magCamera.position.z) : camera.position.z;

    if (effectiveZ <= 1.2) {
        processTiles(tilesL19, '19', true, 1.2);
        processTiles(tilesL18, '18', true, 2.5);
        processTiles(tilesL17, '17', true, 5.0);
        processTiles(tiles, '16', false, 9999);
    } else if (effectiveZ <= 2.5) {
        processTiles(tilesL18, '18', true, 2.5);
        processTiles(tilesL17, '17', true, 5.0);
        processTiles(tiles, '16', false, 9999);
        processTiles(tilesL19, '19', true, 1.2); // Fast unload
    } else if (effectiveZ <= 5.0) {
        processTiles(tilesL17, '17', true, 5.0);
        processTiles(tiles, '16', false, 9999);
        processTiles(tilesL18, '18', true, 2.5); // Fast unload
        processTiles(tilesL19, '19', true, 1.2); // Fast unload
    } else {
        processTiles(tiles, '16', false, 9999);
        processTiles(tilesL17, '17', true, 5.0); // Fast unload
        processTiles(tilesL18, '18', true, 2.5); // Fast unload
        processTiles(tilesL19, '19', true, 1.2); // Fast unload
    }
}

/**
 * Main WebGL render loop.
 * Updates physics, animations, dynamic lighting, and triggers the renderer.
 */
let autoScrollTargetX = null;
let autoScrollTargetY = null;
let autoScrollTargetZ = null;

// POI dwell state: slow breathing zoom when camera arrives at a scene
let isSceneDwell = false;
let sceneDwellTimer = 0;
let sceneDwellPOI = null; // The tourPOI we're dwelling on
let sceneDwellStartZ = 8.5; // Camera Z when dwell began
let sceneDwellStartY = 0; // Camera Y when dwell began
let activePulsePOIIndex = -1;
let initialSlowZoom = true;
let cinematicStartTime = null;
let cinematicRate = 0.008;

// Schedule an initial slow zoom in for both desktop and mobile
// "Have the initial slow zoom get closer to the canvas." -> Z=6.5
autoScrollTargetZ = 6.5;
setTimeout(() => {
    if (initialSlowZoom) {
        const ct = document.getElementById('cinematic-title');
        if (ct) ct.style.opacity = '1';
    }
}, 100);
let pulseTimer = 0;

function triggerPOIPulse(index) {
    // Pulse logic disabled per user request to "eliminate the rectangle"
    activePulsePOIIndex = -1;
}

function updateDynamicPopup() {
    // Do not override POI text while drone tour is actively running
    if (typeof isTourActive !== 'undefined' && isTourActive) return;

    const popup = document.getElementById('context-scroll');
    if (!popup || window.getComputedStyle(popup).display === 'none') return;
    if (autoScrollTargetX !== null) return; // Don't interfere with auto-scrolling

    let closestIndex = -1;
    let minDistance = Infinity;

    for (let i = 0; i < annotations.length; i++) {
        const ann = annotations[i];
        if (!ann || !ann.mesh || !ann.data) continue;

        const width = ann.mesh.geometry.parameters.width;
        const centerPoint = ann.data.x + width / 2.0;

        const dist = Math.abs(camera.position.x - centerPoint);
        if (dist < minDistance) {
            minDistance = dist;
            closestIndex = tituliData.indexOf(ann.data);
        }
    }

    if (closestIndex !== -1 && closestIndex !== currentPopupSceneIndex) {
        // Only update if it's reasonably close to the center of the screen (within 10 units of distance)
        // This prevents the popup from jumping to a scene that is completely off-screen
        if (minDistance < 8.0) {
            updatePopupUI(closestIndex, false);
        }
    }
}

const tourClock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);
    const dt = Math.min(tourClock.getDelta(), 0.1);
    

    updateDynamicPopup();

    // --- POI PULSE LOGIC ---
    if (activePulsePOIIndex >= 0) {
        pulseTimer -= dt;

        if (typeof tourPOIs !== 'undefined' && tourPOIs) {
            for (let i = 0; i < tourPOIs.length; i++) {
                const p = tourPOIs[i];
                if (p && p.boxMesh) {
                    if (i === activePulsePOIIndex && pulseTimer > 0) {
                        // Fade out over 5 seconds
                        const intensity = pulseTimer / 5.0; // 1.0 down to 0.0
                        p.boxMesh.updateHighlight(true, true);
                        p.boxMesh.children.forEach(child => {
                            if (child.material) {
                                // "Make the rectangle 50% transparent" => maxOp for frame is 0.5
                                const maxOp = (child.userData && child.userData.poiIndex !== undefined) ? 0.08 : 0.5;
                                child.material.opacity = intensity * maxOp;
                                child.material.transparent = true;
                            }
                        });
                        p.boxMesh.visible = true;
                    } else {
                        p.boxMesh.visible = false;
                    }
                }
            }
        }

        if (pulseTimer <= 0) {
            activePulsePOIIndex = -1;
            if (typeof tourPOIs !== 'undefined' && tourPOIs) {
                for (let i = 0; i < tourPOIs.length; i++) {
                    const p = tourPOIs[i];
                    if (p && p.boxMesh) {
                        p.boxMesh.visible = false;
                    }
                }
            }
        }
    }


    if (autoScrollTargetX !== null) {
        camera.position.x += (autoScrollTargetX - camera.position.x) * 0.1;
        let zReached = true;
        let yReached = true;

        if (autoScrollTargetY !== null) {
            camera.position.y += (autoScrollTargetY - camera.position.y) * 0.1;
            if (Math.abs(camera.position.y - autoScrollTargetY) > 0.01) {
                yReached = false;
            } else {
                camera.position.y = autoScrollTargetY;
            }
        }

        if (autoScrollTargetZ !== null) {
            camera.position.z += (autoScrollTargetZ - camera.position.z) * 0.1;
            if (Math.abs(camera.position.z - autoScrollTargetZ) > 0.01) {
                zReached = false;
            } else {
                camera.position.z = autoScrollTargetZ;
            }
        }

        if (Math.abs(camera.position.x - autoScrollTargetX) < 0.01 && zReached && yReached) {
            camera.position.x = autoScrollTargetX;
            autoScrollTargetX = null; autoScrollTargetZ = null; autoScrollTargetY = null;
            autoScrollTargetZ = null; autoScrollTargetY = null;
            
            // Start scene dwell (breathing zoom) if notes popup is open
            const notesPopup = document.getElementById('context-scroll');
            if (notesPopup && window.getComputedStyle(notesPopup).display !== 'none' && typeof tourPOIs !== 'undefined' && tourPOIs) {
                const targetScene = tituliData[currentPopupSceneIndex];
                if (targetScene) {
                    const dwellPOI = tourPOIs.find(p => p.scene === targetScene.scene);
                    if (dwellPOI && dwellPOI.bounds) {
                        isSceneDwell = true;
                        sceneDwellTimer = 0;
                        sceneDwellPOI = dwellPOI;
                        sceneDwellStartZ = camera.position.z;
                        sceneDwellStartY = camera.position.y;
                        triggerPOIPulse(tourPOIs.indexOf(dwellPOI));
                    }
                }
            } else if (typeof tituliData !== 'undefined' && tituliData.length > 0) {
                const targetScene = tituliData[currentPopupSceneIndex];
                if (targetScene && typeof tourPOIs !== 'undefined') {
                    const targetPOIIndex = tourPOIs.findIndex(p => p.scene === targetScene.scene);
                    if (targetPOIIndex >= 0) {
                        triggerPOIPulse(targetPOIIndex);
                    }
                }
            }
        }
    }
    // --- SCENE DWELL: slow breathing zoom in and out ---
    if (isSceneDwell && sceneDwellPOI && autoScrollTargetX === null) {
        sceneDwellTimer += dt;
        const INITIAL_PAUSE = 0.25; // 0.25s wait before zoom begins
        const ZOOM_IN = 64.0;    // 64s zoom in (half as fast as previous)
        const PAUSE_IN = 5.0;    // 5s hold at close-up
        const ZOOM_OUT = 64.0;   // 64s zoom out
        const PAUSE_OUT = 5.0;   // 5s hold at far
        const FULL_CYCLE = INITIAL_PAUSE + ZOOM_IN + PAUSE_IN + ZOOM_OUT + PAUSE_OUT;
        
        // Get significantly closer to the canvas at the apex of the zoom
        const closeZ = (sceneDwellPOI.targetZ || 3.35) * 0.6;
        const farZ = sceneDwellStartZ;
        const targetY = sceneDwellPOI.bounds.yMin + 0.80 * (sceneDwellPOI.bounds.yMax - sceneDwellPOI.bounds.yMin); // Aim for 80% of the bounding box
        
        const cyclePos = sceneDwellTimer % FULL_CYCLE;
        let progress; // 0 = far, 1 = close
        if (cyclePos <= INITIAL_PAUSE) {
            // Initial pause before starting to zoom
            progress = 0.0;
        } else if (cyclePos <= INITIAL_PAUSE + ZOOM_IN) {
            // Zooming in
            const t = (cyclePos - INITIAL_PAUSE) / ZOOM_IN;
            // Cubic ease-out: starts fast, spends a long time slowly creeping up to the canvas
            progress = 1.0 - Math.pow(1.0 - t, 3);
        } else if (cyclePos <= INITIAL_PAUSE + ZOOM_IN + PAUSE_IN) {
            // Holding at close-up
            progress = 1.0;
        } else if (cyclePos <= INITIAL_PAUSE + ZOOM_IN + PAUSE_IN + ZOOM_OUT) {
            // Zooming out
            const t = (cyclePos - INITIAL_PAUSE - ZOOM_IN - PAUSE_IN) / ZOOM_OUT;
            // Cubic ease-in reversed: starts slowly pulling away, speeds up at the end
            progress = 1.0 - Math.pow(t, 3);
        } else {
            // Holding at far
            progress = 0.0;
        }
        
        const desiredZ = farZ + (closeZ - farZ) * progress;
        camera.position.z += (desiredZ - camera.position.z) * (dt * 2.0);
        
        const currentYTarget = sceneDwellStartY + (targetY - sceneDwellStartY) * progress;
        camera.position.x += (sceneDwellPOI.centerX - camera.position.x) * (dt * 0.15);
        camera.position.y += (currentYTarget - camera.position.y) * (dt * 2.0);
        targetRotationY += (0 - targetRotationY) * (dt * 0.3);
        
        // Zero velocity so updateCamera doesn't fight our lerps
        velocityX = 0; velocityY = 0; velocityZ = 0;
    }

    updateCamera();
    updateTiles();

    dirLight.position.set(camera.position.x - 5.0, tapestryElevation + 4.0, 2.0);
    dirLight.target.position.set(camera.position.x + 2.0, tapestryElevation, 0);
    dirLight.target.updateMatrixWorld();


    if (magActive) {
        magLight.visible = true;
        // Position the light closely and slightly offset from the lens center for extreme grazing
        magLight.position.set(magCamera.position.x - 0.5, magCamera.position.y + 0.5, 0.8);
        // Point the spotlight directly at the canvas center of the lens
        magLight.target.position.set(magCamera.position.x, magCamera.position.y, 0);
        magLight.target.updateMatrixWorld();

        magCamera.position.z = Math.max(0.3, camera.position.z * 0.25);
        renderer.setRenderTarget(magRenderTarget);
        renderer.render(scene, magCamera);
        renderer.setRenderTarget(null);

        // Hide it for the main render if we don't want the flashlight visible globally, 
        // but keeping it visible globally creates a cool flashlight effect!
        // Let's keep it visible globally since it simulates holding a magnifying glass with a built in light.
    } else {
        magLight.visible = false;
    }
    renderer.render(scene, camera);
    if (magActive) {
        renderer.autoClear = false;
        renderer.clearDepth();
        renderer.render(uiScene, uiCamera);
        renderer.autoClear = true;
    }
    if (typeof updateAnnotations === 'function') updateAnnotations();
}

animate();

// UI Dialog Listeners

const notesBtnTop = document.getElementById('notes-btn-top');
if (notesBtnTop) {
    notesBtnTop.addEventListener('click', (e) => {
        e.preventDefault();
        openNotes(true);
    });
}

const tourBtn = document.getElementById('tour-btn');
if (tourBtn) {
    tourBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openNotes(true); // Treat it exactly like the top tour button
    });
}

document.querySelectorAll('#learn-more-link').forEach(link => {
    // Open the About dialog when the top navigation link is clicked
    link.addEventListener('click', (e) => { e.preventDefault(); document.getElementById('about-dialog').style.display = 'block'; });
});

document.querySelectorAll('#help-link').forEach(link => {
    // Open the Help/Controls dialog when the top navigation link is clicked
    link.addEventListener('click', (e) => { e.preventDefault(); document.getElementById('help-dialog').style.display = 'block'; });
});

// Close the About dialog
document.getElementById('close-dialog').addEventListener('click', () => {
    document.getElementById('about-dialog').style.display = 'none';
});


document.querySelectorAll('#lang-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        // Highlight current language
        document.querySelectorAll('.lang-option').forEach(opt => {
            if (opt.getAttribute('data-lang') === currentLanguage) {
                opt.style.background = '#8b7355';
                opt.style.border = '1px solid #f4e4bc';
            } else {
                opt.style.background = '#2c221a';
                opt.style.border = '1px solid #444';
            }
        });
        document.getElementById('lang-dialog').style.display = 'block';
    });
});

document.getElementById('close-lang').addEventListener('click', () => {
    document.getElementById('lang-dialog').style.display = 'none';
});

document.querySelectorAll('.lang-option').forEach(btn => {
    btn.addEventListener('click', (e) => {
        changeLanguage(e.target.getAttribute('data-lang'));
    });
});

// Close the Help/Controls dialog
document.getElementById('close-help').addEventListener('click', () => {
    document.getElementById('help-dialog').style.display = 'none';
});

// Close the Context popup
document.getElementById('close-context').addEventListener('click', () => {
    closeNotes();
});

const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('hold')) {
    setTimeout(() => { console.log('Hold expired'); }, parseInt(urlParams.get('hold')));
}
if (urlParams.get('adv') === '1') {
    const advBtn = document.getElementById('lighting-controls-btn');
    if (advBtn) advBtn.style.display = 'flex';
}
if (urlParams.get('x')) {
    camera.position.x = parseFloat(urlParams.get('x'));
}
if (urlParams.get('z')) {
    camera.position.z = parseFloat(urlParams.get('z'));
}

// --- AUTHORING MODE LOGIC ---
// Authoring mode allows editors to visually drag and drop text annotations over the tapestry.
// It bypasses the standard UI and enables raycasting-based 3D mesh dragging, saving directly to localStorage.
let tituliData = [];
let isAuthoringMode = urlParams.get('author') === '1';

if (isAuthoringMode) {
    document.getElementById('authoring-panel').style.display = 'block';

    // Export the current layout of 3D text meshes to the console as formatted JSON
    document.getElementById('auth-export').addEventListener('click', () => {
        const exportData = annotations.map(a => a.data);
        console.log(JSON.stringify(exportData, null, 2));
        alert('Exported ' + exportData.length + ' scenes to console! See developer tools.');
    });
}
// ----------------------------

// --- ANNOTATION DISPLAY LOGIC ---

/**
 * Renders English translation text to a 2D canvas and maps it onto a 3D PlaneGeometry.
 * @param {string} text - The English string to render
 * @param {boolean} isPlaced - In authoring mode, unplaced text is rendered in red
 * @returns {THREE.Mesh}
 */

function changeLanguage(lang) {
    currentLanguage = lang;
    localStorage.setItem('bayeux_lang', currentLanguage);

    // Update UI buttons
    document.querySelectorAll('.lang-option').forEach(btn => {
        if (btn.getAttribute('data-lang') === currentLanguage) {
            btn.style.background = '#8b7355';
            btn.style.border = '1px solid #f4e4bc';
        } else {
            btn.style.background = '#2c221a';
            btn.style.border = '1px solid #444';
        }
    });

    // Translate static UI elements
    const dict = uiDict[currentLanguage] || uiDict['en'];
    document.querySelectorAll('#help-link').forEach(el => el.innerText = dict.help);
    document.querySelectorAll('#learn-more-link').forEach(el => el.innerText = dict.about);
    document.querySelectorAll('#toggle-supertitles').forEach(el => el.innerText = dict.titles);
    document.querySelectorAll('#tour-btn-text').forEach(el => {
        if (typeof isTourActive !== 'undefined' && isTourActive) {
            el.innerText = dict.stopTour || 'Stop Tour';
        } else {
            el.innerText = dict.tour;
        }
    });
    const mLabel = document.getElementById('mobile-tour-label');
    if (mLabel) mLabel.innerText = dict.startTour || dict.tour || 'Start Tour';
    if (typeof isTourActive !== 'undefined' && isTourActive) {
        const statusLabel = document.getElementById('tour-status-label');
        if (statusLabel) statusLabel.innerText = isTourPaused ? (dict.paused || 'Paused') : (dict.tourStatus || 'Touring');
    }
    document.querySelectorAll('#notes-btn-text, #tour-btn-text').forEach(el => el.innerText = dict.tour);

    // Translate mobile menu elements
    const mTextTour = document.getElementById('m-text-tour');
    if (mTextTour) {
        mTextTour.innerText = (typeof isTourActive !== 'undefined' && isTourActive) ? (dict.stopTour || 'Stop Tour') : (dict.startTour || 'Start Tour');
    }
    const mTextNotes = document.getElementById('m-text-notes');
    if (mTextNotes) mTextNotes.innerText = dict.sceneNotes || 'Tour';
    const mTextTitles = document.getElementById('m-text-titles');
    if (mTextTitles) mTextTitles.innerText = dict.titles || 'Titles';
    const mTextLang = document.getElementById('m-text-lang');
    if (mTextLang) mTextLang.innerText = dict.language || 'Language';
    const mBadgeLang = document.getElementById('m-badge-lang');
    if (mBadgeLang) mBadgeLang.innerText = currentLanguage.toUpperCase();
    const mTextHelp = document.getElementById('m-text-help');
    if (mTextHelp) mTextHelp.innerText = dict.help || 'Help';
    const mTextAbout = document.getElementById('m-text-about');
    if (mTextAbout) mTextAbout.innerText = dict.about || 'About';
    const mTextMusic = document.getElementById('m-text-music');
    if (mTextMusic) mTextMusic.innerText = dict.music || 'Music';
    const mTextFullscreen = document.getElementById('m-text-fullscreen');
    if (mTextFullscreen) mTextFullscreen.innerText = dict.fullscreen || 'Fullscreen';

    const prevBtn = document.getElementById('prev-scene');
    const nextBtn = document.getElementById('next-scene');
    const closeBtn = document.getElementById('close-context');
    if (prevBtn) prevBtn.innerText = dict.prev;
    if (nextBtn) nextBtn.innerText = dict.next;
    if (closeBtn) closeBtn.innerText = dict.close;

    document.getElementById('lang-dialog').style.display = 'none';

    // Re-render all 3D meshes
    annotations.forEach(ann => {
        if (ann.mesh) {
            canvasGroup.remove(ann.mesh);
            ann.mesh.geometry.dispose();
            ann.mesh.material.map.dispose();
            ann.mesh.material.dispose();
        }
        const str = (ann.data.translations && ann.data.translations[currentLanguage]) ? ann.data.translations[currentLanguage].text : ann.data.translations['en'].text;
        const newMesh = createTextMesh(str, ann.data.x !== undefined);
        newMesh.position.set(ann.data.x, ann.data.y, 0.05);
        newMesh.visible = false;
        ann.mesh = newMesh;
        canvasGroup.add(newMesh);
    });
    const popup = document.getElementById('context-scroll');
    if (popup && window.getComputedStyle(popup).display !== 'none') {
        updatePopupUI(currentPopupSceneIndex, false);
    }
    if (typeof tituliData !== 'undefined' && tituliData && tituliData.length > 0) {
        buildTourPOIs(tituliData);
    }
}


function createTextMesh(text, isPlaced) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    let fontSize = 80; // High-res font rendering
    if (currentLanguage === 'de' || currentLanguage === 'nl') {
        fontSize = 60; // Make font smaller for longer languages
    }
    const fontStr = (currentLanguage === 'zh' || currentLanguage === 'hi' || currentLanguage === 'ar' || currentLanguage === 'bn') ? `normal ${fontSize}px serif` : `normal ${fontSize}px 'MedievalSharp', serif`;
    ctx.font = fontStr;
    ctx.letterSpacing = '3px';
    const renderText = currentLanguage === 'zh' ? text : text.toUpperCase();
    const metrics = ctx.measureText(renderText);
    canvas.width = Math.ceil(metrics.width) + 20;
    canvas.height = fontSize * 1.5;

    // Re-apply context styles after canvas resize clears them
    ctx.font = fontStr;
    ctx.letterSpacing = '3px';
    ctx.fillStyle = (!isPlaced && isAuthoringMode) ? '#aa0000' : '#5b5349';
    ctx.textBaseline = 'top';
    ctx.fillText(renderText, 10, 10);

    const texture = new THREE.CanvasTexture(canvas);
    texture.minFilter = THREE.LinearMipmapLinearFilter;

    // Convert raw canvas pixels into 3D world space coordinates
    const scale = 0.004433; // Base scale factor applied to text meshes for legibility
    const worldWidth = canvas.width * scale;
    const worldHeight = canvas.height * scale;

    const geometry = new THREE.PlaneGeometry(worldWidth, worldHeight);
    // Re-anchor the mesh origin to its top-left corner to align cleanly with the parsed JSON coordinates
    geometry.translate(worldWidth / 2, -worldHeight, 0);

    const material = new THREE.MeshBasicMaterial({
        map: texture,
        transparent: true,
        opacity: 0.50,
        depthWrite: false
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.z = 0.05; // Float above the highest LOD tapestry (z=0.02)
    mesh.frustumCulled = false; // Prevent pop-in of wide text strings
    mesh.renderOrder = 999; // Ensure text always renders ON TOP of all tapestry tiles
    canvasGroup.add(mesh);
    return mesh;
}

fetch('bayeux_data.json?v=1').then(res => res.json()).then(payload => {
    uiDict = payload.ui;
    const data = payload.tituli;

    if (isAuthoringMode) {
        const savedData = localStorage.getItem('bayeux-tituli');
        if (savedData) {
            try {
                const parsed = JSON.parse(savedData);
                data.forEach(t => {
                    const match = parsed.find(p => p.scene === t.scene);
                    if (match && match.x !== undefined) {
                        t.x = match.x;
                        t.y = match.y;
                    }
                });
            } catch (e) { console.error("Error parsing local storage", e); }
        }
    }

    tituliData = data;
    buildTourPOIs(tituliData);
    
    // Apply UI translations now that uiDict is populated
    changeLanguage(currentLanguage);

    // Force the browser to download the custom font (since it's not used in standard DOM) before rendering
    document.fonts.load('80px "MedievalSharp"').then(() => {
        data.forEach(t => {
            const textStr = (t.translations && t.translations[currentLanguage]) ? t.translations[currentLanguage].text : t.translations['en'].text;
            const mesh = createTextMesh(textStr, t.x !== undefined);
            mesh.visible = false;

            const annObj = { data: t, mesh: mesh, isHovered: false, currentHover: 0 };
            mesh.userData.annotation = annObj;
            annotations.push(annObj);
        });
        if (urlParams.get('notes') === '1') {
            openNotes();
        }
        if (urlParams.get('menu') === '1') {
            openMobileMenu();
        }
        if (urlParams.get('tour') === '1') {
            startTour();
        }
    });
});

const hoverRaycaster = new THREE.Raycaster();
let lastCameraXForFading = 0;
let smoothedCameraSpeed = 0;

window.updateAnnotations = function () {
    // Calculate true camera speed
    const currentSpeed = Math.abs(camera.position.x - lastCameraXForFading);
    smoothedCameraSpeed = smoothedCameraSpeed * 0.8 + currentSpeed * 0.2;
    lastCameraXForFading = camera.position.x;

    let scrollOpacityMult = 1.0;
    if (isAuthoringMode) scrollOpacityMult = 1.0;

    // Perform raycasting for hover detection if we have valid mouse coordinates
    let hoveredMesh = null;
    if (mouseCoords.x !== -9999 && !isDragging && !isMouseDown) {
        hoverRaycaster.setFromCamera(mouseCoords, camera);
        // Extract visible annotation meshes
        const annMeshes = annotations.map(a => a.mesh).filter(m => m && m.visible);
        const intersects = hoverRaycaster.intersectObjects(annMeshes, false);
        if (intersects.length > 0) {
            hoveredMesh = intersects[0].object;
        }

        // Change mouse cursor to indicate clickability
        if (!isAuthoringMode) {
            document.body.style.cursor = hoveredMesh ? 'pointer' : 'default';
        }
    }

    // UI button state controls visibility
    // (showSupertitles is now a global variable updated by the click listener)

    annotations.forEach((ann, index) => {
        if (!ann.mesh) return;

        const isNotesOpen = document.getElementById('context-scroll') && window.getComputedStyle(document.getElementById('context-scroll')).display !== 'none';
        const isTourRunning = typeof isTourActive !== 'undefined' && isTourActive;

        if (!showSupertitles || ann.data.x === undefined || isNotesOpen || isTourRunning || initialSlowZoom) {
            ann.mesh.visible = false;
            return;
        }

        // We rely on Three.js native frustum culling rather than hardcoded distance checks

        ann.mesh.visible = true;
        ann.mesh.position.x = ann.data.x;
        ann.mesh.position.y = ann.data.y;

        // Smoothly transition opacity to 1.0 when hovered, 0.50 normally (or 0.85 when touring)
        if (ann.currentOpacity === undefined) ann.currentOpacity = 0.50;

        const baseOpacity = (typeof isTourActive !== 'undefined' && isTourActive) ? 0.85 : 0.50;
        const targetOpacity = (hoveredMesh === ann.mesh || isAuthoringMode) ? 1.0 : baseOpacity;
        ann.currentOpacity += (targetOpacity - ann.currentOpacity) * 0.2; // Smooth lerp

        ann.mesh.material.opacity = ann.currentOpacity * scrollOpacityMult;

        // Add a subtle scale effect on hover as well
        const targetScale = (hoveredMesh === ann.mesh) ? 1.002 : 1.0; // Drastically reduced hover scale to prevent perceived horizontal shifting
        if (ann.currentScale === undefined) ann.currentScale = 1.0;
        ann.currentScale += (targetScale - ann.currentScale) * 0.2;
        ann.mesh.scale.set(ann.currentScale, ann.currentScale, 1);
    });

    if (isAuthoringMode) {
        const activeAnn = draggedAnnotation ? draggedAnnotation : (hoveredMesh ? hoveredMesh.userData.annotation : null);
        const infoDiv = document.getElementById('auth-info');
        if (activeAnn) {
            infoDiv.style.display = 'block';
            document.getElementById('auth-scene').innerText = activeAnn.data.scene;
            document.getElementById('auth-latin').innerText = activeAnn.data.latin || '';
            document.getElementById('auth-english').innerText = activeAnn.data.translations['en'].text || '';
        } else {
            infoDiv.style.display = 'none';
        }
    }
};
// --------------------------------

// Open the hidden lighting configuration dialog
document.getElementById('lighting-controls-btn').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('lighting-dialog').style.display = 'block';
});

// Close the hidden lighting configuration dialog
document.getElementById('close-lighting').addEventListener('click', () => {
    document.getElementById('lighting-dialog').style.display = 'none';
});

function toggleMusic() {
    if (!ytPlayer || !ytPlayer.getPlayerState) return; // Not loaded yet

    const btn = document.getElementById('music-toggle');
    const badge = document.getElementById('m-badge-music');
    const state = ytPlayer.getPlayerState();

    if (state === YT.PlayerState.PLAYING || state === YT.PlayerState.BUFFERING) {
        ytPlayer.pauseVideo();
        if (btn) {
            btn.innerHTML = '►';
            btn.style.background = 'rgba(20,20,20,0.8)';
        }
        if (badge) {
            badge.innerText = 'OFF';
            badge.style.color = '#888';
            badge.style.borderColor = 'rgba(255,255,255,0.15)';
            badge.style.background = 'rgba(255,255,255,0.05)';
        }
    } else {
        ytPlayer.playVideo();
        if (btn) {
            btn.innerHTML = '||';
            btn.style.background = 'rgba(214, 168, 72, 0.2)';
        }
        if (badge) {
            badge.innerText = 'ON';
            badge.style.color = '#d6a848';
            badge.style.borderColor = 'rgba(214,168,72,0.35)';
            badge.style.background = 'rgba(214,168,72,0.18)';
        }
    }
}

// Toggle the background YouTube audio player state between play and pause
const musicToggleBtn = document.getElementById('music-toggle');
if (musicToggleBtn) {
    musicToggleBtn.addEventListener('click', toggleMusic);
}

// Initialize language settings on boot

