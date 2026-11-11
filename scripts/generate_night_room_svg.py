import datetime
import base64
import os

def generate_night_room_svg(output_path="night-room-ambience.svg", png_path="night-room.png"):
    # Current timestamp in IST (Indian Standard Time)
    try:
        import zoneinfo
        tz = zoneinfo.ZoneInfo("Asia/Kolkata")
    except Exception:
        tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now = datetime.datetime.now(tz)
    
    hour_12 = now.hour % 12 or 12
    hour_str = f"{hour_12:02d}"
    cur_min = now.minute
    cur_sec = now.second
    ampm = now.strftime("%p")
    date_str = now.strftime("%a, %b %d, %Y")

    # Read PNG image and encode to Base64 so SVG is 100% self-contained
    img_data_uri = ""
    if os.path.exists(png_path):
        with open(png_path, "rb") as img_file:
            encoded_bytes = base64.b64encode(img_file.read()).decode("utf-8")
            img_data_uri = f"data:image/png;base64,{encoded_bytes}"
    else:
        # Fallback raw github url if local file missing
        img_data_uri = "https://raw.githubusercontent.com/DiptarkaSamanta/DiptarkaSamanta/main/night-room.png"

    # Generate CSS rules and SVG elements for live seconds (60s loop)
    sec_css = []
    sec_tags = []
    for s in range(60):
        time_since_s = (cur_sec - s) % 60
        delay = -time_since_s
        sec_css.append(f".s-{s:02d} {{ animation: secShow 60s infinite {delay}s; }}")
        sec_tags.append(f'<text class="digital-time anim-digit s-{s:02d}" x="113.5" y="21" text-anchor="middle">{s:02d}</text>')

    sec_rules_str = "\n      ".join(sec_css)
    sec_tags_str = "\n    ".join(sec_tags)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1536 1024" width="100%" height="100%">
  <defs>
    <style>
      .digital-time {{
        font-family: 'Courier New', Consolas, Monaco, 'Lucida Console', monospace;
        font-size: 16px;
        font-weight: 700;
        fill: #ffc266;
        letter-spacing: 0.8px;
        filter: drop-shadow(0px 0px 6px rgba(255, 170, 40, 0.85));
      }}
      .digital-date {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 9.5px;
        font-weight: 600;
        fill: #ffe0b2;
        letter-spacing: 0.6px;
        opacity: 0.95;
        filter: drop-shadow(0px 0px 4px rgba(255, 180, 70, 0.6));
      }}

      /* Blinking LED Colons */
      .blink-colon {{
        animation: blinkColon 1s steps(1) infinite;
      }}
      @keyframes blinkColon {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0.25; }}
      }}

      /* Real-Time Digit Visibility Animations */
      .anim-digit {{
        opacity: 0;
      }}
      @keyframes secShow {{
        0%, 1.6666% {{ opacity: 1; }}
        1.6667%, 100% {{ opacity: 0; }}
      }}

      {sec_rules_str}

      /* Dynamic Atmospheric Animations */
      .wind-stream {{
        animation: windDrift 7s linear infinite;
        opacity: 0.35;
      }}
      .wind-2 {{
        animation: windDrift 9s linear infinite 3s;
        opacity: 0.25;
      }}
      @keyframes windDrift {{
        0% {{ transform: translateX(-300px); }}
        100% {{ transform: translateX(1600px); }}
      }}

      .clock-screen-box {{
        fill: #0a0705;
        fill-opacity: 0.88;
        stroke: rgba(255, 170, 50, 0.35);
        stroke-width: 1.5;
        rx: 7px;
        filter: drop-shadow(0 4px 14px rgba(0,0,0,0.85));
      }}

      .clock-screen-inner {{
        fill: none;
        stroke: rgba(255, 190, 70, 0.15);
        stroke-width: 0.8;
        rx: 5.5px;
      }}
    </style>

    <linearGradient id="windGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="transparent"/>
      <stop offset="50%" stop-color="#d2e6ff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="transparent"/>
    </linearGradient>
  </defs>

  <!-- 1. Background Night Room Artwork with scenic landscape wall -->
  <image href="{img_data_uri}" x="0" y="0" width="1536" height="1024" preserveAspectRatio="xMidYMid slice"/>

  <!-- 2. Animated Wind Streams -->
  <g pointer-events="none">
    <rect class="wind-stream" x="0" y="240" width="350" height="3" fill="url(#windGrad)"/>
    <rect class="wind-stream wind-2" x="0" y="320" width="280" height="2" fill="url(#windGrad)"/>
  </g>

  <!-- 3. Real-time Compact Digital LED Wall Clock on wall -->
  <g transform="translate(868, 217)">
    <!-- Compact Glassmorphic Clock Base -->
    <rect class="clock-screen-box" x="0" y="0" width="164" height="44" rx="7"/>
    <rect class="clock-screen-inner" x="1.5" y="1.5" width="161" height="41" rx="5.5"/>

    <!-- Static Hours -->
    <text class="digital-time" x="23.5" y="21" text-anchor="middle">{hour_str}</text>

    <!-- Blinking Colon 1 -->
    <text class="digital-time blink-colon" x="46.0" y="21" text-anchor="middle">:</text>

    <!-- Synced Minutes -->
    <text class="digital-time" x="68.5" y="21" text-anchor="middle">{cur_min:02d}</text>

    <!-- Blinking Colon 2 -->
    <text class="digital-time blink-colon" x="91.0" y="21" text-anchor="middle">:</text>

    <!-- Real-time Live Seconds (00-59) -->
    {sec_tags_str}

    <!-- AM / PM Indicator -->
    <text class="digital-time" x="140.5" y="21" text-anchor="middle">{ampm}</text>

    <!-- Date text: centered with IST indicator -->
    <text class="digital-date" x="82.0" y="35" text-anchor="middle">{date_str} (IST)</text>
  </g>
</svg>
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated updated Night Room SVG at {output_path}")

if __name__ == "__main__":
    generate_night_room_svg()
