def generate_nqueens_svg(output_path="n-queens-chessboard.svg"):
    # 8-Queens solution coordinates: (row 0..7, col 0..7)
    # A8 (0,0), E7 (1,4), H6 (2,7), F5 (3,5), C4 (4,2), G3 (5,6), B2 (6,1), D1 (7,3)
    queens = [(0,0), (1,4), (2,7), (3,5), (4,2), (5,6), (6,1), (7,3)]
    queen_set = set(queens)

    cell = 48
    grid_x = 410
    grid_y = 25

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 450" width="860" height="450">
  <defs>
    <style>
      .bg-card {{ fill: #0f172a; rx: 16px; }}
      .header-title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 22px; font-weight: 800; fill: #f59e0b; }}
      .header-sub {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; fill: #94a3b8; }}

      .queen-piece-glow {{
        animation: queenPulse 3s ease-in-out infinite alternate;
        filter: drop-shadow(0 0 8px #f59e0b) drop-shadow(0 0 14px #fbbf24);
      }}

      @keyframes queenPulse {{
        0% {{ transform: scale(1); filter: drop-shadow(0 0 6px #f59e0b); }}
        100% {{ transform: scale(1.06); filter: drop-shadow(0 0 12px #fbbf24) drop-shadow(0 0 18px #f59e0b); }}
      }}
    </style>

    <linearGradient id="boardFrame" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <!-- Golden Queen Crown Piece -->
    <g id="queen-crown">
      <path d="M 4 28 L 28 28 L 26 24 L 6 24 Z" fill="#d97706" stroke="#78350f" stroke-width="1"/>
      <path d="M 5 24 L 2 10 L 9 17 L 16 6 L 23 17 L 30 10 L 27 24 Z" fill="#fbbf24" stroke="#d97706" stroke-width="1.2"/>
      <circle cx="2" cy="9" r="2" fill="#ef4444"/>
      <circle cx="9" cy="16" r="1.5" fill="#3b82f6"/>
      <circle cx="16" cy="5" r="2.5" fill="#f59e0b"/>
      <circle cx="23" cy="16" r="1.5" fill="#3b82f6"/>
      <circle cx="30" cy="9" r="2" fill="#ef4444"/>
      <rect x="7" y="25" width="18" height="2" rx="1" fill="#fef08a"/>
    </g>
  </defs>

  <!-- Background Card -->
  <rect width="860" height="450" class="bg-card" stroke="#334155" stroke-width="2"/>

  <!-- Left Sidebar Panel -->
  <g transform="translate(30, 20)">
    <text x="0" y="35" class="header-title">♛ N-Queens Problem</text>
    <text x="0" y="60" class="header-sub">8-Queens Non-Attacking Solution</text>

    <!-- Info Cards -->
    <g transform="translate(0, 90)">
      <rect width="320" height="46" rx="10" fill="#1e293b" stroke="#334155"/>
      <text x="18" y="28" font-family="sans-serif" font-size="14" fill="#94a3b8">Piece: <tspan fill="#fbbf24" font-weight="bold">Golden Queen ♛</tspan></text>
    </g>
    
    <g transform="translate(0, 150)">
      <rect width="320" height="46" rx="10" fill="#1e293b" stroke="#334155"/>
      <text x="18" y="28" font-family="sans-serif" font-size="14" fill="#94a3b8">Constraint: <tspan fill="#f59e0b" font-weight="bold">Zero Attacking Lines</tspan></text>
    </g>
    
    <g transform="translate(0, 210)">
      <rect width="320" height="46" rx="10" fill="#1e293b" stroke="#334155"/>
      <text x="18" y="28" font-family="sans-serif" font-size="14" fill="#94a3b8">Board Status: <tspan fill="#22c55e" font-weight="bold">8 Queens Placed Safely</tspan></text>
    </g>

    <!-- Legend -->
    <g transform="translate(0, 280)">
      <text x="0" y="15" font-family="sans-serif" font-size="13" font-weight="bold" fill="#f8fafc">Board Legend:</text>
      
      <rect x="0" y="30" width="20" height="20" rx="4" fill="#78350f" stroke="#fbbf24"/>
      <text x="30" y="45" font-family="sans-serif" font-size="13" fill="#fbbf24" font-weight="bold">Queen Square</text>
      
      <rect x="150" y="30" width="20" height="20" rx="4" fill="#334155" stroke="#64748b"/>
      <text x="180" y="45" font-family="sans-serif" font-size="13" fill="#94a3b8" font-weight="bold">Empty Square</text>
    </g>
  </g>

  <!-- Chessboard Frame -->
  <rect x="384" y="13" width="424" height="430" rx="12" fill="url(#boardFrame)" stroke="#f59e0b" stroke-width="2"/>

  <!-- Rank (1-8) and File (A-H) Labels -->
  <text x="396" y="53.0" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">8</text> <text x="396" y="101.0" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">7</text> <text x="396" y="149.0" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">6</text> <text x="396" y="197.0" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">5</text> <text x="396" y="245.0" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">4</text> <text x="396" y="293.0" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">3</text> <text x="396" y="341.0" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">2</text> <text x="396" y="389.0" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">1</text>
  <text x="434.0" y="429" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">A</text> <text x="482.0" y="429" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">B</text> <text x="530.0" y="429" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">C</text> <text x="578.0" y="429" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">D</text> <text x="626.0" y="429" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">E</text> <text x="674.0" y="429" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">F</text> <text x="722.0" y="429" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">G</text> <text x="770.0" y="429" font-family="sans-serif" font-size="12" font-weight="bold" fill="#94a3b8" text-anchor="middle">H</text>

  <!-- 8x8 Chessboard Grid -->
  <g>
'''

    for r in range(8):
        for c in range(8):
            is_q = (r, c) in queen_set
            if is_q:
                fill_col = "#78350f" if (r+c)%2==1 else "#b45309"
                stroke_col = "#fbbf24"
                stroke_w = "1.5"
            else:
                fill_col = "#e2e8f0" if (r+c)%2==0 else "#334155"
                stroke_col = "#64748b"
                stroke_w = "0.5"

            x_pos = grid_x + c * cell
            y_pos = grid_y + r * cell
            svg_content += f'    <rect x="{x_pos}" y="{y_pos}" width="{cell}" height="{cell}" fill="{fill_col}" stroke="{stroke_col}" stroke-width="{stroke_w}"/>\n'

    svg_content += '  </g>\n\n  <!-- Queen Pieces Placement -->\n  <g>\n'

    for qr, qc in queens:
        qx = grid_x + qc * cell + cell/2.0 - 16
        qy = grid_y + qr * cell + cell/2.0 - 16
        svg_content += f'    <g transform="translate({qx:.1f}, {qy:.1f})" class="queen-piece-glow">\n'
        svg_content += '      <use href="#queen-crown" />\n'
        svg_content += '    </g>\n'

    svg_content += '  </g>\n</svg>\n'

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated N-Queens SVG at {output_path}")

if __name__ == "__main__":
    generate_nqueens_svg()
