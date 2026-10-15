"""
Flappy Bird - Streamlit + HTML5 Canvas (components.html)

Chạy:  pip install streamlit
       streamlit run flappy_bird.py

Điều khiển: Space / Mũi tên lên (máy tính) hoặc chạm vào canvas (điện thoại).
Chọn độ khó: bấm nút DỄ / THƯỜNG / KHÓ (hoặc phím 1 / 2 / 3).
"""
import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  html,body{margin:0;background:transparent;display:flex;justify-content:center;touch-action:none;
    user-select:none;-webkit-user-select:none;-webkit-tap-highlight-color:transparent;overscroll-behavior:none}
  canvas{width:100%;max-width:347px;aspect-ratio:2/3;height:auto;border-radius:16px;
    box-shadow:0 8px 24px rgba(0,0,0,.35);outline:none;cursor:pointer}
</style></head>
<body>
<canvas id="c" tabindex="0"></canvas>
<script>
const W=320,H=480,GH=64,R=12,PW=56,INK='#533846';
const FONT='"Trebuchet MS",system-ui,sans-serif';
const BTN={x:70,y:300,w:180,h:56},SELY=244,SELH=36;
/* Độ khó: gap = khe hở, sp = tốc độ ống, g = trọng lực, f = lực vỗ cánh,
   sx = khoảng cách giữa các ống, mv = ống di chuyển lên xuống */
const LV={
  easy:  {n:'DỄ',     gap:152,sp:105,g:1300,f:-380,sx:[190,245],mv:0},
  normal:{n:'THƯỜNG', gap:126,sp:128,g:1500,f:-400,sx:[170,225],mv:0},
  hard:  {n:'KHÓ',    gap:106,sp:158,g:1650,f:-415,sx:[150,200],mv:1}
};
const SEL=[{k:'easy',x:14,w:94,c:'#4caf50'},{k:'normal',x:113,w:94,c:'#f0a030'},{k:'hard',x:212,w:94,c:'#e0453a'}];
const C=document.getElementById('c'),X=C.getContext('2d'),D=Math.min(2,window.devicePixelRatio||1);
C.width=W*D;C.height=H*D;
const rnd=(a,b)=>a+Math.random()*(b-a);
const rgb=a=>'rgb('+(a[0]|0)+','+(a[1]|0)+','+(a[2]|0)+')';

let diff='normal',best={easy:0,normal:0,hard:0};
try{const d=localStorage.getItem('fb_diff');if(LV[d])diff=d;Object.assign(best,JSON.parse(localStorage.getItem('fb_best')||'{}'))}catch(e){}
const save=()=>{try{localStorage.setItem('fb_diff',diff);localStorage.setItem('fb_best',JSON.stringify(best))}catch(e){}};

let st='ready',bird,pipes,score,nextSpace,dist=0,clock=0,overAt=0,shake=0,flash=0,bump=0,newBest=false;
const parts=[],clouds=[],stars=[],bld=[];
for(let i=0;i<5;i++)clouds.push({x:rnd(0,W),y:rnd(40,190),s:rnd(.7,1.2)});
for(let i=0;i<45;i++)stars.push({x:rnd(0,W),y:rnd(0,240),r:rnd(1,2.2),p:rnd(0,6)});
(function(){let x=0,i=0;while(x<400){const w=rnd(26,44),h=rnd(45,115);bld.push({x,w,h,i:i++});x+=w+rnd(0,5)}bld.total=x})();

/* Bảng màu bầu trời: ngày -> hoàng hôn -> đêm (đổi mỗi 12 điểm) */
const PAL=[[[78,192,202],[205,242,245]],[[255,140,100],[255,226,160]],[[24,34,84],[74,95,160]]];
let skyCur=JSON.parse(JSON.stringify(PAL[0])),night=0;
function skyUpdate(dt){
  const idx=Math.floor(score/12)%3,tg=PAL[idx],k=Math.min(1,dt*1.5);
  for(let i=0;i<2;i++)for(let j=0;j<3;j++)skyCur[i][j]+=(tg[i][j]-skyCur[i][j])*k;
  night+=((idx===2?1:0)-night)*k;
}

function reset(){bird={x:90,y:175,v:0,rot:0};pipes=[];score=0;nextSpace=0;newBest=false;parts.length=0}
reset();

/* ---------- hiệu ứng hạt ---------- */
function puff(){for(let i=0;i<4;i++)parts.push({x:bird.x-12,y:bird.y+5,vx:rnd(-70,-20),vy:rnd(10,70),g:0,r:rnd(2.5,5),col:'#fff',life:.45,max:.45})}
function burst(){for(let i=0;i<22;i++)parts.push({x:bird.x,y:bird.y,vx:rnd(-220,220),vy:rnd(-260,60),g:700,r:rnd(2,5),col:['#ffe85a','#fff','#ff9a3d'][i%3],life:.8,max:.8})}

/* ---------- điều khiển ---------- */
function flap(){bird.v=LV[diff].f;puff()}
function startGame(){reset();st='play';flap()}
function gameOver(){
  st='over';overAt=clock;shake=.4;flash=1;burst();
  if(score>best[diff]){best[diff]=score;newBest=true;save()}
}
const inBtn=(x,y)=>x>=BTN.x&&x<=BTN.x+BTN.w&&y>=BTN.y&&y<=BTN.y+BTN.h;
const selHit=(x,y)=>{if(y<SELY||y>SELY+SELH)return null;for(const s of SEL)if(x>=s.x&&x<=s.x+s.w)return s.k;return null};
const canPick=()=>st==='ready'||(st==='over'&&clock-overAt>.45);
function act(px,py){
  const key=px==null;
  if(st==='play'){flap();return}
  if(!canPick())return;
  if(!key){const k=selHit(px,py);if(k){diff=k;save();return}}
  if(key||inBtn(px,py))startGame();
}
C.addEventListener('pointerdown',e=>{
  e.preventDefault();C.focus();
  const r=C.getBoundingClientRect();
  act((e.clientX-r.left)*W/r.width,(e.clientY-r.top)*H/r.height);
});
addEventListener('keydown',e=>{
  if(e.code==='Space'||e.code==='ArrowUp'){e.preventDefault();if(!e.repeat)act(null)}
  const m={Digit1:'easy',Digit2:'normal',Digit3:'hard',Numpad1:'easy',Numpad2:'normal',Numpad3:'hard'}[e.code];
  if(m&&canPick()){diff=m;save()}
});
C.addEventListener('contextmenu',e=>e.preventDefault());

/* ---------- logic ---------- */
function circleRect(cx,cy,r,rx,ry,rw,rh){
  const nx=Math.max(rx,Math.min(cx,rx+rw)),ny=Math.max(ry,Math.min(cy,ry+rh));
  return (cx-nx)**2+(cy-ny)**2<r*r;
}
function update(dt){
  const L=LV[diff];
  skyUpdate(dt);
  clouds.forEach(c=>{c.x-=8*c.s*dt;if(c.x<-70)c.x=W+40});
  shake=Math.max(0,shake-dt);flash=Math.max(0,flash-dt*3);bump=Math.max(0,bump-dt*4);
  for(let i=parts.length-1;i>=0;i--){const p=parts[i];p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=p.g*dt;p.life-=dt;if(p.life<=0)parts.splice(i,1)}
  if(st==='ready'){bird.y=175+Math.sin(clock*4)*8;dist+=L.sp*dt;return}
  if(st==='over'){
    if(bird.y+R<H-GH){bird.v+=1500*dt;bird.y=Math.min(H-GH-R,bird.y+bird.v*dt);bird.rot=Math.min(1.5,bird.rot+7*dt)}
    return;
  }
  dist+=L.sp*dt;
  bird.v+=L.g*dt;bird.y+=bird.v*dt;
  bird.rot=Math.max(-.45,Math.min(1.3,bird.v/520));
  const last=pipes[pipes.length-1];
  if(!last||last.x<W-nextSpace){
    const amp=L.mv?rnd(14,32):0,lo=44+amp,hi=H-GH-L.gap-44-amp;
    pipes.push({x:W+10,base:rnd(lo,hi),amp,ph:rnd(0,6.28),top:0,passed:false});
    nextSpace=rnd(L.sx[0],L.sx[1]);
  }
  for(const p of pipes){
    p.x-=L.sp*dt;
    p.top=p.base+Math.sin(clock*1.7+p.ph)*p.amp;
    if(!p.passed&&p.x+PW<bird.x-R){p.passed=true;score++;bump=1}
    if(circleRect(bird.x,bird.y,R,p.x,0,PW,p.top)||circleRect(bird.x,bird.y,R,p.x,p.top+L.gap,PW,H))return gameOver();
  }
  pipes=pipes.filter(p=>p.x>-PW-10);
  if(bird.y+R>=H-GH){bird.y=H-GH-R;return gameOver()}
  if(bird.y-R<0)return gameOver();
}

/* ---------- vẽ: tiện ích ---------- */
function rr(x,y,w,h,r,f,s){X.beginPath();X.moveTo(x+r,y);X.arcTo(x+w,y,x+w,y+h,r);X.arcTo(x+w,y+h,x,y+h,r);X.arcTo(x,y+h,x,y,r);X.arcTo(x,y,x+w,y,r);X.closePath();if(f){X.fillStyle=f;X.fill()}if(s){X.strokeStyle=s;X.lineWidth=3;X.stroke()}}
function ci(x,y,r,f,s,lw){X.beginPath();X.arc(x,y,r,0,7);if(f){X.fillStyle=f;X.fill()}if(s){X.strokeStyle=s;X.lineWidth=lw||2;X.stroke()}}
function tx(s,x,y,z,col,stroke){
  X.font='800 '+z+'px '+FONT;X.textAlign='center';X.textBaseline='middle';
  if(stroke){X.lineWidth=Math.max(4,z/7);X.lineJoin='round';X.strokeStyle=INK;X.strokeText(s,x,y)}
  X.fillStyle=col;X.fillText(s,x,y);
}

/* ---------- vẽ: bối cảnh ---------- */
function hills(off,amp,y,col,k){
  X.fillStyle=col;X.beginPath();X.moveTo(0,H-GH);
  for(let x=0;x<=W;x+=8)X.lineTo(x,y+Math.sin((x+off)/k)*amp);
  X.lineTo(W,H-GH);X.closePath();X.fill();
}
function skyline(){
  const base=H-GH-8,off=(dist*.22)%bld.total;
  for(let rep=0;rep<2;rep++)bld.forEach(b=>{
    const bx=b.x-off+rep*bld.total;if(bx>W||bx+b.w<0)return;
    X.fillStyle='#9cc7d6';X.fillRect(bx,base-b.h,b.w,b.h);
    X.fillStyle='#b9dfeb';X.fillRect(bx,base-b.h,b.w,4);
    X.fillStyle='#86b3c4';X.fillRect(bx+b.w-5,base-b.h+4,5,b.h-4);
    for(let r=0;r<Math.floor((b.h-12)/12);r++)for(let c=0;c<Math.floor((b.w-8)/9);c++){
      const lit=((b.i*7+r*3+c*5)%4)<2;
      X.fillStyle=lit?'rgba(255,230,120,'+(.25+night*.75)+')':'rgba(120,160,180,.45)';
      X.fillRect(bx+5+c*9,base-b.h+8+r*12,5,7);
    }
  });
}
function sky(){
  const g=X.createLinearGradient(0,0,0,H-GH);g.addColorStop(0,rgb(skyCur[0]));g.addColorStop(1,rgb(skyCur[1]));
  X.fillStyle=g;X.fillRect(0,0,W,H);
  stars.forEach(s=>{X.globalAlpha=night*(.5+.5*Math.sin(clock*2+s.p));X.fillStyle='#fff';X.fillRect(s.x,s.y,s.r,s.r)});
  X.globalAlpha=1-night;
  const sg=X.createRadialGradient(245,85,8,245,85,75);sg.addColorStop(0,'rgba(255,250,200,.7)');sg.addColorStop(1,'rgba(255,250,200,0)');
  X.fillStyle=sg;X.fillRect(170,10,150,150);ci(245,85,24,'#fff6b0');
  X.globalAlpha=night;ci(245,85,21,'#f4f1c8');ci(238,79,4,'#dcd9a8');ci(251,91,5,'#dcd9a8');ci(252,76,2.5,'#dcd9a8');
  X.globalAlpha=1;
  clouds.forEach(c=>{const f='rgba(255,255,255,'+(.9-night*.55)+')';
    for(const [dx,dy,r] of [[0,0,16],[18,-7,21],[40,0,16],[20,6,17]])ci(c.x+dx*c.s,c.y+dy*c.s,r*c.s,f)});
  hills(dist*.1,14,H-GH-72,'#a8dca6',48);
  skyline();
  hills(dist*.3,8,H-GH-22,'#7ccb7a',34);
  const bo=(dist*.5)%46;
  for(let i=-1;i<9;i++)ci(i*46-bo,H-GH+2,18+(i%3)*4,'#5fb85a');
  X.fillStyle='rgba(8,12,45,'+(night*.4)+')';X.fillRect(0,0,W,H-GH);
}
function mkGrad(w){
  const g=X.createLinearGradient(0,0,w,0);
  [[0,'#4f8f1a'],[.15,'#9be15a'],[.4,'#73bf2e'],[.8,'#5a9e22'],[1,'#3f7416']].forEach(s=>g.addColorStop(s[0],s[1]));
  return g;
}
const pg=mkGrad(PW),cg=mkGrad(PW+8);
function pipe(x,top,gap){
  X.strokeStyle=INK;X.lineWidth=3;
  const part=(y,h,cy)=>{
    X.save();X.translate(x,0);X.fillStyle=pg;X.fillRect(0,y,PW,h);X.strokeRect(0,y,PW,h);X.restore();
    X.save();X.translate(x-4,0);X.fillStyle=cg;X.fillRect(0,cy,PW+8,24);X.strokeRect(0,cy,PW+8,24);
    X.fillStyle='rgba(255,255,255,.2)';X.fillRect(4,cy+3,PW,4);X.restore();
  };
  part(-4,top+4,top-24);part(top+gap,H,top+gap);
}
function ground(){
  const o=dist%24;
  X.fillStyle='#ded895';X.fillRect(0,H-GH,W,GH);
  X.fillStyle='#d2c97c';for(let y=H-GH+28;y<H;y+=14)X.fillRect(0,y,W,2);
  X.fillStyle='#73bf2e';X.fillRect(0,H-GH,W,14);
  X.fillStyle='#5a9e22';
  for(let x=-24;x<W+24;x+=24){X.beginPath();X.moveTo(x-o,H-GH+14);X.lineTo(x-o+12,H-GH+14);X.lineTo(x-o+20,H-GH);X.lineTo(x-o+8,H-GH);X.fill()}
  X.fillStyle='#9be15a';X.fillRect(0,H-GH,W,3);
  X.fillStyle=INK;X.fillRect(0,H-GH-1,W,3);
  X.fillStyle='rgba(8,12,45,'+(night*.35)+')';X.fillRect(0,H-GH,W,GH);
}

/* ---------- vẽ: chim ---------- */
function drawBird(){
  X.save();X.translate(bird.x,bird.y);X.rotate(bird.rot);
  X.strokeStyle=INK;X.lineWidth=3;X.lineJoin='round';
  X.fillStyle='#f0a41c';X.beginPath();X.moveTo(-14,-2);X.lineTo(-26,-8);X.lineTo(-23,0);X.lineTo(-26,7);X.lineTo(-14,5);X.closePath();X.fill();X.stroke();
  const g=X.createLinearGradient(0,-14,0,14);g.addColorStop(0,'#ffec6a');g.addColorStop(1,'#f5b01c');
  X.fillStyle=g;X.beginPath();X.ellipse(0,0,18,14,0,0,7);X.fill();X.stroke();
  X.fillStyle='#fff4c2';X.beginPath();X.ellipse(-2,7,11,5.5,0,0,7);X.fill();
  const w=Math.sin(clock*(st==='play'?30:12));
  X.save();X.translate(-7,2);X.rotate(-.3+w*.45);X.fillStyle='#fffbe0';X.strokeStyle=INK;X.lineWidth=2.5;
  X.beginPath();X.ellipse(0,0,10,6,0,0,7);X.fill();X.stroke();X.restore();
  ci(9,-5,6.5,'#fff',INK,2.5);
  if(st==='over'){X.strokeStyle=INK;X.lineWidth=2;X.beginPath();X.moveTo(8,-8);X.lineTo(14,-2);X.moveTo(14,-8);X.lineTo(8,-2);X.stroke()}
  else{ci(11,-5,3.2,'#222');ci(12.2,-6.2,1.1,'#fff')}
  ci(6,5,3,'rgba(255,110,110,.55)');
  rr(11,-2,14,6,3,'#ff6a3d',INK);rr(11,3,12,5,2.5,'#e04a24',INK);
  X.restore();
}

/* ---------- vẽ: giao diện ---------- */
function button(label){
  rr(BTN.x,BTN.y+5,BTN.w,BTN.h,14,'#a8501b');
  rr(BTN.x,BTN.y,BTN.w,BTN.h,14,'#f08a24',INK);
  X.fillStyle='rgba(255,255,255,.25)';X.fillRect(BTN.x+10,BTN.y+5,BTN.w-20,5);
  tx(label,BTN.x+BTN.w/2,BTN.y+BTN.h/2+2,24,'#fff',true);
}
function selector(){
  tx('ĐỘ KHÓ',W/2,SELY-14,12,'#fff',true);
  SEL.forEach(s=>{
    const on=diff===s.k;
    rr(s.x,SELY+(on?3:0),s.w,SELH,10,on?s.c:'#7d8794',on?'#fff':INK);
    tx(LV[s.k].n,s.x+s.w/2,SELY+SELH/2+(on?4:1),on?15:13,'#fff',on);
  });
}
function medalFor(s){return s>=40?'#8fe8ff':s>=30?'#ffd700':s>=20?'#c8ccd2':s>=10?'#cd7f32':null}
function draw(){
  X.setTransform(D,0,0,D,0,0);
  X.save();
  if(shake>0)X.translate(rnd(-1,1)*shake*16,rnd(-1,1)*shake*16);
  sky();
  const L=LV[diff];
  pipes.forEach(p=>pipe(p.x,p.top,L.gap));
  ground();
  parts.forEach(p=>{X.globalAlpha=Math.max(0,p.life/p.max);ci(p.x,p.y,p.r,p.col)});X.globalAlpha=1;
  drawBird();

  if(st==='play'){
    X.save();X.translate(W/2,72);const s=1+bump*.35;X.scale(s,s);tx(score,0,0,52,'#fff',true);X.restore();
    const c=SEL.find(s=>s.k===diff).c;
    rr(8,8,74,22,11,c,INK);tx(L.n,45,20,12,'#fff');
  }
  if(st==='ready'){
    tx('FLAPPY',W/2,78,40,'#ffd23f',true);tx('BIRD',W/2,116,40,'#ff7a3d',true);
    selector();button('BẮT ĐẦU');
    tx('Space / ↑ / chạm để vỗ cánh',W/2,385,14,'#fff',true);
    tx('Phím 1 · 2 · 3: chọn độ khó',W/2,406,12,'#fff',true);
  }
  if(st==='over'){
    X.fillStyle='rgba(0,0,0,.28)';X.fillRect(0,0,W,H);
    tx('GAME OVER',W/2,62,40,'#ff6b4a',true);
    rr(40,92,240,122,16,'#ded895',INK);
    const m=medalFor(score);
    if(m){ci(88,153,27,m,INK,3);ci(88,153,19,null,'rgba(255,255,255,.7)');tx('★',88,154,26,'#fff')}
    else{ci(88,153,27,'rgba(0,0,0,.12)','rgba(0,0,0,.25)');tx('?',88,154,24,'rgba(0,0,0,.3)')}
    tx('ĐIỂM',200,112,13,'#a8501b');tx(score,200,138,34,'#fff',true);
    tx('CAO NHẤT · '+L.n,200,170,11,'#a8501b');tx(best[diff],200,194,24,'#fff',true);
    if(newBest&&score>0){rr(238,180,36,18,6,'#ff4d4d',INK);tx('MỚI',256,189,10,'#fff')}
    selector();button('CHƠI LẠI');
    tx('Space: chơi lại · 1 · 2 · 3: độ khó',W/2,392,12,'#fff',true);
  }
  X.restore();
  if(flash>0){X.fillStyle='rgba(255,255,255,'+flash*.6+')';X.fillRect(0,0,W,H)}
}

let last=performance.now();
(function loop(n){const dt=Math.min(.04,(n-last)/1000);last=n;clock+=dt;update(dt);draw();requestAnimationFrame(loop)})(last);
C.focus();
</script>
</body></html>
"""

st.set_page_config(page_title="Flappy Bird", page_icon="🐤", layout="centered")
st.markdown("<h2 style='text-align:center'>🐤 Flappy Bird</h2>", unsafe_allow_html=True)
st.caption("Chọn độ khó DỄ / THƯỜNG / KHÓ rồi bấm BẮT ĐẦU. Dùng Space / ↑ hoặc chạm màn hình để vỗ cánh. "
           "Nếu phím không phản hồi, hãy bấm vào khung game một lần.")

components.html(GAME_HTML, height=540, scrolling=False)
