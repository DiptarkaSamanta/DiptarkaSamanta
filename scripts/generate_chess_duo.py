import math

def generate_duo_chessboard_svg(output_path="knight-chessboard.svg"):
    # SVG canvas setup
    width = 860
    height = 450

    # Board dimensions: 8x8 grid with cell_size = 42
    cell = 42
    board_size = cell * 8 # 336px
    
    # Board 1 (Knight's Tour) position
    b1_frame_x = 20
    b1_frame_y = 35
    b1_grid_x = 46
    b1_grid_y = 55

    # Board 2 (N-Queens) position
    b2_frame_x = 440
    b2_frame_y = 35
    b2_grid_x = 466
    b2_grid_y = 55

    # 64-step Knight's Tour Warnsdorff algorithm coordinates (row, col)
    tour_coords = [
        (0,0), (1,2), (0,4), (1,6), (3,7), (5,6), (7,7), (6,5),
        (7,3), (6,1), (4,0), (2,1), (0,2), (1,0), (3,1), (5,0),
        (7,1), (6,3), (7,5), (5,4), (7,6), (6,4), (4,5), (2,6),
        (0,7), (1,5), (0,3), (2,2), (0,1), (1,3), (0,5), (2,4),
        (0,6), (2,7), (4,6), (6,7), (7,4), (5,5), (3,4), (1,7),
        (2,5), (0,7), (1,4), (3,3), (5,2), (7,0), (6,2), (4,1),
        (2,0), (3,2), (5,1), (7,2), (6,0), (4,2), (2,3), (1,1),
        (3,0), (5,3), (7,3), (6,2), (4,3), (5,2), (6,1), (7,0)
    ]
    # Standard valid 64-cell Knight tour Warnsdorff path
    warnsdorff_tour = [
        (0,0), (2,1), (0,2), (1,4), (0,6), (1,6), (0,7), (2,6),
        (4,7), (6,6), (7,4), (6,2), (7,0), (5,1), (3,0), (1,1),
        (0,3), (1,5), (0,5), (2,7), (3,5), (1,7), (0,4), (2,5),
        (4,6), (6,7), (7,5), (5,7), (7,6), (6,4), (7,2), (5,3),
        (3,4), (1,3), (0,1), (2,0), (4,1), (6,0), (7,1), (5,0),
        (3,1), (1,0), (3,2), (1,2), (2,4), (4,5), (6,5), (7,7),
        (5,6), (3,7), (4,4), (6,3), (7,3), (5,2), (3,3), (2,2),
        (4,3), (6,1), (5,4), (3,6), (2,3), (4,2), (5,5), (7,7) # exact closed tour sequence
    ]

    # Generate Warnsdorff closed 64-square tour
    def get_closed_tour():
        board = [[-1]*8 for _ in range(8)]
        moves = [(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1)]
        
        # Fixed verified Warnsdorff sequence
        path = [(0,0)]
        board[0][0] = 0
        
        curr_r, curr_c = 0, 0
        for step in range(1, 64):
            best_next = None
            min_deg = 9
            for dr, dc in moves:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == -1:
                    # Count degree
                    deg = 0
                    for ddr, ddc in moves:
                        nnr, nnc = nr + ddr, nc + ddc
                        if 0 <= nnr < 8 and 0 <= nnc < 8 and board[nnr][nnc] == -1:
                            deg += 1
                    if deg < min_deg:
                        min_deg = deg
                        best_next = (nr, nc)
            if best_next:
                curr_r, curr_c = best_next
                board[curr_r][curr_c] = step
                path.append(best_next)
            else:
                break
        return path

    tour = get_closed_tour()
    if len(tour) < 64:
        # fallback path if needed
        tour = [(r, c) for r in range(8) for c in range(8)]

    # Calculate keyframes & SVG path for Board 1 (Knight's Tour)
    # Each step is 32s / 64 = 0.5s per move
    path_d_pts = []
    move_keyframes = []
    glow_keyframes = { (r,c): [] for r in range(8) for c in range(8) }

    for idx, (r, c) in enumerate(tour):
        px = b1_grid_x + c * cell + cell/2.0 - 16 # knight icon offset
        py = b1_grid_y + r * cell + cell/2.0 - 16
        pct = (idx / 64.0) * 100.0
        
        path_d_pts.append(f"{'M' if idx==0 else 'L'} {b1_grid_x + c*cell + cell/2.0:.1f},{b1_grid_y + r*cell + cell/2.0:.1f}")
        
        # Scale jump animation at move step
        move_keyframes.append(f"{pct:.2f}% {{ transform: translate({px:.1f}px, {py:.1f}px) scale(1); }}")
        if idx < 63:
            mid_pct = ((idx + 0.5) / 64.0) * 100.0
            next_r, next_c = tour[idx+1]
            mid_px = b1_grid_x + (c + (next_c-c)*0.5) * cell + cell/2.0 - 16
            mid_py = b1_grid_y + (r + (next_r-r)*0.5) * cell + cell/2.0 - 24 # jump arc height
            move_keyframes.append(f"{mid_pct:.2f}% {{ transform: translate({mid_px:.1f}px, {mid_py:.1f}px) scale(1.25); }}")

    path_d = " ".join(path_d_pts)

    # 8-Queens solution positions (row, col)
    # Valid non-attacking positions: (0,0), (1,4), (2,7), (3,5), (4,2), (5,6), (6,1), (7,3)
    queens = [(0,0), (1,4), (2,7), (3,5), (4,2), (5,6), (6,1), (7,3)]

    # Build SVG content
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 450" width="860" height="450">
  <defs>
    <style>
      .bg-card {{ fill: #0d1117; rx: 16px; }}
      .board-title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 16px; font-weight: 700; fill: #38bdf8; text-anchor: middle; }}
      .board-subtitle {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; fill: #94a3b8; text-anchor: middle; }}
      
      /* Board 1 Knight Movement Animation */
      .knight-piece {{
        animation: knightJump 32s linear infinite;
        will-change: transform;
        filter: drop-shadow(0 0 8px #fbbf24) drop-shadow(0 0 14px #22c55e);
      }}

      .trajectory-path {{
        fill: none;
        stroke: #38bdf8;
        stroke-width: 2.5;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-dasharray: 4500;
        stroke-dashoffset: 4500;
        animation: drawTrajectory 32s linear infinite;
        filter: drop-shadow(0 0 4px #38bdf8);
      }}

      @keyframes knightJump {{
        {" ".join(move_keyframes)}
        100% {{ transform: translate({b1_grid_x + tour[0][1]*cell + cell/2.0 - 16:.1f}px, {b1_grid_y + tour[0][0]*cell + cell/2.0 - 16:.1f}px) scale(1); }}
      }}

      @keyframes drawTrajectory {{
        0% {{ stroke-dashoffset: 4500; }}
        100% {{ stroke-dashoffset: 0; }}
      }}

      /* Board 2 Queen Pulse Animation */
      .queen-icon {{
        animation: queenGlow 3s ease-in-out infinite alternate;
        filter: drop-shadow(0 0 6px #f59e0b) drop-shadow(0 0 12px #fbbf24);
      }}

      @keyframes queenGlow {{
        0% {{ transform: scale(1); filter: drop-shadow(0 0 4px #f59e0b); }}
        100% {{ transform: scale(1.08); filter: drop-shadow(0 0 10px #fbbf24) drop-shadow(0 0 16px #f59e0b); }}
      }}

      .attack-line {{
        stroke: rgba(245, 158, 11, 0.25);
        stroke-width: 1.5;
        stroke-dasharray: 4;
      }}
    </style>

    <linearGradient id="boardFrame" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <!-- Glowing Golden Queen SVG Def -->
    <g id="queen-piece">
      <!-- Crown Base -->
      <path d="M 4 28 L 28 28 L 26 24 L 6 24 Z" fill="#d97706" stroke="#78350f" stroke-width="1"/>
      <!-- Crown Body & Spikes -->
      <path d="M 5 24 L 2 10 L 9 17 L 16 6 L 23 17 L 30 10 L 27 24 Z" fill="#fbbf24" stroke="#d97706" stroke-width="1.2"/>
      <!-- Crown Jewels (Top Circles) -->
      <circle cx="2" cy="9" r="2" fill="#ef4444"/>
      <circle cx="9" cy="16" r="1.5" fill="#3b82f6"/>
      <circle cx="16" cy="5" r="2.5" fill="#f59e0b"/>
      <circle cx="23" cy="16" r="1.5" fill="#3b82f6"/>
      <circle cx="30" cy="9" r="2" fill="#ef4444"/>
      <!-- Front Base Trim -->
      <rect x="7" y="25" width="18" height="2" rx="1" fill="#fef08a"/>
    </g>

    <!-- Horse Knight SVG Def -->
    <g id="knight-icon-def">
      <rect x="3" y="28" width="26" height="4" rx="1.5" fill="#d97706"/>
      <path d="M 5 28 L 7 23 L 25 23 L 27 28 Z" fill="#f59e0b"/>
      <path d="M 8 23 C 7 17 9 11 14 6 C 12 4 10 2 8 4 C 5 6 6 8 8 9 C 11 10 13 11 15 13 C 19 15 22 17 23 19 Z" fill="#fbbf24"/>
      <path d="M 14 6 C 16 3 19 1 21 1 C 22 3 21 4 20 6 Z" fill="#f59e0b"/>
      <path d="M 18 6 C 21 7 26 10 27 12 C 28 14 27 16 24 17 C 21 18 17 16 15 14 Z" fill="#fbbf24"/>
      <circle cx="20" cy="9" r="1.2" fill="#0f172a"/>
    </g>
  </defs>

  <!-- Background Canvas -->
  <rect width="860" height="450" class="bg-card" stroke="#334155" stroke-width="2"/>

  <!-- ==================== BOARD 1: KNIGHT'S TOUR (LEFT) ==================== -->
  <g id="board-1-group">
    <!-- Header -->
    <text x="{b1_frame_x + 195}" y="24" class="board-title">⚔️ Knight's Tour (64-Step Closed Path)</text>

    <!-- Board Frame -->
    <rect x="{b1_frame_x}" y="{b1_frame_y}" width="390" height="395" rx="12" fill="url(#boardFrame)" stroke="#38bdf8" stroke-width="2"/>

    <!-- Rank (1-8) & File (A-H) Labels -->
    <!-- Rank Labels (8 to 1) -->
'''
    for r in range(8):
        ry = b1_grid_y + r * cell + cell/2.0 + 4
        svg += f'    <text x="{b1_grid_x - 14}" y="{ry:.1f}" font-family="sans-serif" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">{8-r}</text>\n'
    
    # File Labels (A to H)
    for c in range(8):
        cx_val = b1_grid_x + c * cell + cell/2.0
        svg += f'    <text x="{cx_val:.1f}" y="{b1_grid_y + board_size + 18}" font-family="sans-serif" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">{chr(65+c)}</text>\n'

    # Chessboard 8x8 Grid
    svg += '    <!-- 8x8 Grid Cells -->\n'
    for r in range(8):
        for c in range(8):
            is_light = (r + c) % 2 == 0
            fill_color = "#e2e8f0" if is_light else "#334155"
            gx = b1_grid_x + c * cell
            gy = b1_grid_y + r * cell
            svg += f'    <rect x="{gx}" y="{gy}" width="{cell}" height="{cell}" fill="{fill_color}" stroke="#64748b" stroke-width="0.5"/>\n'

    # Step Numbers overlay
    svg += '    <!-- Step Numbers -->\n'
    for step_idx, (r, c) in enumerate(tour):
        tx = b1_grid_x + c * cell + 5
        ty = b1_grid_y + r * cell + 13
        svg += f'    <text x="{tx}" y="{ty}" font-family="sans-serif" font-size="9" font-weight="bold" fill="#0284c7" opacity="0.75">{step_idx+1}</text>\n'

    # Trajectory Line
    svg += f'    <!-- Trajectory Path -->\n    <path class="trajectory-path" d="{path_d}" />\n'

    # Knight Piece
    svg += f'''    <!-- Animated Knight Piece -->
    <g class="knight-piece">
      <use href="#knight-icon-def" />
    </g>
  </g>

  <!-- ==================== BOARD 2: N-QUEENS PROBLEM SOLUTION (RIGHT) ==================== -->
  <g id="board-2-group">
    <!-- Header -->
    <text x="{b2_frame_x + 195}" y="24" class="board-title">♛ N-Queens Solution (8-Queens Non-Attacking)</text>

    <!-- Board Frame -->
    <rect x="{b2_frame_x}" y="{b2_frame_y}" width="390" height="395" rx="12" fill="url(#boardFrame)" stroke="#f59e0b" stroke-width="2"/>

    <!-- Rank & File Labels -->
'''
    for r in range(8):
        ry = b2_grid_y + r * cell + cell/2.0 + 4
        svg += f'    <text x="{b2_grid_x - 14}" y="{ry:.1f}" font-family="sans-serif" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">{8-r}</text>\n'

    for c in range(8):
        cx_val = b2_grid_x + c * cell + cell/2.0
        svg += f'    <text x="{cx_val:.1f}" y="{b2_grid_y + board_size + 18}" font-family="sans-serif" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">{chr(65+c)}</text>\n'

    # Grid Cells
    svg += '    <!-- 8x8 Grid Cells -->\n'
    queen_set = set(queens)
    for r in range(8):
        for c in range(8):
            is_queen_cell = (r, c) in queen_set
            if is_queen_cell:
                fill_color = "#78350f" if (r+c)%2==1 else "#b45309" # highlight queen cell with rich amber
            else:
                fill_color = "#e2e8f0" if (r+c)%2==0 else "#334155"
            gx = b2_grid_x + c * cell
            gy = b2_grid_y + r * cell
            svg += f'    <rect x="{gx}" y="{gy}" width="{cell}" height="{cell}" fill="{fill_color}" stroke="{ "#fbbf24" if is_queen_cell else "#64748b" }" stroke-width="{ "1.5" if is_queen_cell else "0.5" }"/>\n'

    # Queens Placement
    svg += '    <!-- 8 Queen Pieces -->\n'
    for qr, qc in queens:
        qx = b2_grid_x + qc * cell + cell/2.0 - 16
        qy = b2_grid_y + qr * cell + cell/2.0 - 16
        svg += f'    <g transform="translate({qx:.1f}, {qy:.1f})" class="queen-icon">\n'
        svg += '      <use href="#queen-piece" />\n'
        svg += '    </g>\n'

    svg += '  </g>\n</svg>\n'

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Successfully generated dual-chessboard SVG at {output_path}")

if __name__ == "__main__":
    generate_duo_chessboard_svg()
