import datetime
import base64
import os

def generate_night_room_svg(output_path="night-room-ambience.svg", png_path="night-room.png"):
    # Current UTC or local timestamp for initial generation
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M:%S")
    ampm_str = now.strftime("%p")
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

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1536 1024" width="100%" height="100%">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;700&amp;family=Inter:wght@400;600&amp;display=swap');

      .clock-container {{
        font-family: 'Fira Code', 'Courier New', monospace;
      }}
      .clock-time {{
        font-size: 38px;
        font-weight: 700;
        fill: #ffdf9a;
        letter-spacing: 2px;
        filter: drop-shadow(0px 0px 8px rgba(255, 190, 90, 0.8));
      }}
      .clock-ampm {{
        font-size: 16px;
        font-weight: 700;
        fill: #ffb84d;
      }}
      .clock-date {{
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 600;
        fill: rgba(255, 223, 154, 0.85);
        letter-spacing: 0.5px;
      }}
      .moon-icon {{
        font-size: 32px;
        fill: #ffdf9a;
        animation: moonGlow 3s ease-in-out infinite alternate;
      }}

      /* Dynamic Animations */
      @keyframes moonGlow {{
        0% {{ filter: drop-shadow(0 0 4px rgba(255,223,154,0.4)); opacity: 0.85; }}
        100% {{ filter: drop-shadow(0 0 14px rgba(255,190,90,0.95)); opacity: 1; }}
      }}

      .wind-stream {{
        animation: windDrift 6s linear infinite;
        opacity: 0.4;
      }}
      .wind-2 {{
        animation: windDrift 8s linear infinite 2.5s;
        opacity: 0.3;
      }}
      @keyframes windDrift {{
        0% {{ transform: translateX(-300px); }}
        100% {{ transform: translateX(1600px); }}
      }}

      .rain-line {{
        stroke: rgba(190, 215, 255, 0.35);
        stroke-width: 1.5;
        stroke-dasharray: 8 16;
        animation: rainFall 0.8s linear infinite;
      }}
      @keyframes rainFall {{
        0% {{ stroke-dashoffset: 0; }}
        100% {{ stroke-dashoffset: -48; }}
      }}

      .clock-box {{
        fill: #070a11;
        fill-opacity: 0.93;
        stroke: rgba(255, 224, 165, 0.25);
        stroke-width: 2.5;
        rx: 8px;
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.6));
      }}
    </style>

    <linearGradient id="windGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="transparent"/>
      <stop offset="50%" stop-color="#d2e6ff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="transparent"/>
    </linearGradient>

    <pattern id="rainPattern" width="60" height="60" patternUnits="userSpaceOnUse" patternTransform="rotate(15)">
      <line x1="10" y1="0" x2="10" y2="60" class="rain-line" />
      <line x1="35" y1="20" x2="35" y2="80" class="rain-line" />
    </pattern>
  </defs>

  <!-- 1. Background Night Room Artwork -->
  <image href="{img_data_uri}" x="0" y="0" width="1536" height="1024" preserveAspectRatio="xMidYMid slice"/>

  <!-- 2. Animated Rain Overlay -->
  <rect x="0" y="0" width="1536" height="1024" fill="url(#rainPattern)" pointer-events="none" opacity="0.45"/>

  <!-- 3. Animated Wind Streams -->
  <g pointer-events="none">
    <rect class="wind-stream" x="0" y="240" width="350" height="3" fill="url(#windGrad)"/>
    <rect class="wind-stream wind-2" x="0" y="320" width="280" height="2" fill="url(#windGrad)"/>
  </g>

  <!-- 4. Live Digital Clock Container positioned over Artwork Screen -->
  <!-- Box at x=998 (65%), y=196 (19.2%), w=318 (20.7%), h=123 (12%) -->
  <g transform="translate(998, 196)">
    <rect class="clock-box" x="0" y="0" width="318" height="125"/>

    <!-- Moon Icon -->
    <text class="moon-icon" x="20" y="58">☾</text>

    <!-- Time text -->
    <text class="clock-container clock-time" x="72" y="54">{time_str}</text>
    <text class="clock-container clock-ampm" x="255" y="54">{ampm_str}</text>

    <!-- Date text -->
    <text class="clock-date" x="159" y="98" text-anchor="middle">{date_str}</text>
  </g>
</svg>
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated animated Night Room SVG at {output_path}")

if __name__ == "__main__":
    generate_night_room_svg()
