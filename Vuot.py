"""
SUBWAY RUSH - Endless Runner (Upgraded Graphics + Performance)
Python + Streamlit + HTML5 Canvas + JavaScript
Optimized for iOS & PC
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Subway Rush",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    #MainMenu, footer, header, div[data-testid="stToolbar"], section[data-testid="stSidebar"] {display:none!important;visibility:hidden!important;}
    .stApp {background:#050510;padding:0!important;margin:0!important;}
    .block-container {padding:0!important;max-width:100%!important;}
    iframe {border:none!important;}
</style>
""", unsafe_allow_html=True)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<title>Subway Rush</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;-webkit-touch-callout:none;user-select:none;}
html,body{width:100%;height:100%;overflow:hidden;background:#050510;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;touch-action:none;}
#wrap{position:relative;width:100vw;height:100vh;height:100dvh;display:flex;justify-content:center;align-items:center;background:linear-gradient(180deg,#0d0d2b,#050510);}
canvas{display:block;border-radius:0;background:#0a0a18;}
#ui{position:absolute;inset:0;pointer-events:none;z-index:20;}
#ui>*{pointer-events:auto;}
.screen{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;background:linear-gradient(160deg,#1a0040 0%,#000028 45%,#001a30 100%);color:#fff;text-align:center;padding:20px;overflow-y:auto;}
.screen.hidden{display:none!important;}
.logo{font-size:clamp(2rem,7.5vw,3.6rem);font-weight:900;background:linear-gradient(90deg,#ff2d95,#00e5ff,#ffe600);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:1px;margin-bottom:6px;filter:drop-shadow(0 0 12px rgba(255,45,149,.5));}
.sub{color:#9ab;margin-bottom:22px;font-size:.95rem;}
.btn{background:linear-gradient(90deg,#ff2d95,#00c8ff);border:none;color:#fff;font-size:1.1rem;font-weight:700;padding:13px 42px;margin:7px;border-radius:50px;cursor:pointer;box-shadow:0 4px 18px rgba(255,45,149,.45);min-width:190px;transition:transform .12s;}
.btn:active{transform:scale(1.05);}
.btn.sec{background:linear-gradient(90deg,#2a2a4a,#3a3a5a);box-shadow:0 3px 12px rgba(0,0,0,.4);}
.btn.sm{padding:9px 22px;font-size:.9rem;min-width:120px;}
.hud{position:absolute;top:0;left:0;right:0;display:none;justify-content:space-around;align-items:center;padding:10px 14px;padding-top:max(10px,env(safe-area-inset-top));background:rgba(0,0,0,.6);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);font-size:.95rem;font-weight:700;color:#fff;pointer-events:none;z-index:30;}
.hud span{color:#00e5ff;}
#pauseBtn{position:absolute;top:max(52px,calc(env(safe-area-inset-top)+44px));right:12px;width:42px;height:42px;border-radius:50%;background:rgba(0,0,0,.55);border:2px solid rgba(255,255,255,.3);color:#fff;font-size:1.15rem;display:none;justify-content:center;align-items:center;cursor:pointer;z-index:30;}
#touchPad{position:absolute;bottom:max(16px,env(safe-area-inset-bottom));left:0;right:0;display:none;justify-content:center;gap:14px;z-index:30;pointer-events:none;}
.tbtn{width:58px;height:58px;border-radius:50%;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.28);color:#fff;font-size:1.45rem;display:flex;justify-content:center;align-items:center;pointer-events:auto;backdrop-filter:blur(4px);}
.tbtn:active{background:rgba(0,200,255,.4);}
.list{max-height:48vh;overflow-y:auto;width:92%;max-width:340px;margin:12px 0;text-align:left;-webkit-overflow-scrolling:touch;}
.item{background:rgba(255,255,255,.07);border-radius:12px;padding:11px 14px;margin:7px 0;display:flex;justify-content:space-between;align-items:center;border:1px solid rgba(255,255,255,.1);}
.item.own{border-color:#00e89a;}
.price{color:#ffd000;font-weight:700;}
.purow{position:absolute;bottom:90px;left:10px;display:none;gap:7px;z-index:25;pointer-events:none;}
.pui{width:36px;height:36px;border-radius:8px;background:rgba(0,0,0,.5);border:2px solid rgba(255,255,255,.25);display:flex;justify-content:center;align-items:center;font-size:1.1rem;opacity:.25;}
.pui.on{opacity:1;border-color:#00e89a;box-shadow:0 0 10px #00e89a;}
@media(max-width:700px){#touchPad{display:flex;}}
</style>
</head>
<body>
<div id="wrap">
<canvas id="c" width="400" height="700"></canvas>
<div id="ui">
  <div id="menu" class="screen">
    <div class="logo">SUBWAY RUSH</div>
    <div class="sub">Endless Runner</div>
    <div style="margin-bottom:14px;font-size:1.05rem;">🏆 <span id="mHigh">0</span> &nbsp;|&nbsp; 🪙 <span id="mCoin">0</span></div>
    <button class="btn" id="btnPlay">▶ PLAY</button>
    <button class="btn sec" id="btnShop">🛒 SHOP</button>
    <button class="btn sec" id="btnMiss">📋 MISSIONS</button>
    <button class="btn sec" id="btnSet">⚙ SETTINGS</button>
  </div>
  <div id="shop" class="screen hidden">
    <div class="logo" style="font-size:1.8rem;">SHOP</div>
    <div style="margin:6px 0;">🪙 <span id="sCoin">0</span></div>
    <div class="list" id="shopList"></div>
    <button class="btn sec sm" id="btnBackShop">← BACK</button>
  </div>
  <div id="miss" class="screen hidden">
    <div class="logo" style="font-size:1.8rem;">MISSIONS</div>
    <div class="list" id="missList"></div>
    <button class="btn sec sm" id="btnBackMiss">← BACK</button>
  </div>
  <div id="set" class="screen hidden">
    <div class="logo" style="font-size:1.8rem;">SETTINGS</div>
    <label style="display:block;margin:14px 0;font-size:1rem;">🔊 Sound <input type="checkbox" id="chkSound" checked></label>
    <label style="display:block;margin:14px 0;font-size:1rem;">📳 Vibration <input type="checkbox" id="chkVib" checked></label>
    <button class="btn sec sm" id="btnBackSet">← BACK</button>
  </div>
  <div id="over" class="screen hidden">
    <div class="logo" style="font-size:2.2rem;">GAME OVER</div>
    <div style="font-size:1.35rem;margin:14px 0;">Score: <span id="fScore" style="color:#00e5ff;">0</span></div>
    <div style="margin-bottom:6px;">Coins: <span id="fCoin">0</span></div>
    <div style="margin-bottom:18px;">High Score: <span id="fHigh">0</span></div>
    <button class="btn" id="btnRetry">↻ PLAY AGAIN</button>
    <button class="btn sec" id="btnMenu">⌂ MENU</button>
  </div>
  <div id="pause" class="screen hidden" style="background:rgba(0,0,0,.78);">
    <div class="logo" style="font-size:2.2rem;">PAUSED</div>
    <button class="btn" id="btnResume">▶ CONTINUE</button>
    <button class="btn sec" id="btnQuit">⌂ QUIT</button>
  </div>
  <div class="hud" id="hud">
    <div>⭐ <span id="hScore">0</span></div>
    <div>🪙 <span id="hCoin">0</span></div>
    <div>🏆 <span id="hHigh">0</span></div>
  </div>
  <button id="pauseBtn">⏸</button>
  <div class="purow" id="purow">
    <div class="pui" id="pMag">🧲</div>
    <div class="pui" id="pJmp">👟</div>
    <div class="pui" id="pX2">✖2</div>
    <div class="pui" id="pShd">🛡</div>
  </div>
  <div id="touchPad">
    <div class="tbtn" data-d="L">◀</div>
    <div class="tbtn" data-d="U">▲</div>
    <div class="tbtn" data-d="D">▼</div>
    <div class="tbtn" data-d="R">▶</div>
  </div>
</div>
</div>

<script>
(function(){
"use strict";

const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d', {alpha:false});
const W = 400, H = 700;
const LANES = [W*0.22, W*0.5, W*0.78];

const KEY = 'srush_v2';
let S = {
  high:0, coins:0, skin:0, unlocked:[0],
  miss:[
    {n:'Collect 50 coins',t:50,p:0,r:100,ty:'c'},
    {n:'Score 500',t:500,p:0,r:150,ty:'s'},
    {n:'Survive 30s',t:30,p:0,r:120,ty:'t'},
    {n:'20 coins / run',t:20,p:0,r:80,ty:'rc'},
    {n:'Reach 1000',t:1000,p:0,r:200,ty:'s'}
  ],
  sound:true, vib:true
};
try{const r=localStorage.getItem(KEY);if(r)Object.assign(S,JSON.parse(r));}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}}

const SKINS=[
  {id:0,n:'Classic',pr:0,body:'#00b4ff',hair:'#ffd000',skin:'#ffdbac'},
  {id:1,n:'Neon Ninja',pr:300,body:'#ff2d95',hair:'#00e89a',skin:'#ffdbac'},
  {id:2,n:'Golden',pr:500,body:'#ffd000',hair:'#ff6a00',skin:'#ffe0b0'},
  {id:3,n:'Shadow',pr:800,body:'#9b30ff',hair:'#eee',skin:'#d0c0e0'},
  {id:4,n:'Blaze',pr:1200,body:'#ff3a00',hair:'#ffaa00',skin:'#ffdbac'}
];

let state='menu';
let player,obs,coins,pups,parts;
let score=0,runC=0,dist=0,spd=5.5,combo=0,lastC=0,gTime=0,frame=0;
let pu={mag:0,jmp:0,x2:0,shd:0},inv=0;
let tSX=0,tSY=0;
let raf=0;

const BLD=[90,130,70,150,100,160,80,140,110,95,155,75];

function mkPlayer(){
  return{lane:1,x:LANES[1],tx:LANES[1],y:H*0.70,w:34,h:52,jp:false,jy:0,jv:0,sl:false,st:0,af:0};
}

function spObs(){
  const lane=Math.floor(Math.random()*3);
  const types=['train','bar','box','low'];
  const type=types[Math.floor(Math.random()*types.length)];
  let h=60,w=48;
  if(type==='train'){h=100;w=54;}
  else if(type==='bar'){h=72;w=44;}
  else if(type==='low'){h=32;w=48;}
  obs.push({lane,x:LANES[lane],y:-130,type,w,h});
}
function spCoin(){
  const lane=Math.floor(Math.random()*3);
  coins.push({lane,x:LANES[lane],y:-30,r:11,got:false});
}
function spPup(){
  if(Math.random()>0.012)return;
  const types=['mag','jmp','x2','shd'];
  const type=types[Math.floor(Math.random()*types.length)];
  const lane=Math.floor(Math.random()*3);
  pups.push({lane,x:LANES[lane],y:-40,type,r:16,got:false});
}

function moveL(d){
  if(player.sl)return;
  const nl=Math.max(0,Math.min(2,player.lane+d));
  if(nl!==player.lane){player.lane=nl;player.tx=LANES[nl];}
}
function doJump(){
  if(!player.jp&&!player.sl){player.jp=true;player.jv=pu.jmp>0?-15.5:-12.5;}
}
function doSlide(){
  if(!player.jp&&!player.sl){player.sl=true;player.st=22;}
}

document.addEventListener('keydown',e=>{
  if(state!=='playing')return;
  if(e.code==='ArrowLeft'||e.code==='KeyA')moveL(-1);
  if(e.code==='ArrowRight'||e.code==='KeyD')moveL(1);
  if(e.code==='ArrowUp'||e.code==='KeyW'||e.code==='Space')doJump();
  if(e.code==='ArrowDown'||e.code==='KeyS')doSlide();
  if(e.code==='Escape'||e.code==='KeyP')doPause();
  e.preventDefault();
},{passive:false});

canvas.addEventListener('touchstart',e=>{
  const t=e.changedTouches[0];tSX=t.clientX;tSY=t.clientY;
},{passive:true});
canvas.addEventListener('touchend',e=>{
  if(state!=='playing')return;
  const t=e.changedTouches[0];
  const dx=t.clientX-tSX,dy=t.clientY-tSY;
  if(Math.abs(dx)>Math.abs(dy)&&Math.abs(dx)>28)moveL(dx>0?1:-1);
  else if(Math.abs(dy)>28){if(dy<0)doJump();else doSlide();}
},{passive:true});

document.getElementById('touchPad').addEventListener('touchstart',e=>{
  e.preventDefault();
  const d=e.target.closest('.tbtn');
  if(!d||state!=='playing')return;
  const dir=d.dataset.d;
  if(dir==='L')moveL(-1);if(dir==='R')moveL(1);
  if(dir==='U')doJump();if(dir==='D')doSlide();
},{passive:false});
document.getElementById('touchPad').addEventListener('mousedown',e=>{
  const d=e.target.closest('.tbtn');
  if(!d||state!=='playing')return;
  const dir=d.dataset.d;
  if(dir==='L')moveL(-1);if(dir==='R')moveL(1);
  if(dir==='U')doJump();if(dir==='D')doSlide();
});

function startGame(){
  player=mkPlayer();obs=[];coins=[];pups=[];parts=[];
  score=0;runC=0;dist=0;spd=5.5;combo=0;gTime=0;frame=0;
  pu={mag:0,jmp:0,x2:0,shd:0};inv=50;
  state='playing';
  hideAll();
  document.getElementById('hud').style.display='flex';
  document.getElementById('pauseBtn').style.display='flex';
  document.getElementById('purow').style.display='flex';
  updHud();
  cancelAnimationFrame(raf);
  raf=requestAnimationFrame(loop);
}
function doPause(){
  if(state==='playing'){state='paused';document.getElementById('pause').classList.remove('hidden');}
}
function doResume(){
  if(state==='paused'){state='playing';document.getElementById('pause').classList.add('hidden');raf=requestAnimationFrame(loop);}
}
function doQuit(){
  state='menu';document.getElementById('pause').classList.add('hidden');
  document.getElementById('hud').style.display='none';
  document.getElementById('pauseBtn').style.display='none';
  document.getElementById('purow').style.display='none';
  show('menu');updMenu();
}
function gameOver(){
  state='over';
  const sc=Math.floor(score);
  if(sc>S.high)S.high=sc;
  S.coins+=runC;
  S.miss.forEach(m=>{
    if(m.ty==='c')m.p=Math.min(m.t,m.p+runC);
    if(m.ty==='s')m.p=Math.max(m.p,sc);
    if(m.ty==='t')m.p=Math.max(m.p,Math.floor(gTime));
    if(m.ty==='rc')m.p=Math.max(m.p,runC);
    if(m.p>=m.t&&!m.claimed){S.coins+=m.r;m.claimed=true;}
  });
  save();
  document.getElementById('fScore').textContent=sc;
  document.getElementById('fCoin').textContent=runC;
  document.getElementById('fHigh').textContent=S.high;
  document.getElementById('hud').style.display='none';
  document.getElementById('pauseBtn').style.display='none';
  document.getElementById('purow').style.display='none';
  document.getElementById('over').classList.remove('hidden');
  if(S.vib&&navigator.vibrate)navigator.vibrate([60,30,60]);
}

function update(){
  if(state!=='playing')return;
  frame++;
  gTime+=1/60;
  dist+=spd;
  score+=(spd*0.12)*(pu.x2>0?2:1);
  if(frame%280===0)spd=Math.min(spd+0.3,14);

  player.x+=(player.tx-player.x)*0.28;
  player.af=(player.af+0.28)%6.28;
  if(player.jp){
    player.jv+=0.68;
    player.jy+=player.jv;
    if(player.jy>=0){player.jy=0;player.jp=false;player.jv=0;}
  }
  if(player.sl){player.st--;if(player.st<=0)player.sl=false;}

  if(frame%Math.max(22,48-Math.floor(spd*1.8))===0)spObs();
  if(frame%16===0)spCoin();
  spPup();

  for(let i=obs.length-1;i>=0;i--){
    const o=obs[i];
    o.y+=spd;
    if(o.y>H+60){obs.splice(i,1);continue;}
    if(inv>0)continue;
    const px=player.x,py=player.y+player.jy;
    const ph=player.sl?player.h*0.42:player.h;
    const pyA=player.sl?py+player.h*0.55:py;
    if(Math.abs(px-o.x)<(player.w+o.w)*0.38 && pyA<o.y+o.h && pyA+ph>o.y){
      let hit=true;
      if(o.type==='low'&&player.jp&&player.jy<-18)hit=false;
      if((o.type==='bar'||o.type==='train')&&player.sl)hit=false;
      if(hit){
        if(pu.shd>0){pu.shd=0;inv=80;burst(px,py,'#00e89a');}
        else{gameOver();return;}
      }
    }
  }

  for(let i=coins.length-1;i>=0;i--){
    const c=coins[i];
    c.y+=spd;
    if(pu.mag>0){
      const dx=player.x-c.x,dy=(player.y+player.jy)-c.y;
      const d=Math.sqrt(dx*dx+dy*dy);
      if(d<160){c.x+=dx*0.14;c.y+=dy*0.14;}
    }
    if(c.y>H+20){coins.splice(i,1);continue;}
    if(Math.abs(player.x-c.x)<28&&Math.abs(player.y+player.jy-c.y)<36){
      coins.splice(i,1);runC++;combo++;lastC=frame;
      score+=10*(pu.x2>0?2:1)*Math.min(combo,5);
      burst(c.x,c.y,'#ffd000');
    }
  }
  if(frame-lastC>35)combo=0;

  for(let i=pups.length-1;i>=0;i--){
    const p=pups[i];
    p.y+=spd;
    if(p.y>H+20){pups.splice(i,1);continue;}
    if(Math.abs(player.x-p.x)<32&&Math.abs(player.y+player.jy-p.y)<36){
      pups.splice(i,1);
      if(p.type==='mag')pu.mag=280;
      if(p.type==='jmp')pu.jmp=230;
      if(p.type==='x2')pu.x2=260;
      if(p.type==='shd')pu.shd=180;
      burst(p.x,p.y,'#00e89a');
    }
  }

  if(inv>0)inv--;
  for(const k in pu)if(pu[k]>0)pu[k]--;

  for(let i=parts.length-1;i>=0;i--){
    const p=parts[i];p.x+=p.vx;p.y+=p.vy;p.life--;
    if(p.life<=0)parts.splice(i,1);
  }
  if(parts.length>40)parts.length=40;

  updHud();
  document.getElementById('pMag').classList.toggle('on',pu.mag>0);
  document.getElementById('pJmp').classList.toggle('on',pu.jmp>0);
  document.getElementById('pX2').classList.toggle('on',pu.x2>0);
  document.getElementById('pShd').classList.toggle('on',pu.shd>0);
}

function burst(x,y,col){
  for(let i=0;i<6;i++){
    parts.push({x,y,vx:(Math.random()-.5)*5,vy:(Math.random()-.5)*5-1.5,life:14+Math.random()*10,col,sz:2+Math.random()*3});
  }
}

function draw(){
  const g=ctx.createLinearGradient(0,0,0,H);
  g.addColorStop(0,'#0e0630');
  g.addColorStop(0.35,'#0a1540');
  g.addColorStop(1,'#061820');
  ctx.fillStyle=g;
  ctx.fillRect(0,0,W,H);

  ctx.fillStyle='rgba(255,255,255,0.5)';
  for(let i=0;i<12;i++){
    const sx=(i*97+30)%W, sy=(i*53+20)%(H*0.3);
    ctx.fillRect(sx,sy,2,2);
  }

  const off=(dist*0.25)%90;
  for(let i=-1;i<6;i++){
    const bx=i*75-off;
    const bh=BLD[(i+10)%BLD.length];
    const by=H*0.38-bh;
    ctx.fillStyle='#0c0c28';
    ctx.fillRect(bx,by,62,bh);
    ctx.fillStyle='#080820';
    ctx.fillRect(bx+50,by,12,bh);
    ctx.fillStyle='#1a4060';
    for(let wy=8;wy<bh-10;wy+=13){
      for(let wx=6;wx<48;wx+=11){
        if(((wx+wy+i*3)&3)!==0)ctx.fillRect(bx+wx,by+wy,7,8);
      }
    }
  }

  ctx.fillStyle='#12121a';
  ctx.fillRect(0,H*0.52,W,H*0.48);

  const ro=(dist*1.15)%36;
  ctx.strokeStyle='#666';
  ctx.lineWidth=3.5;
  for(let l=0;l<3;l++){
    const lx=LANES[l];
    ctx.beginPath();ctx.moveTo(lx-26,H*0.52);ctx.lineTo(lx-26,H);ctx.stroke();
    ctx.beginPath();ctx.moveTo(lx+26,H*0.52);ctx.lineTo(lx+26,H);ctx.stroke();
  }
  ctx.fillStyle='#3d2a14';
  for(let y=H*0.52-ro;y<H;y+=36){
    for(let l=0;l<3;l++)ctx.fillRect(LANES[l]-30,y,60,9);
  }
  ctx.strokeStyle='rgba(255,220,0,0.22)';
  ctx.lineWidth=2;
  ctx.setLineDash([12,14]);
  ctx.beginPath();ctx.moveTo((LANES[0]+LANES[1])/2,H*0.52);ctx.lineTo((LANES[0]+LANES[1])/2,H);ctx.stroke();
  ctx.beginPath();ctx.moveTo((LANES[1]+LANES[2])/2,H*0.52);ctx.lineTo((LANES[1]+LANES[2])/2,H);ctx.stroke();
  ctx.setLineDash([]);

  for(const c of coins)drawCoin(c);
  for(const p of pups)drawPup(p);
  for(const o of obs)drawObs(o);
  if(state==='playing'||state==='paused')drawPlayer();

  for(const p of parts){
    ctx.globalAlpha=p.life/24;
    ctx.fillStyle=p.col;
    ctx.beginPath();ctx.arc(p.x,p.y,p.sz,0,6.28);ctx.fill();
  }
  ctx.globalAlpha=1;
}

function drawPlayer(){
  const sk=SKINS[S.skin]||SKINS[0];
  const px=player.x|0;
  const baseY=player.y|0;
  const jy=player.jy|0;
  const py=baseY+jy;
  const ph=player.sl?player.h*0.48:player.h;
  const pyd=player.sl?py+player.h*0.5:py;

  ctx.save();
  if(inv>0&&(frame&4))ctx.globalAlpha=0.45;

  ctx.fillStyle='rgba(0,0,0,0.35)';
  ctx.beginPath();ctx.ellipse(px,baseY+player.h+4,18,7,0,0,6.28);ctx.fill();

  ctx.fillStyle=sk.body;
  rr(px-player.w/2,pyd,player.w,ph,7);

  if(!player.sl){
    ctx.fillStyle=sk.skin;
    ctx.beginPath();ctx.arc(px,pyd-6,13,0,6.28);ctx.fill();
    ctx.fillStyle=sk.hair;
    ctx.beginPath();ctx.arc(px,pyd-12,11,3.14,0);ctx.fill();
    ctx.fillStyle='#1a1a1a';
    ctx.beginPath();ctx.arc(px-4.5,pyd-7,2.2,0,6.28);ctx.arc(px+4.5,pyd-7,2.2,0,6.28);ctx.fill();
    ctx.strokeStyle='#c07050';ctx.lineWidth=1.5;
    ctx.beginPath();ctx.arc(px,pyd-3,4,0.2,2.9);ctx.stroke();
  }

  if(!player.sl&&!player.jp){
    const lo=Math.sin(player.af)*7;
    ctx.fillStyle='#1a1a2a';
    ctx.fillRect(px-11,pyd+ph-4,7,11+lo);
    ctx.fillRect(px+4,pyd+ph-4,7,11-lo);
  }

  if(pu.shd>0){
    ctx.strokeStyle='rgba(0,232,154,0.65)';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.arc(px,pyd+ph/2,30,0,6.28);ctx.stroke();
  }
  ctx.restore();
}

function drawObs(o){
  const x=o.x|0,y=o.y|0;
  if(o.type==='train'){
    ctx.fillStyle='#c41e1e';
    rr(x-o.w/2,y,o.w,o.h,5);
    ctx.fillStyle='#8b0000';
    ctx.fillRect(x-o.w/2-2,y-6,o.w+4,8);
    ctx.fillStyle='#7ec8ff';
    ctx.fillRect(x-o.w/2+7,y+12,o.w-14,22);
    ctx.fillStyle='#ffd000';
    ctx.fillRect(x-o.w/2,y+o.h-28,o.w,6);
    ctx.fillStyle='#ffff66';
    ctx.beginPath();ctx.arc(x-10,y+o.h-12,4.5,0,6.28);ctx.arc(x+10,y+o.h-12,4.5,0,6.28);ctx.fill();
  }else if(o.type==='bar'){
    ctx.fillStyle='#ff5a00';
    rr(x-o.w/2,y,o.w,o.h,4);
    ctx.fillStyle='#fff';
    for(let i=0;i<4;i++)ctx.fillRect(x-o.w/2+5,y+10+i*14,o.w-10,5);
  }else if(o.type==='low'){
    ctx.fillStyle='#e62020';
    rr(x-o.w/2,y,o.w,o.h,3);
    ctx.fillStyle='#fff';
    for(let i=0;i<3;i++)ctx.fillRect(x-o.w/2+5+i*14,y+6,8,o.h-12);
  }else{
    ctx.fillStyle='#8B5A2B';
    rr(x-o.w/2,y,o.w,o.h,4);
    ctx.strokeStyle='#5a3a1a';ctx.lineWidth=2;
    ctx.strokeRect(x-o.w/2+3,y+3,o.w-6,o.h-6);
    ctx.beginPath();ctx.moveTo(x-o.w/2+3,y+3);ctx.lineTo(x+o.w/2-3,y+o.h-3);
    ctx.moveTo(x+o.w/2-3,y+3);ctx.lineTo(x-o.w/2+3,y+o.h-3);ctx.stroke();
  }
}

function drawCoin(c){
  const x=c.x|0,y=c.y|0;
  ctx.save();
  ctx.translate(x,y);
  ctx.fillStyle='rgba(255,208,0,0.25)';
  ctx.beginPath();ctx.arc(0,0,c.r+4,0,6.28);ctx.fill();
  ctx.fillStyle='#ffd000';
  ctx.beginPath();ctx.arc(0,0,c.r,0,6.28);ctx.fill();
  ctx.fillStyle='#e8a800';
  ctx.beginPath();ctx.arc(0,0,c.r*0.6,0,6.28);ctx.fill();
  ctx.fillStyle='#fff';
  ctx.font='bold 11px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.fillText('$',0,1);
  ctx.restore();
}

function drawPup(p){
  const icons={mag:'🧲',jmp:'👟',x2:'✖2',shd:'🛡'};
  const cols={mag:'#00a0ff',jmp:'#ff60a0',x2:'#ffd000',shd:'#00e89a'};
  const x=p.x|0,y=p.y|0;
  ctx.fillStyle=cols[p.type]||'#fff';
  ctx.beginPath();ctx.arc(x,y,p.r,0,6.28);ctx.fill();
  ctx.fillStyle='#fff';
  ctx.font='14px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.fillText(icons[p.type]||'?',x,y+1);
}

function rr(x,y,w,h,r){
  ctx.beginPath();
  ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);
  ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);
  ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
  ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);
  ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();ctx.fill();
}

function hideAll(){
  ['menu','shop','miss','set','over','pause'].forEach(id=>document.getElementById(id).classList.add('hidden'));
}
function show(id){
  hideAll();
  document.getElementById(id).classList.remove('hidden');
  if(id==='shop')renderShop();
  if(id==='miss')renderMiss();
  if(id==='set'){document.getElementById('chkSound').checked=S.sound;document.getElementById('chkVib').checked=S.vib;}
}
function updMenu(){
  document.getElementById('mHigh').textContent=S.high;
  document.getElementById('mCoin').textContent=S.coins;
}
function updHud(){
  document.getElementById('hScore').textContent=Math.floor(score);
  document.getElementById('hCoin').textContent=runC;
  document.getElementById('hHigh').textContent=Math.max(S.high,Math.floor(score));
}

function renderShop(){
  document.getElementById('sCoin').textContent=S.coins;
  const list=document.getElementById('shopList');
  list.innerHTML='';
  SKINS.forEach(sk=>{
    const owned=S.unlocked.includes(sk.id);
    const cur=S.skin===sk.id;
    const d=document.createElement('div');
    d.className='item'+(owned?' own':'');
    d.innerHTML='<div><div style="font-weight:700">'+sk.n+'</div><div style="font-size:.82rem;color:#99a">'+(owned?(cur?'✓ Equipped':'Owned'):'Locked')+'</div></div><div>'+(owned?(cur?'<span style="color:#00e89a">Equipped</span>':'<button class="btn sm" style="padding:5px 12px;min-width:auto" data-eq="'+sk.id+'">Equip</button>'):'<span class="price">🪙 '+sk.pr+'</span> <button class="btn sm" style="padding:5px 12px;min-width:auto;margin-left:6px" data-buy="'+sk.id+'">Buy</button>')+'</div>';
    list.appendChild(d);
  });
  list.querySelectorAll('[data-buy]').forEach(b=>b.onclick=function(){
    const id=+this.dataset.buy;const sk=SKINS.find(s=>s.id===id);
    if(!sk||S.unlocked.includes(id))return;
    if(S.coins>=sk.pr){S.coins-=sk.pr;S.unlocked.push(id);S.skin=id;save();renderShop();updMenu();}
    else alert('Not enough coins!');
  });
  list.querySelectorAll('[data-eq]').forEach(b=>b.onclick=function(){
    const id=+this.dataset.eq;if(S.unlocked.includes(id)){S.skin=id;save();renderShop();}
  });
}
function renderMiss(){
  const list=document.getElementById('missList');
  list.innerHTML='';
  S.miss.forEach(m=>{
    const pct=Math.min(100,(m.p/m.t)*100);
    const d=document.createElement('div');
    d.className='item';d.style.flexDirection='column';d.style.alignItems='flex-start';d.style.gap='4px';
    d.innerHTML='<div style="width:100%;display:flex;justify-content:space-between"><span style="font-weight:600">'+m.n+'</span><span class="price">🪙 '+m.r+'</span></div><div style="font-size:.82rem;color:#99a">'+Math.min(m.p,m.t)+' / '+m.t+(m.p>=m.t?(m.claimed?' ✓':' ✓ Done!'):'')+'</div><div style="width:100%;height:7px;background:#333;border-radius:4px;overflow:hidden"><div style="height:100%;width:'+pct+'%;background:linear-gradient(90deg,#00e89a,#00c8ff)"></div></div>';
    list.appendChild(d);
  });
}

document.getElementById('btnPlay').onclick=startGame;
document.getElementById('btnShop').onclick=function(){show('shop');};
document.getElementById('btnMiss').onclick=function(){show('miss');};
document.getElementById('btnSet').onclick=function(){show('set');};
document.getElementById('btnBackShop').onclick=function(){show('menu');};
document.getElementById('btnBackMiss').onclick=function(){show('menu');};
document.getElementById('btnBackSet').onclick=function(){S.sound=document.getElementById('chkSound').checked;S.vib=document.getElementById('chkVib').checked;save();show('menu');};
document.getElementById('btnRetry').onclick=startGame;
document.getElementById('btnMenu').onclick=function(){show('menu');updMenu();};
document.getElementById('btnResume').onclick=doResume;
document.getElementById('btnQuit').onclick=doQuit;
document.getElementById('pauseBtn').onclick=doPause;

function loop(){
  if(state==='playing'){
    update();
    draw();
    raf=requestAnimationFrame(loop);
  }else if(state==='paused'){
    draw();
  }
}

function resize(){
  const ww=window.innerWidth,hh=window.innerHeight;
  const ratio=W/H;
  let cw=ww,ch=ww/ratio;
  if(ch>hh){ch=hh;cw=ch*ratio;}
  canvas.style.width=cw+'px';
  canvas.style.height=ch+'px';
}
window.addEventListener('resize',resize);
window.addEventListener('orientationchange',function(){setTimeout(resize,100);});
resize();

updMenu();
show('menu');
draw();
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=800, scrolling=False)
