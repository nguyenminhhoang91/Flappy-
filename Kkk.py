"""
SUBWAY SURFERS STYLE - Endless Runner
Python + Streamlit + HTML5 Canvas + JavaScript
Complete playable game in one file.
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Subway Rush",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit chrome completely
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background: #0a0a1a; padding: 0 !important; margin: 0 !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    iframe {border: none !important;}
    div[data-testid="stToolbar"] {display: none;}
    section[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Subway Rush</title>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    html, body {
        width: 100%; height: 100%; overflow: hidden;
        background: #0a0a1a; font-family: 'Segoe UI', system-ui, sans-serif;
        touch-action: none; user-select: none;
    }
    #gameContainer {
        position: relative; width: 100vw; height: 100vh;
        display: flex; justify-content: center; align-items: center;
        background: linear-gradient(180deg, #1a1a3e 0%, #0a0a1a 100%);
    }
    canvas {
        display: block; max-width: 100%; max-height: 100%;
        border-radius: 12px; box-shadow: 0 0 40px rgba(0,200,255,0.3);
        background: #111;
    }
    /* UI Overlay */
    #ui {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 10;
    }
    #ui > * { pointer-events: auto; }
    .screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background: linear-gradient(135deg, #1a0033 0%, #000033 50%, #001a33 100%);
        color: #fff; text-align: center; padding: 20px;
    }
    .screen.hidden { display: none; }
    .logo {
        font-size: clamp(2.2rem, 8vw, 4rem); font-weight: 900;
        background: linear-gradient(90deg, #ff00cc, #00ffff, #ffff00);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255,0,200,0.5);
        margin-bottom: 8px; letter-spacing: 2px;
    }
    .subtitle { color: #aaa; margin-bottom: 30px; font-size: 1rem; }
    .btn {
        background: linear-gradient(90deg, #ff00aa, #00ccff);
        border: none; color: #fff; font-size: 1.15rem; font-weight: 700;
        padding: 14px 48px; margin: 8px; border-radius: 50px;
        cursor: pointer; transition: transform 0.15s, box-shadow 0.15s;
        box-shadow: 0 4px 20px rgba(255,0,170,0.4);
        min-width: 200px;
    }
    .btn:hover, .btn:active { transform: scale(1.06); box-shadow: 0 6px 28px rgba(0,200,255,0.6); }
    .btn.secondary {
        background: linear-gradient(90deg, #333, #555);
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .btn.small { padding: 10px 28px; font-size: 0.95rem; min-width: 140px; }
    .stats-bar {
        position: absolute; top: 12px; left: 0; right: 0;
        display: flex; justify-content: space-around; align-items: center;
        padding: 8px 16px; background: rgba(0,0,0,0.55);
        backdrop-filter: blur(8px); border-radius: 0 0 16px 16px;
        font-size: 0.95rem; font-weight: 600; color: #fff;
        pointer-events: none;
    }
    .stat { display: flex; align-items: center; gap: 6px; }
    .stat span { color: #00ffff; }
    /* Touch controls */
    #touchControls {
        position: absolute; bottom: 20px; left: 0; right: 0;
        display: none; justify-content: center; gap: 12px;
        pointer-events: none;
    }
    .touch-btn {
        width: 64px; height: 64px; border-radius: 50%;
        background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.35);
        color: #fff; font-size: 1.6rem; display: flex;
        justify-content: center; align-items: center;
        pointer-events: auto; backdrop-filter: blur(4px);
    }
    .touch-btn:active { background: rgba(0,200,255,0.4); }
    /* Pause / HUD buttons */
    #hudButtons {
        position: absolute; top: 60px; right: 12px;
        display: none; flex-direction: column; gap: 8px;
    }
    .hud-btn {
        width: 44px; height: 44px; border-radius: 50%;
        background: rgba(0,0,0,0.5); border: 2px solid rgba(255,255,255,0.3);
        color: #fff; font-size: 1.2rem; cursor: pointer;
        display: flex; justify-content: center; align-items: center;
    }
    /* Shop / Missions lists */
    .list-box {
        max-height: 50vh; overflow-y: auto; width: 90%; max-width: 360px;
        margin: 16px 0; text-align: left;
    }
    .list-item {
        background: rgba(255,255,255,0.08); border-radius: 12px;
        padding: 12px 16px; margin: 8px 0; display: flex;
        justify-content: space-between; align-items: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .list-item.owned { border-color: #00ff99; }
    .list-item .price { color: #ffcc00; font-weight: 700; }
    .mission-item { flex-direction: column; align-items: flex-start; gap: 4px; }
    .progress-bar {
        width: 100%; height: 8px; background: #333; border-radius: 4px; overflow: hidden;
    }
    .progress-fill { height: 100%; background: linear-gradient(90deg,#00ff99,#00ccff); transition: width 0.3s; }
    .powerup-icons {
        position: absolute; bottom: 100px; left: 12px;
        display: flex; gap: 8px; pointer-events: none;
    }
    .powerup-icon {
        width: 40px; height: 40px; border-radius: 8px;
        background: rgba(0,0,0,0.5); border: 2px solid #fff;
        display: flex; justify-content: center; align-items: center;
        font-size: 1.2rem; opacity: 0.3;
    }
    .powerup-icon.active { opacity: 1; border-color: #00ff99; box-shadow: 0 0 12px #00ff99; }
    @media (max-width: 600px) {
        .btn { min-width: 160px; padding: 12px 32px; font-size: 1rem; }
        #touchControls { display: flex; }
    }
</style>
</head>
<body>
<div id="gameContainer">
    <canvas id="gameCanvas" width="480" height="720"></canvas>
    <div id="ui">
        <!-- MAIN MENU -->
        <div id="menuScreen" class="screen">
            <div class="logo">SUBWAY RUSH</div>
            <div class="subtitle">Endless Runner Adventure</div>
            <div style="margin-bottom:16px;font-size:1.1rem;">
                🏆 High: <span id="menuHighScore">0</span> &nbsp;|&nbsp; 🪙 <span id="menuCoins">0</span>
            </div>
            <button class="btn" onclick="startGame()">▶ PLAY</button>
            <button class="btn secondary" onclick="showScreen('shopScreen')">🛒 SHOP</button>
            <button class="btn secondary" onclick="showScreen('missionsScreen')">📋 MISSIONS</button>
            <button class="btn secondary" onclick="showScreen('settingsScreen')">⚙ SETTINGS</button>
        </div>

        <!-- SHOP -->
        <div id="shopScreen" class="screen hidden">
            <div class="logo" style="font-size:2rem;">SHOP</div>
            <div style="margin:8px 0;">🪙 <span id="shopCoins">0</span></div>
            <div class="list-box" id="shopList"></div>
            <button class="btn secondary small" onclick="showScreen('menuScreen')">← BACK</button>
        </div>

        <!-- MISSIONS -->
        <div id="missionsScreen" class="screen hidden">
            <div class="logo" style="font-size:2rem;">MISSIONS</div>
            <div class="list-box" id="missionsList"></div>
            <button class="btn secondary small" onclick="showScreen('menuScreen')">← BACK</button>
        </div>

        <!-- SETTINGS -->
        <div id="settingsScreen" class="screen hidden">
            <div class="logo" style="font-size:2rem;">SETTINGS</div>
            <div style="margin:20px 0;">
                <label style="display:block;margin:12px 0;">
                    Sound: <input type="checkbox" id="soundToggle" checked onchange="toggleSound()">
                </label>
                <label style="display:block;margin:12px 0;">
                    Vibration: <input type="checkbox" id="vibToggle" checked>
                </label>
            </div>
            <button class="btn secondary small" onclick="showScreen('menuScreen')">← BACK</button>
        </div>

        <!-- GAME OVER -->
        <div id="gameOverScreen" class="screen hidden">
            <div class="logo" style="font-size:2.5rem;">GAME OVER</div>
            <div style="font-size:1.4rem;margin:16px 0;">
                Score: <span id="finalScore" style="color:#00ffff;">0</span>
            </div>
            <div style="margin-bottom:8px;">Coins collected: <span id="finalCoins">0</span></div>
            <div style="margin-bottom:20px;">High Score: <span id="finalHigh">0</span></div>
            <button class="btn" onclick="startGame()">↻ PLAY AGAIN</button>
            <button class="btn secondary" onclick="showScreen('menuScreen')">⌂ MENU</button>
        </div>

        <!-- PAUSE -->
        <div id="pauseScreen" class="screen hidden" style="background:rgba(0,0,0,0.75);">
            <div class="logo" style="font-size:2.5rem;">PAUSED</div>
            <button class="btn" onclick="resumeGame()">▶ CONTINUE</button>
            <button class="btn secondary" onclick="quitToMenu()">⌂ QUIT</button>
        </div>

        <!-- In-game HUD -->
        <div id="statsBar" class="stats-bar" style="display:none;">
            <div class="stat">⭐ <span id="hudScore">0</span></div>
            <div class="stat">🪙 <span id="hudCoins">0</span></div>
            <div class="stat">🏆 <span id="hudHigh">0</span></div>
        </div>
        <div id="hudButtons" style="display:none;">
            <button class="hud-btn" onclick="pauseGame()">⏸</button>
        </div>
        <div id="powerupIcons" class="powerup-icons" style="display:none;">
            <div class="powerup-icon" id="puMagnet" title="Magnet">🧲</div>
            <div class="powerup-icon" id="puJump" title="Super Jump">👟</div>
            <div class="powerup-icon" id="puScore" title="2x Score">✖2</div>
            <div class="powerup-icon" id="puShield" title="Shield">🛡</div>
        </div>
        <div id="touchControls">
            <button class="touch-btn" ontouchstart="handleTouch('left')" onmousedown="handleTouch('left')">◀</button>
            <button class="touch-btn" ontouchstart="handleTouch('up')" onmousedown="handleTouch('up')">▲</button>
            <button class="touch-btn" ontouchstart="handleTouch('down')" onmousedown="handleTouch('down')">▼</button>
            <button class="touch-btn" ontouchstart="handleTouch('right')" onmousedown="handleTouch('right')">▶</button>
        </div>
    </div>
</div>

<script>
// ==================== DATA & PERSISTENCE ====================
const STORAGE_KEY = 'subwayRushSave_v1';
let save = {
    highScore: 0,
    coins: 0,
    unlockedSkins: [0],
    currentSkin: 0,
    missions: [
        { id: 1, name: 'Collect 50 coins', target: 50, progress: 0, reward: 100, type: 'coins' },
        { id: 2, name: 'Score 500 points', target: 500, progress: 0, reward: 150, type: 'score' },
        { id: 3, name: 'Survive 30 seconds', target: 30, progress: 0, reward: 120, type: 'time' },
        { id: 4, name: 'Collect 20 coins in one run', target: 20, progress: 0, reward: 80, type: 'runCoins' },
        { id: 5, name: 'Reach 1000 score', target: 1000, progress: 0, reward: 200, type: 'score' }
    ],
    sound: true,
    vibration: true
};

function loadSave() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
            const data = JSON.parse(raw);
            Object.assign(save, data);
            // ensure missions exist
            if (!save.missions || save.missions.length < 5) {
                save.missions = [
                    { id: 1, name: 'Collect 50 coins', target: 50, progress: 0, reward: 100, type: 'coins' },
                    { id: 2, name: 'Score 500 points', target: 500, progress: 0, reward: 150, type: 'score' },
                    { id: 3, name: 'Survive 30 seconds', target: 30, progress: 0, reward: 120, type: 'time' },
                    { id: 4, name: 'Collect 20 coins in one run', target: 20, progress: 0, reward: 80, type: 'runCoins' },
                    { id: 5, name: 'Reach 1000 score', target: 1000, progress: 0, reward: 200, type: 'score' }
                ];
            }
        }
    } catch(e) {}
    updateMenuStats();
}
function persist() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(save)); } catch(e) {}
}

// Skins
const SKINS = [
    { id: 0, name: 'Classic Runner', price: 0, color: '#00ccff', hair: '#ffcc00' },
    { id: 1, name: 'Neon Ninja', price: 300, color: '#ff00aa', hair: '#00ff99' },
    { id: 2, name: 'Golden Hero', price: 500, color: '#ffcc00', hair: '#ff6600' },
    { id: 3, name: 'Shadow Ghost', price: 800, color: '#aa00ff', hair: '#ffffff' },
    { id: 4, name: 'Fire Blaze', price: 1200, color: '#ff3300', hair: '#ffaa00' }
];

// ==================== GAME STATE ====================
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let W = 480, H = 720;
const LANES = [W * 0.25, W * 0.5, W * 0.75];
const LANE_COUNT = 3;

let state = 'menu'; // menu | playing | paused | gameover
let player, obstacles, coins, powerups, particles;
let score = 0, runCoins = 0, distance = 0, speed = 6;
let combo = 0, lastCoinTime = 0;
let gameTime = 0, frame = 0;
let activePowerups = { magnet: 0, jump: 0, scorex2: 0, shield: 0 };
let invincible = 0;
let keys = {};
let touchStartX = 0, touchStartY = 0;

// ==================== PLAYER ====================
function createPlayer() {
    return {
        lane: 1,
        x: LANES[1],
        y: H * 0.72,
        targetX: LANES[1],
        width: 36,
        height: 56,
        jumping: false,
        jumpY: 0,
        jumpVel: 0,
        sliding: false,
        slideTimer: 0,
        animFrame: 0
    };
}

// ==================== OBJECTS ====================
function spawnObstacle() {
    const lane = Math.floor(Math.random() * 3);
    const types = ['train', 'barrier', 'box', 'lowbarrier'];
    const type = types[Math.floor(Math.random() * types.length)];
    let h = 70, w = 50;
    if (type === 'train') { h = 110; w = 58; }
    else if (type === 'barrier') { h = 80; w = 46; }
    else if (type === 'lowbarrier') { h = 36; w = 50; }
    else { h = 55; w = 48; }
    obstacles.push({
        lane, x: LANES[lane], y: -120, type, w, h,
        passed: false
    });
}

function spawnCoin() {
    const lane = Math.floor(Math.random() * 3);
    coins.push({
        lane, x: LANES[lane], y: -40, r: 12, collected: false
    });
}

function spawnPowerup() {
    if (Math.random() > 0.015) return;
    const types = ['magnet', 'jump', 'scorex2', 'shield'];
    const type = types[Math.floor(Math.random() * types.length)];
    const lane = Math.floor(Math.random() * 3);
    powerups.push({
        lane, x: LANES[lane], y: -50, type, r: 18, collected: false
    });
}

// ==================== INPUT ====================
document.addEventListener('keydown', e => {
    keys[e.code] = true;
    if (state === 'playing') {
        if (e.code === 'ArrowLeft' || e.code === 'KeyA') moveLane(-1);
        if (e.code === 'ArrowRight' || e.code === 'KeyD') moveLane(1);
        if (e.code === 'ArrowUp' || e.code === 'KeyW' || e.code === 'Space') jump();
        if (e.code === 'ArrowDown' || e.code === 'KeyS') slide();
        if (e.code === 'Escape' || e.code === 'KeyP') pauseGame();
    }
    e.preventDefault();
});
document.addEventListener('keyup', e => { keys[e.code] = false; });

// Swipe
canvas.addEventListener('touchstart', e => {
    const t = e.changedTouches[0];
    touchStartX = t.clientX; touchStartY = t.clientY;
}, { passive: true });
canvas.addEventListener('touchend', e => {
    if (state !== 'playing') return;
    const t = e.changedTouches[0];
    const dx = t.clientX - touchStartX;
    const dy = t.clientY - touchStartY;
    if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 30) {
        moveLane(dx > 0 ? 1 : -1);
    } else if (Math.abs(dy) > 30) {
        if (dy < 0) jump(); else slide();
    }
}, { passive: true });

function handleTouch(dir) {
    if (state !== 'playing') return;
    if (dir === 'left') moveLane(-1);
    if (dir === 'right') moveLane(1);
    if (dir === 'up') jump();
    if (dir === 'down') slide();
}

function moveLane(dir) {
    if (player.sliding) return;
    const newLane = Math.max(0, Math.min(2, player.lane + dir));
    if (newLane !== player.lane) {
        player.lane = newLane;
        player.targetX = LANES[newLane];
    }
}
function jump() {
    if (!player.jumping && !player.sliding) {
        player.jumping = true;
        player.jumpVel = activePowerups.jump > 0 ? -16 : -13;
    }
}
function slide() {
    if (!player.jumping && !player.sliding) {
        player.sliding = true;
        player.slideTimer = 25;
    }
}

// ==================== GAME FLOW ====================
function startGame() {
    player = createPlayer();
    obstacles = [];
    coins = [];
    powerups = [];
    particles = [];
    score = 0; runCoins = 0; distance = 0; speed = 6;
    combo = 0; gameTime = 0; frame = 0;
    activePowerups = { magnet: 0, jump: 0, scorex2: 0, shield: 0 };
    invincible = 60; // short invincibility at start
    state = 'playing';
    showScreen(null);
    document.getElementById('statsBar').style.display = 'flex';
    document.getElementById('hudButtons').style.display = 'flex';
    document.getElementById('powerupIcons').style.display = 'flex';
    updateHud();
    requestAnimationFrame(loop);
}

function pauseGame() {
    if (state === 'playing') {
        state = 'paused';
        document.getElementById('pauseScreen').classList.remove('hidden');
    }
}
function resumeGame() {
    if (state === 'paused') {
        state = 'playing';
        document.getElementById('pauseScreen').classList.add('hidden');
        requestAnimationFrame(loop);
    }
}
function quitToMenu() {
    state = 'menu';
    document.getElementById('pauseScreen').classList.add('hidden');
    document.getElementById('statsBar').style.display = 'none';
    document.getElementById('hudButtons').style.display = 'none';
    document.getElementById('powerupIcons').style.display = 'none';
    showScreen('menuScreen');
    updateMenuStats();
}

function gameOver() {
    state = 'gameover';
    // Update save
    if (score > save.highScore) save.highScore = score;
    save.coins += runCoins;
    // Missions progress
    save.missions.forEach(m => {
        if (m.type === 'coins') m.progress = Math.min(m.target, m.progress + runCoins);
        if (m.type === 'score') m.progress = Math.max(m.progress, score);
        if (m.type === 'time') m.progress = Math.max(m.progress, Math.floor(gameTime));
        if (m.type === 'runCoins') m.progress = Math.max(m.progress, runCoins);
    });
    // Claim completed
    save.missions.forEach(m => {
        if (m.progress >= m.target && !m.claimed) {
            save.coins += m.reward;
            m.claimed = true;
        }
    });
    persist();
    document.getElementById('finalScore').textContent = Math.floor(score);
    document.getElementById('finalCoins').textContent = runCoins;
    document.getElementById('finalHigh').textContent = save.highScore;
    document.getElementById('statsBar').style.display = 'none';
    document.getElementById('hudButtons').style.display = 'none';
    document.getElementById('powerupIcons').style.display = 'none';
    document.getElementById('gameOverScreen').classList.remove('hidden');
    if (save.vibration && navigator.vibrate) navigator.vibrate([80, 40, 80]);
}

// ==================== UPDATE ====================
function update() {
    if (state !== 'playing') return;
    frame++;
    gameTime += 1/60;
    distance += speed;
    score += (speed * 0.15) * (activePowerups.scorex2 > 0 ? 2 : 1);
    if (frame % 300 === 0) speed = Math.min(speed + 0.35, 16);

    // Player movement
    player.x += (player.targetX - player.x) * 0.25;
    player.animFrame = (player.animFrame + 0.3) % 4;

    if (player.jumping) {
        player.jumpVel += 0.7;
        player.jumpY += player.jumpVel;
        if (player.jumpY >= 0) {
            player.jumpY = 0;
            player.jumping = false;
            player.jumpVel = 0;
        }
    }
    if (player.sliding) {
        player.slideTimer--;
        if (player.slideTimer <= 0) player.sliding = false;
    }

    // Spawn
    if (frame % Math.max(25, 55 - Math.floor(speed * 2)) === 0) spawnObstacle();
    if (frame % 18 === 0) spawnCoin();
    spawnPowerup();

    // Move obstacles
    for (let i = obstacles.length - 1; i >= 0; i--) {
        const o = obstacles[i];
        o.y += speed;
        if (o.y > H + 50) { obstacles.splice(i, 1); continue; }
        // Collision
        if (invincible <= 0 && !o.passed) {
            const px = player.x, py = player.y + player.jumpY;
            const pw = player.width, ph = player.sliding ? player.height * 0.45 : player.height;
            const pyAdj = player.sliding ? py + player.height * 0.55 : py;
            if (Math.abs(px - o.x) < (pw + o.w) * 0.4 &&
                pyAdj < o.y + o.h && pyAdj + ph > o.y) {
                // Can jump over low or slide under high
                let hit = true;
                if (o.type === 'lowbarrier' && player.jumping && player.jumpY < -20) hit = false;
                if ((o.type === 'barrier' || o.type === 'train') && player.sliding) hit = false;
                if (hit) {
                    if (activePowerups.shield > 0) {
                        activePowerups.shield = 0;
                        invincible = 90;
                        createParticles(px, py, '#00ff99');
                    } else {
                        gameOver();
                        return;
                    }
                }
            }
        }
    }

    // Coins
    for (let i = coins.length - 1; i >= 0; i--) {
        const c = coins[i];
        c.y += speed;
        // Magnet
        if (activePowerups.magnet > 0) {
            const dx = player.x - c.x;
            const dy = (player.y + player.jumpY) - c.y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            if (dist < 180) {
                c.x += dx * 0.12;
                c.y += dy * 0.12;
            }
        }
        if (c.y > H + 30) { coins.splice(i, 1); continue; }
        const px = player.x, py = player.y + player.jumpY;
        if (Math.abs(px - c.x) < 30 && Math.abs(py - c.y) < 40) {
            coins.splice(i, 1);
            runCoins++;
            combo++;
            lastCoinTime = frame;
            score += 10 * (activePowerups.scorex2 > 0 ? 2 : 1) * Math.min(combo, 5);
            createParticles(c.x, c.y, '#ffcc00');
        }
    }
    if (frame - lastCoinTime > 40) combo = 0;

    // Powerups
    for (let i = powerups.length - 1; i >= 0; i--) {
        const p = powerups[i];
        p.y += speed;
        if (p.y > H + 30) { powerups.splice(i, 1); continue; }
        const px = player.x, py = player.y + player.jumpY;
        if (Math.abs(px - p.x) < 35 && Math.abs(py - p.y) < 40) {
            powerups.splice(i, 1);
            if (p.type === 'magnet') activePowerups.magnet = 300;
            if (p.type === 'jump') activePowerups.jump = 250;
            if (p.type === 'scorex2') activePowerups.scorex2 = 280;
            if (p.type === 'shield') activePowerups.shield = 200;
            createParticles(p.x, p.y, '#00ff99');
        }
    }

    // Timers
    if (invincible > 0) invincible--;
    for (let k in activePowerups) {
        if (activePowerups[k] > 0) activePowerups[k]--;
    }

    // Particles
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx; p.y += p.vy; p.life--;
        if (p.life <= 0) particles.splice(i, 1);
    }

    updateHud();
    updatePowerupIcons();
}

function createParticles(x, y, color) {
    for (let i = 0; i < 8; i++) {
        particles.push({
            x, y,
            vx: (Math.random() - 0.5) * 6,
            vy: (Math.random() - 0.5) * 6 - 2,
            life: 20 + Math.random() * 15,
            color, size: 3 + Math.random() * 4
        });
    }
}

// ==================== DRAW ====================
function draw() {
    // Sky gradient
    const grad = ctx.createLinearGradient(0, 0, 0, H);
    grad.addColorStop(0, '#1a0a3e');
    grad.addColorStop(0.4, '#0a1a4e');
    grad.addColorStop(1, '#0a2a2a');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    // Moving city buildings (parallax)
    drawBuildings();

    // Tracks
    drawTracks();

    // Coins
    coins.forEach(c => drawCoin(c));

    // Powerups
    powerups.forEach(p => drawPowerup(p));

    // Obstacles
    obstacles.forEach(o => drawObstacle(o));

    // Player
    if (state === 'playing' || state === 'paused') drawPlayer();

    // Particles
    particles.forEach(p => {
        ctx.globalAlpha = p.life / 35;
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
    });

    // Speed lines when fast
    if (speed > 10) {
        ctx.strokeStyle = 'rgba(255,255,255,0.08)';
        ctx.lineWidth = 2;
        for (let i = 0; i < 6; i++) {
            const x = (frame * 8 + i * 80) % W;
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x - 30, H);
            ctx.stroke();
        }
    }
}

function drawBuildings() {
    const offset = (distance * 0.3) % 120;
    ctx.fillStyle = '#0d0d2a';
    for (let i = -1; i < 8; i++) {
        const x = i * 70 - offset;
        const h = 80 + (Math.sin(i * 1.7) * 40 + 40);
        ctx.fillRect(x, H * 0.35 - h, 55, h);
        // windows
        ctx.fillStyle = '#1a3a5a';
        for (let wy = 0; wy < h - 10; wy += 14) {
            for (let wx = 8; wx < 45; wx += 12) {
                if (Math.random() > 0.3) ctx.fillRect(x + wx, H * 0.35 - h + wy + 5, 6, 8);
            }
        }
        ctx.fillStyle = '#0d0d2a';
    }
}

function drawTracks() {
    // Ground
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, H * 0.55, W, H * 0.45);

    // Rails
    const railOffset = (distance * 1.2) % 40;
    ctx.strokeStyle = '#555';
    ctx.lineWidth = 4;
    // Left rail
    ctx.beginPath();
    ctx.moveTo(LANES[0] - 30, H * 0.55);
    ctx.lineTo(LANES[0] - 30, H);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(LANES[0] + 30, H * 0.55);
    ctx.lineTo(LANES[0] + 30, H);
    ctx.stroke();
    // Center
    ctx.beginPath();
    ctx.moveTo(LANES[1] - 30, H * 0.55);
    ctx.lineTo(LANES[1] - 30, H);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(LANES[1] + 30, H * 0.55);
    ctx.lineTo(LANES[1] + 30, H);
    ctx.stroke();
    // Right
    ctx.beginPath();
    ctx.moveTo(LANES[2] - 30, H * 0.55);
    ctx.lineTo(LANES[2] - 30, H);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(LANES[2] + 30, H * 0.55);
    ctx.lineTo(LANES[2] + 30, H);
    ctx.stroke();

    // Sleepers
    ctx.fillStyle = '#3a2a1a';
    for (let y = H * 0.55 - railOffset; y < H; y += 40) {
        for (let l = 0; l < 3; l++) {
            ctx.fillRect(LANES[l] - 35, y, 70, 10);
        }
    }

    // Lane dividers (dashed)
    ctx.strokeStyle = 'rgba(255,255,0,0.25)';
    ctx.lineWidth = 2;
    ctx.setLineDash([15, 15]);
    ctx.beginPath();
    ctx.moveTo((LANES[0]+LANES[1])/2, H*0.55);
    ctx.lineTo((LANES[0]+LANES[1])/2, H);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo((LANES[1]+LANES[2])/2, H*0.55);
    ctx.lineTo((LANES[1]+LANES[2])/2, H);
    ctx.stroke();
    ctx.setLineDash([]);
}

function drawPlayer() {
    const skin = SKINS[save.currentSkin] || SKINS[0];
    const px = player.x;
    const py = player.y + player.jumpY;
    const ph = player.sliding ? player.height * 0.5 : player.height;
    const pyDraw = player.sliding ? py + player.height * 0.5 : py;

    ctx.save();
    if (invincible > 0 && Math.floor(frame / 4) % 2 === 0) ctx.globalAlpha = 0.5;

    // Shadow
    ctx.fillStyle = 'rgba(0,0,0,0.3)';
    ctx.beginPath();
    ctx.ellipse(px, player.y + player.height + 5, 20, 8, 0, 0, Math.PI * 2);
    ctx.fill();

    // Body
    ctx.fillStyle = skin.color;
    roundRect(px - player.width/2, pyDraw, player.width, ph, 8);

    // Head
    if (!player.sliding) {
        ctx.fillStyle = '#ffdbac';
        ctx.beginPath();
        ctx.arc(px, pyDraw - 8, 14, 0, Math.PI * 2);
        ctx.fill();
        // Hair
        ctx.fillStyle = skin.hair;
        ctx.beginPath();
        ctx.arc(px, pyDraw - 14, 12, Math.PI, 0);
        ctx.fill();
        // Eyes
        ctx.fillStyle = '#222';
        ctx.beginPath();
        ctx.arc(px - 5, pyDraw - 9, 2.5, 0, Math.PI * 2);
        ctx.arc(px + 5, pyDraw - 9, 2.5, 0, Math.PI * 2);
        ctx.fill();
    }

    // Legs / running animation
    if (!player.sliding && !player.jumping) {
        const legOffset = Math.sin(player.animFrame * 1.5) * 8;
        ctx.fillStyle = '#222';
        ctx.fillRect(px - 12, pyDraw + ph - 5, 8, 12 + legOffset);
        ctx.fillRect(px + 4, pyDraw + ph - 5, 8, 12 - legOffset);
    }

    // Shield aura
    if (activePowerups.shield > 0) {
        ctx.strokeStyle = 'rgba(0,255,150,0.6)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(px, pyDraw + ph/2, 32, 0, Math.PI * 2);
        ctx.stroke();
    }

    ctx.restore();
}

function drawObstacle(o) {
    const x = o.x, y = o.y;
    if (o.type === 'train') {
        // Train body
        ctx.fillStyle = '#cc2222';
        roundRect(x - o.w/2, y, o.w, o.h, 6);
        // Windows
        ctx.fillStyle = '#88ccff';
        ctx.fillRect(x - o.w/2 + 8, y + 15, o.w - 16, 25);
        // Front
        ctx.fillStyle = '#aa1111';
        ctx.fillRect(x - o.w/2, y + o.h - 20, o.w, 20);
        // Lights
        ctx.fillStyle = '#ffff00';
        ctx.beginPath();
        ctx.arc(x - 12, y + o.h - 10, 5, 0, Math.PI*2);
        ctx.arc(x + 12, y + o.h - 10, 5, 0, Math.PI*2);
        ctx.fill();
    } else if (o.type === 'barrier') {
        ctx.fillStyle = '#ff6600';
        roundRect(x - o.w/2, y, o.w, o.h, 4);
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 20px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('⚠', x, y + o.h/2 + 7);
    } else if (o.type === 'lowbarrier') {
        ctx.fillStyle = '#ff3300';
        roundRect(x - o.w/2, y, o.w, o.h, 3);
        // stripes
        ctx.fillStyle = '#fff';
        for (let i = 0; i < 3; i++) {
            ctx.fillRect(x - o.w/2 + 6 + i*14, y + 8, 8, o.h - 16);
        }
    } else { // box
        ctx.fillStyle = '#8B4513';
        roundRect(x - o.w/2, y, o.w, o.h, 4);
        ctx.strokeStyle = '#5a2d0c';
        ctx.lineWidth = 2;
        ctx.strokeRect(x - o.w/2 + 4, y + 4, o.w - 8, o.h - 8);
        ctx.fillStyle = '#ffcc00';
        ctx.font = 'bold 16px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('📦', x, y + o.h/2 + 6);
    }
}

function drawCoin(c) {
    ctx.save();
    ctx.translate(c.x, c.y);
    ctx.rotate(frame * 0.1);
    // Outer
    ctx.fillStyle = '#ffcc00';
    ctx.beginPath();
    ctx.arc(0, 0, c.r, 0, Math.PI * 2);
    ctx.fill();
    // Inner
    ctx.fillStyle = '#ffaa00';
    ctx.beginPath();
    ctx.arc(0, 0, c.r * 0.65, 0, Math.PI * 2);
    ctx.fill();
    // $ 
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 12px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('$', 0, 1);
    ctx.restore();
}

function drawPowerup(p) {
    const icons = { magnet: '🧲', jump: '👟', scorex2: '✖2', shield: '🛡' };
    const colors = { magnet: '#00aaff', jump: '#ff66aa', scorex2: '#ffcc00', shield: '#00ff99' };
    ctx.fillStyle = colors[p.type] || '#fff';
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#fff';
    ctx.font = '16px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(icons[p.type] || '?', p.x, p.y + 1);
}

function roundRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
    ctx.fill();
}

// ==================== UI HELPERS ====================
function showScreen(id) {
    ['menuScreen','shopScreen','missionsScreen','settingsScreen','gameOverScreen','pauseScreen']
        .forEach(s => document.getElementById(s).classList.add('hidden'));
    if (id) {
        document.getElementById(id).classList.remove('hidden');
        if (id === 'shopScreen') renderShop();
        if (id === 'missionsScreen') renderMissions();
        if (id === 'settingsScreen') {
            document.getElementById('soundToggle').checked = save.sound;
            document.getElementById('vibToggle').checked = save.vibration;
        }
    }
}

function updateMenuStats() {
    document.getElementById('menuHighScore').textContent = save.highScore;
    document.getElementById('menuCoins').textContent = save.coins;
}

function updateHud() {
    document.getElementById('hudScore').textContent = Math.floor(score);
    document.getElementById('hudCoins').textContent = runCoins;
    document.getElementById('hudHigh').textContent = Math.max(save.highScore, Math.floor(score));
}

function updatePowerupIcons() {
    document.getElementById('puMagnet').classList.toggle('active', activePowerups.magnet > 0);
    document.getElementById('puJump').classList.toggle('active', activePowerups.jump > 0);
    document.getElementById('puScore').classList.toggle('active', activePowerups.scorex2 > 0);
    document.getElementById('puShield').classList.toggle('active', activePowerups.shield > 0);
}

function renderShop() {
    document.getElementById('shopCoins').textContent = save.coins;
    const list = document.getElementById('shopList');
    list.innerHTML = '';
    SKINS.forEach(skin => {
        const owned = save.unlockedSkins.includes(skin.id);
        const current = save.currentSkin === skin.id;
        const div = document.createElement('div');
        div.className = 'list-item' + (owned ? ' owned' : '');
        div.innerHTML = `
            <div>
                <div style="font-weight:700;">${skin.name}</div>
                <div style="font-size:0.85rem;color:#aaa;">${owned ? (current ? '✓ Equipped' : 'Owned') : 'Locked'}</div>
            </div>
            <div>
                ${owned
                    ? (current ? '<span style="color:#00ff99;">Equipped</span>'
                               : `<button class="btn small" style="padding:6px 14px;min-width:auto;" onclick="equipSkin(${skin.id})">Equip</button>`)
                    : `<span class="price">🪙 ${skin.price}</span>
                       <button class="btn small" style="padding:6px 14px;min-width:auto;margin-left:8px;" onclick="buySkin(${skin.id})">Buy</button>`
                }
            </div>
        `;
        list.appendChild(div);
    });
}

function buySkin(id) {
    const skin = SKINS.find(s => s.id === id);
    if (!skin || save.unlockedSkins.includes(id)) return;
    if (save.coins >= skin.price) {
        save.coins -= skin.price;
        save.unlockedSkins.push(id);
        save.currentSkin = id;
        persist();
        renderShop();
        updateMenuStats();
    } else {
        alert('Not enough coins!');
    }
}
function equipSkin(id) {
    if (save.unlockedSkins.includes(id)) {
        save.currentSkin = id;
        persist();
        renderShop();
    }
}

function renderMissions() {
    const list = document.getElementById('missionsList');
    list.innerHTML = '';
    save.missions.forEach(m => {
        const pct = Math.min(100, (m.progress / m.target) * 100);
        const done = m.progress >= m.target;
        const div = document.createElement('div');
        div.className = 'list-item mission-item';
        div.innerHTML = `
            <div style="width:100%;display:flex;justify-content:space-between;">
                <span style="font-weight:600;">${m.name}</span>
                <span class="price">🪙 ${m.reward}</span>
            </div>
            <div style="width:100%;font-size:0.85rem;color:#aaa;">
                ${Math.min(m.progress, m.target)} / ${m.target}
                ${done ? (m.claimed ? ' ✓ Claimed' : ' ✓ Complete!') : ''}
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
        `;
        list.appendChild(div);
    });
}

function toggleSound() {
    save.sound = document.getElementById('soundToggle').checked;
    persist();
}

// ==================== LOOP ====================
function loop() {
    if (state === 'playing') {
        update();
        draw();
        requestAnimationFrame(loop);
    } else if (state === 'paused') {
        draw(); // keep last frame
    }
}

// Resize
function resize() {
    const container = document.getElementById('gameContainer');
    const maxW = Math.min(window.innerWidth, 480);
    const maxH = window.innerHeight;
    const ratio = 480 / 720;
    let cw = maxW, ch = maxW / ratio;
    if (ch > maxH) { ch = maxH; cw = ch * ratio; }
    canvas.style.width = cw + 'px';
    canvas.style.height = ch + 'px';
}
window.addEventListener('resize', resize);
resize();

// Init
loadSave();
showScreen('menuScreen');
draw(); // initial draw for menu background feel
</script>
</body>
</html>
"""

# Render the game full-screen
components.html(GAME_HTML, height=780, scrolling=False)
