import datetime
import base64
import os

def generate_night_room_svg(output_path="night-room-ambience.svg", png_path="night-room.png"):
    # Current timestamp
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M:%S %p")
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
      .digital-time {{
        font-family: 'Courier New', Consolas, Monaco, 'Lucida Console', monospace;
        font-size: 52px;
        font-weight: 700;
        fill: #ffc266;
        letter-spacing: 2px;
        filter: drop-shadow(0px 0px 12px rgba(255, 170, 40, 0.85));
      }}
      .digital-date {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 22px;
        font-weight: 600;
        fill: #ffe0b2;
        letter-spacing: 1.5px;
        opacity: 0.95;
        filter: drop-shadow(0px 0px 8px rgba(255, 180, 70, 0.6));
      }}

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

      .rain-line {{
        stroke: rgba(190, 215, 255, 0.3);
        stroke-width: 1.5;
        stroke-dasharray: 8 16;
        animation: rainFall 0.8s linear infinite;
      }}
      @keyframes rainFall {{
        0% {{ stroke-dashoffset: 0; }}
        100% {{ stroke-dashoffset: -48; }}
      }}

      .clock-screen-box {{
        fill: #0c0906;
        fill-opacity: 0.96;
        stroke: #3d2719;
        stroke-width: 4;
        rx: 8px;
        filter: drop-shadow(0 8px 20px rgba(0,0,0,0.9));
      }}

      .clock-screen-inner {{
        fill: #080604;
        stroke: rgba(255, 170, 50, 0.25);
        stroke-width: 1.5;
        rx: 5px;
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

  <!-- 2. Animated Rain Overlay over window -->
  <rect x="0" y="0" width="1536" height="1024" fill="url(#rainPattern)" pointer-events="none" opacity="0.4"/>

  <!-- 3. Animated Wind Streams -->
  <g pointer-events="none">
    <rect class="wind-stream" x="0" y="240" width="350" height="3" fill="url(#windGrad)"/>
    <rect class="wind-stream wind-2" x="0" y="320" width="280" height="2" fill="url(#windGrad)"/>
  </g>

  <!-- 4. Real-time Digital LED Clock centered on wall display screen -->
  <g transform="translate(680, 142)">
    <!-- Dark Frame fitting artwork screen -->
    <rect class="clock-screen-box" x="0" y="0" width="506" height="186"/>
    <rect class="clock-screen-inner" x="5" y="5" width="496" height="176"/>

    <!-- Time text: perfectly centered -->
    <text class="digital-time" x="253" y="98" text-anchor="middle">{time_str}</text>

    <!-- Date text: perfectly centered -->
    <text class="digital-date" x="253" y="148" text-anchor="middle">{date_str}</text>
  </g>
</svg>
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated updated Night Room SVG at {output_path}")

if __name__ == "__main__":
    generate_night_room_svg()
