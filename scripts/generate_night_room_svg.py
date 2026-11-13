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
    
    cur_sec = now.second
    cur_min = now.minute
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

    # 1. Live Seconds (60s loop with clean steps)
    sec_css = []
    sec_tags = []
    for s in range(60):
        time_since_s = (cur_sec - s) % 60
        delay = -time_since_s
        sec_css.append(f".s-{s:02d} {{ animation: secShow 60s steps(1) infinite {delay}s; }}")
        sec_tags.append(f'<text class="digital-time anim-digit s-{s:02d}" x="162.0" y="24" text-anchor="middle">{s:02d}</text>')

    # 2. Live Minutes (3600s loop with clean steps)
    elapsed_in_hour = cur_min * 60 + cur_sec
    min_css = []
    min_tags = []
    for m in range(60):
        time_since_m = (elapsed_in_hour - m * 60) % 3600
        delay = -time_since_m
        min_css.append(f".m-{m:02d} {{ animation: minShow 3600s steps(1) infinite {delay}s; }}")
        min_tags.append(f'<text class="digital-time anim-digit m-{m:02d}" x="102.0" y="24" text-anchor="middle">{m:02d}</text>')

    # 3. Live Hours (43200s / 12h loop with clean steps)
    elapsed_in_12h = (now.hour % 12) * 3600 + now.minute * 60 + now.second
    hour_css = []
    hour_tags = []
    for h in range(1, 13):
        h_offset = (h % 12) * 3600
        time_since_h = (elapsed_in_12h - h_offset) % 43200
        delay = -time_since_h
        hour_css.append(f".h-{h:02d} {{ animation: hourShow 43200s steps(1) infinite {delay}s; }}")
        hour_tags.append(f'<text class="digital-time anim-digit h-{h:02d}" x="42.0" y="24" text-anchor="middle">{h:02d}</text>')

    # 4. Live AM / PM (86400s / 24h loop with clean steps)
    elapsed_in_day = now.hour * 3600 + now.minute * 60 + now.second
    delay_day = -elapsed_in_day
    ampm_css = [
        f".ampm-am {{ animation: amShow 86400s steps(1) infinite {delay_day}s; }}",
        f".ampm-pm {{ animation: pmShow 86400s steps(1) infinite {delay_day}s; }}"
    ]
    ampm_tags = [
        '<text class="digital-time anim-digit ampm-am" x="198.0" y="24" text-anchor="middle">AM</text>',
        '<text class="digital-time anim-digit ampm-pm" x="198.0" y="24" text-anchor="middle">PM</text>'
    ]

    sec_rules_str = "\n      ".join(sec_css)
    min_rules_str = "\n      ".join(min_css)
    hour_rules_str = "\n      ".join(hour_css)
    ampm_rules_str = "\n      ".join(ampm_css)

    sec_tags_str = "\n    ".join(sec_tags)
    min_tags_str = "\n    ".join(min_tags)
    hour_tags_str = "\n    ".join(hour_tags)
    ampm_tags_str = "\n    ".join(ampm_tags)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1536 1024" width="100%" height="100%">
  <defs>
    <style>
      .digital-time {{
        font-family: 'Courier New', Consolas, Monaco, 'Lucida Console', monospace;
        font-size: 21px;
        font-weight: 700;
        fill: #ffc266;
        letter-spacing: 0.8px;
        filter: drop-shadow(0px 0px 6px rgba(255, 170, 40, 0.85));
      }}
      .digital-date {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 12px;
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

      /* Real-Time Digit Visibility Animations (no interpolation, clean steps) */
      .anim-digit {{
        opacity: 0;
      }}
      @keyframes secShow {{
        0%, 1.6666% {{ opacity: 1; }}
        1.6667%, 100% {{ opacity: 0; }}
      }}
      @keyframes minShow {{
        0%, 1.6666% {{ opacity: 1; }}
        1.6667%, 100% {{ opacity: 0; }}
      }}
      @keyframes hourShow {{
        0%, 8.3333% {{ opacity: 1; }}
        8.3334%, 100% {{ opacity: 0; }}
      }}
      @keyframes amShow {{
        0%, 49.9999% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes pmShow {{
        0%, 49.9999% {{ opacity: 0; }}
        50%, 100% {{ opacity: 1; }}
      }}

      {hour_rules_str}

      {min_rules_str}

      {sec_rules_str}

      {ampm_rules_str}

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
        fill-opacity: 0.92;
        stroke: rgba(255, 170, 50, 0.45);
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

  <!-- 3. Real-time Compact Digital LED Wall Clock positioned between the two picture frames -->
  <g transform="translate(830, 141)">
    <!-- Compact Glassmorphic Clock Base -->
    <rect class="clock-screen-box" x="0" y="0" width="240" height="48" rx="7"/>
    <rect class="clock-screen-inner" x="1.5" y="1.5" width="237" height="45" rx="5.5"/>

    <!-- Real-time Live Hours (01-12) -->
    {hour_tags_str}

    <!-- Blinking Colon 1 -->
    <text class="digital-time blink-colon" x="72.0" y="24" text-anchor="middle">:</text>

    <!-- Real-time Live Minutes (00-59) -->
    {min_tags_str}

    <!-- Blinking Colon 2 -->
    <text class="digital-time blink-colon" x="132.0" y="24" text-anchor="middle">:</text>

    <!-- Real-time Live Seconds (00-59) -->
    {sec_tags_str}

    <!-- Real-time Live AM / PM Indicator -->
    {ampm_tags_str}

    <!-- Date text: centered with IST indicator -->
    <text class="digital-date" x="120.0" y="38" text-anchor="middle">{date_str} (IST)</text>
  </g>
</svg>
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated updated Night Room SVG at {output_path}")

if __name__ == "__main__":
    generate_night_room_svg()
