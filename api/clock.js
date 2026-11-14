import fs from 'fs';
import path from 'path';

// Cache the base64 background image in memory so subsequent requests respond in under 5ms
let cachedDataUri = null;

function getBackgroundDataUri() {
  if (cachedDataUri) return cachedDataUri;
  try {
    const imgPath = path.join(process.cwd(), 'night-room.png');
    if (fs.existsSync(imgPath)) {
      const buffer = fs.readFileSync(imgPath);
      cachedDataUri = `data:image/png;base64,${buffer.toString('base64')}`;
      return cachedDataUri;
    }
  } catch (err) {
    // fallback to GitHub raw URL if file read fails
  }
  return 'https://raw.githubusercontent.com/DiptarkaSamanta/DiptarkaSamanta/main/night-room.png';
}

export default function handler(req, res) {
  const now = new Date();

  // Format explicitly to Indian Standard Time (IST)
  const timeFormatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Kolkata',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  });

  const dateFormatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Kolkata',
    weekday: 'short',
    month: 'short',
    day: '2-digit',
    year: 'numeric'
  });

  const parts = timeFormatter.formatToParts(now);
  const hour = parts.find(p => p.type === 'hour').value;
  const minute = parts.find(p => p.type === 'minute').value;
  const second = parts.find(p => p.type === 'second').value;
  const dayPeriod = parts.find(p => p.type === 'dayPeriod').value;
  const dateStr = dateFormatter.format(now);

  const curSec = parseInt(second, 10);
  const curMin = parseInt(minute, 10);
  const curHour12 = parseInt(hour, 10);

  // Generate real-time ticking animations starting from the exact request second
  const secCss = [];
  const secTags = [];
  for (let s = 0; s < 60; s++) {
    const timeSinceS = (curSec - s + 60) % 60;
    const delay = -timeSinceS;
    secCss.push(`.s-${String(s).padStart(2, '0')} { animation: secShow 60s steps(1) infinite ${delay}s; }`);
    secTags.push(`<text class="digital-time anim-digit s-${String(s).padStart(2, '0')}" x="162.0" y="24" text-anchor="middle">${String(s).padStart(2, '0')}</text>`);
  }

  const elapsedInHour = curMin * 60 + curSec;
  const minCss = [];
  const minTags = [];
  for (let m = 0; m < 60; m++) {
    const timeSinceM = (elapsedInHour - m * 60 + 3600) % 3600;
    const delay = -timeSinceM;
    minCss.push(`.m-${String(m).padStart(2, '0')} { animation: minShow 3600s steps(1) infinite ${delay}s; }`);
    minTags.push(`<text class="digital-time anim-digit m-${String(m).padStart(2, '0')}" x="102.0" y="24" text-anchor="middle">${String(m).padStart(2, '0')}</text>`);
  }

  const imgUri = getBackgroundDataUri();

  const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1536 1024" width="100%" height="100%">
  <defs>
    <style>
      .digital-time {
        font-family: 'Courier New', Consolas, Monaco, 'Lucida Console', monospace;
        font-size: 21px;
        font-weight: 700;
        fill: #ffc266;
        letter-spacing: 0.8px;
        filter: drop-shadow(0px 0px 6px rgba(255, 170, 40, 0.85));
      }
      .digital-date {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 12px;
        font-weight: 600;
        fill: #ffe0b2;
        letter-spacing: 0.6px;
        opacity: 0.95;
        filter: drop-shadow(0px 0px 4px rgba(255, 180, 70, 0.6));
      }

      .blink-colon {
        animation: blinkColon 1s steps(1) infinite;
      }
      @keyframes blinkColon {
        0%, 49% { opacity: 1; }
        50%, 100% { opacity: 0.25; }
      }

      .anim-digit {
        opacity: 0;
      }
      @keyframes secShow {
        0%, 1.6666% { opacity: 1; }
        1.6667%, 100% { opacity: 0; }
      }
      @keyframes minShow {
        0%, 1.6666% { opacity: 1; }
        1.6667%, 100% { opacity: 0; }
      }

      ${minCss.join('\n      ')}

      ${secCss.join('\n      ')}

      .wind-stream {
        animation: windDrift 7s linear infinite;
        opacity: 0.35;
      }
      .wind-2 {
        animation: windDrift 9s linear infinite 3s;
        opacity: 0.25;
      }
      @keyframes windDrift {
        0% { transform: translateX(-300px); }
        100% { transform: translateX(1600px); }
      }

      .clock-screen-box {
        fill: #0a0705;
        fill-opacity: 0.92;
        stroke: rgba(255, 170, 50, 0.45);
        stroke-width: 1.5;
        rx: 7px;
        filter: drop-shadow(0 4px 14px rgba(0,0,0,0.85));
      }

      .clock-screen-inner {
        fill: none;
        stroke: rgba(255, 190, 70, 0.15);
        stroke-width: 0.8;
        rx: 5.5px;
      }
    </style>

    <linearGradient id="windGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="transparent"/>
      <stop offset="50%" stop-color="#d2e6ff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="transparent"/>
    </linearGradient>
  </defs>

  <image href="${imgUri}" x="0" y="0" width="1536" height="1024" preserveAspectRatio="xMidYMid slice"/>

  <g pointer-events="none">
    <rect class="wind-stream" x="0" y="240" width="350" height="3" fill="url(#windGrad)"/>
    <rect class="wind-stream wind-2" x="0" y="320" width="280" height="2" fill="url(#windGrad)"/>
  </g>

  <g transform="translate(830, 141)">
    <rect class="clock-screen-box" x="0" y="0" width="240" height="48" rx="7"/>
    <rect class="clock-screen-inner" x="1.5" y="1.5" width="237" height="45" rx="5.5"/>

    <text class="digital-time" x="42.0" y="24" text-anchor="middle">${hour}</text>
    <text class="digital-time blink-colon" x="72.0" y="24" text-anchor="middle">:</text>
    ${minTags.join('\n    ')}
    <text class="digital-time blink-colon" x="132.0" y="24" text-anchor="middle">:</text>
    ${secTags.join('\n    ')}
    <text class="digital-time" x="198.0" y="24" text-anchor="middle">${dayPeriod}</text>
    <text class="digital-date" x="120.0" y="38" text-anchor="middle">${dateStr} (IST)</text>
  </g>
</svg>`;

  res.setHeader('Content-Type', 'image/svg+xml');
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0, s-maxage=0');
  res.status(200).send(svgContent);
}

