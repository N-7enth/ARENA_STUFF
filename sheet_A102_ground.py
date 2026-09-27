# A102 - Ground Floor Plan (detailed)
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle
import numpy as np
from arch_lib import *

def build():
    fig, ax = setup_sheet(figsize=(11.9, 16.8))
    # Building local coords: x 0-10.17 (W-E), y 0-39.4 (S-N). Place with margin for dims/title.
    # Data limits: x -6..18, y -6..46
    ax.set_xlim(-7, 20)
    ax.set_ylim(-7.5, 47)

    draw_border(ax, -7, -7.5, 27, 54.5)
    draw_title_block(ax, 0.5, -6.8, 18.5, "A102", "GROUND FLOOR PLAN  •  MACHINE LAYOUT  •  PRODUCTION FLOW N→S", "1:100")

    ax.text(6.5, 45.3, "GROUND FLOOR PLAN  —  PRODUCTION HALL  10.17 × 39.40m  (400.7 m²)", ha='center', va='center', fontsize=11, weight='bold', color='#0F2A52')
    ax.text(6.5, 44.1, "3 entrances on WEST wall  •  Printing room walled + own EAST entrance  •  Steel stanchions @6.0m  •  Flow: Raw → Mix → Extrude → Print → Cut/Seal → QC → FG → Dispatch", ha='center', va='center', fontsize=5.5, color='#333333')

    bx0, by0 = 1.5, 0.0
    bw, bl = 10.17, 39.40
    bx1, by1 = bx0+bw, by0+bl

    # outer walls (thick)
    ax.add_patch(Rectangle((bx0, by0), bw, bl, facecolor='white', edgecolor=COLORS['wall_blue'], linewidth=2.4, zorder=3))
    # wall hatch (inner thin)
    ax.add_patch(Rectangle((bx0+0.23, by0+0.23), bw-0.46, bl-0.46, facecolor='none', edgecolor=COLORS['wall_blue'], linewidth=0.6, zorder=4))

    # grid: bays from south: 3.4,6,6,6,6,6,6
    bays = [3.4, 6, 6, 6, 6, 6, 6]
    grid_ys = [by0]
    yy = by0
    bay_names = []
    for b in bays:
        yy += b
        grid_ys.append(yy)
    grid_labels = ["1","2","3","4","5","6","7","8"]
    for i, gy in enumerate(grid_ys):
        # grid line
        ax.plot([bx0, bx1], [gy, gy], color=COLORS['steel'], lw=0.35, linestyle=(0,(4,3)), alpha=0.45, zorder=2)
        # stanchions
        for gx in [bx0, bx1]:
            ax.add_patch(Rectangle((gx-0.22, gy-0.22), 0.44, 0.44, facecolor=COLORS['steel'], edgecolor='white', linewidth=0.6, zorder=8))
        # bubbles
        draw_grid_bubble(ax, bx0-0.85, gy, grid_labels[i], r=0.32)
        if i == 0 or i == len(grid_ys)-1:
            pass
    # A-B bubbles south/north
    draw_grid_bubble(ax, bx0, by0-0.85, "A", r=0.32)
    draw_grid_bubble(ax, bx1, by0-0.85, "B", r=0.32)
    draw_grid_bubble(ax, bx0, by1+0.85, "A", r=0.32)
    draw_grid_bubble(ax, bx1, by1+0.85, "B", r=0.32)
    ax.text(bx0-0.85, by1+1.7, "GRID @6.0m (last bay 3.4m S)", ha='center', va='bottom', fontsize=4, color=COLORS['steel'], style='italic')

    # ---------- ZONES ----------
    # South zone: y 0-9.4 (mezz above) : Reception/Stair (W-S), QC Lab (W-N of south zone), FG Store (E)
    sz_top = by0 + 9.4  # = grid line 3? 3.4+6=9.4 yes
    mid_x = bx0 + 5.50  # split W rooms / FG store
    # FG STORE (E, full south depth)
    ax.add_patch(Rectangle((mid_x, by0+0.23), bx1-mid_x-0.23, 9.4-0.46, facecolor=COLORS['fg'], edgecolor='#1565C0', linewidth=1.2, zorder=4))
    label_room(ax, mid_x, by0, bx1-mid_x, 9.4, "FINISHED GOODS\nSTORE", "≈ 41 m²", fontsize=6, color='#0D47A1')
    draw_pallets(ax, mid_x+0.4, by0+1.2, cols=3, rows=3, pw=0.95, pd=0.95, gap=0.15)
    draw_pallets(ax, mid_x+0.4, by0+4.8, cols=3, rows=2, pw=0.95, pd=0.95, gap=0.15)
    # Reception (W-S): y 0-5.0
    rec_top = by0 + 5.0
    ax.add_patch(Rectangle((bx0+0.23, by0+0.23), mid_x-bx0-0.46, 5.0-0.46, facecolor=COLORS['office'], edgecolor='#F9A825', linewidth=1.2, zorder=4))
    ax.text((bx0+mid_x)/2, by0+4.3, "RECEPTION / STAIRCASE", ha='center', va='center', fontsize=5, weight='bold', color='#5D4037')
    ax.text((bx0+mid_x)/2, by0+3.85, "Main personnel entry (W) + S door", ha='center', va='center', fontsize=3.8, color='#795548')
    # stair (U-shape simplified as two runs)
    draw_stair(ax, bx0+0.5, by0+0.6, 1.4, 2.6, direction='up', n_steps=9)
    ax.text(bx0+1.2, by0+0.35, "STAIR TO MEZZ.", ha='center', va='top', fontsize=3.5, weight='bold', color='#4E342E')
    # WC under stair
    ax.add_patch(Rectangle((bx0+2.2, by0+0.6), 1.6, 1.3, facecolor=COLORS['toilet'], edgecolor='#0288D1', linewidth=0.8, zorder=5))
    ax.text(bx0+3.0, by0+1.25, "WC", ha='center', va='center', fontsize=4, weight='bold', color='#01579B')
    # office desk hint
    ax.add_patch(Rectangle((mid_x-1.7, by0+0.6), 1.4, 0.7, facecolor='white', edgecolor='#5D4037', linewidth=0.7, zorder=5))
    ax.text(mid_x-1.0, by0+0.95, "DESK", ha='center', va='center', fontsize=3.5, color='#5D4037')
    # QC LAB (W, y 5.0-9.4)
    ax.add_patch(Rectangle((bx0+0.23, rec_top), mid_x-bx0-0.46, sz_top-rec_top-0.23, facecolor=COLORS['qc'], edgecolor='#00796B', linewidth=1.2, zorder=4))
    ax.text((bx0+mid_x)/2, sz_top-0.9, "QC  LAB / QC OFFICE", ha='center', va='center', fontsize=5, weight='bold', color='#004D40')
    ax.text((bx0+mid_x)/2, sz_top-1.5, "lab benches + inspection", ha='center', va='center', fontsize=3.8, color='#00695C')
    # benches
    ax.add_patch(Rectangle((bx0+0.6, rec_top+0.4), 2.0, 0.7, facecolor='white', edgecolor='#00796B', linewidth=0.7, zorder=5))
    ax.text(bx0+1.6, rec_top+0.75, "BENCH", ha='center', va='center', fontsize=3.5, color='#00796B')
    ax.add_patch(Rectangle((mid_x-2.3, rec_top+0.4), 2.0, 0.7, facecolor='white', edgecolor='#00796B', linewidth=0.7, zorder=5))
    ax.text(mid_x-1.3, rec_top+0.75, "BENCH", ha='center', va='center', fontsize=3.5, color='#00796B')
    ax.add_patch(Rectangle((bx0+0.6, rec_top+1.5), 1.2, 1.2, facecolor='#E0F2F1', edgecolor='#00796B', linewidth=0.6, linestyle=(0,(2,2)), zorder=5))
    ax.text(bx0+1.2, rec_top+2.1, "M10\nQC TEST", ha='center', va='center', fontsize=3.5, weight='bold', color='#00796B')

    # partition between W rooms and FG (with door)
    ax.plot([mid_x, mid_x], [by0+0.23, sz_top-0.23], color='#1565C0', lw=1.4, zorder=6)
    # door FG <-> hall (north wall of FG)
    # (gap + swing)
    # North wall of south zone (with 2 openings to hall)
    ax.plot([bx0+0.23, mid_x-0.8], [sz_top, sz_top], color=COLORS['wall_blue'], lw=2.0, zorder=6)
    ax.plot([mid_x+0.8, mid_x+2.2], [sz_top, sz_top], color=COLORS['wall_blue'], lw=2.0, zorder=6)
    ax.plot([mid_x+3.4, bx1-0.23], [sz_top, sz_top], color=COLORS['wall_blue'], lw=2.0, zorder=6)
    ax.text(mid_x-0.1, sz_top+0.25, "1.6m", ha='center', va='bottom', fontsize=3.5, color='#333333')
    ax.text(mid_x+2.8, sz_top+0.25, "1.2m", ha='center', va='bottom', fontsize=3.5, color='#333333')

    # ---------- NORTH ZONE: RAW STORE (W) + PRINTING (E) ----------
    nz_bot = by1 - 6.0
    div_x = bx0 + 5.50
    # RAW STORE
    ax.add_patch(Rectangle((bx0+0.23, nz_bot), div_x-bx0-0.46, 6.0-0.46, facecolor=COLORS['store'], edgecolor='#2E7D32', linewidth=1.2, zorder=4))
    ax.text((bx0+div_x)/2, by1-1.0, "RAW MATERIAL STORE", ha='center', va='center', fontsize=5.5, weight='bold', color='#1B5E20')
    ax.text((bx0+div_x)/2, by1-1.65, "resin, additives  ≈ 30 m²", ha='center', va='center', fontsize=3.8, color='#2E7D32')
    draw_pallets(ax, bx0+0.6, nz_bot+0.6, cols=3, rows=2, pw=0.95, pd=0.95, gap=0.15)
    # PRINTING (walled, chemical)
    ax.add_patch(Rectangle((div_x, nz_bot), bx1-div_x-0.23, 6.0-0.46, facecolor=COLORS['print_fill'], edgecolor=COLORS['print_wall'], linewidth=1.8, zorder=4))
    # double-line to show acoustic/fire wall + hatch
    ax.add_patch(Rectangle((div_x+0.15, nz_bot+0.15), bx1-div_x-0.53, 6.0-0.76, facecolor='none', edgecolor=COLORS['print_wall'], linewidth=0.5, linestyle=(0,(3,2)), zorder=5))
    ax.text((div_x+bx1)/2, by1-0.85, "PRINTING SECTION", ha='center', va='center', fontsize=5.5, weight='bold', color='#6A1B9A')
    ax.text((div_x+bx1)/2, by1-1.40, "WALLED • chemicals • fume extract", ha='center', va='center', fontsize=3.6, color='#6A1B9A', style='italic')
    # printing machines inside
    draw_machine(ax, div_x+0.5, nz_bot+0.7, 1.6, 2.6, "M5", "FLEXO PRINT", tall=False)
    draw_machine(ax, div_x+2.35, nz_bot+0.7, 1.6, 2.6, "M6", "FLEXO PRINT", tall=False)
    ax.text((div_x+bx1)/2, nz_bot+3.9, "own EAST entrance + lobby", ha='center', va='center', fontsize=3.6, color='#6A1B9A', weight='bold',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#6A1B9A"), zorder=8)
    # divider wall RAW|PRINT
    ax.plot([div_x, div_x], [nz_bot, by1-0.23], color=COLORS['print_wall'], lw=2.0, zorder=6)
    # south wall of north zone (with openings)
    ax.plot([bx0+0.23, bx0+2.0], [nz_bot, nz_bot], color=COLORS['wall_blue'], lw=2.0, zorder=6)
    ax.plot([bx0+3.6, div_x-0.6], [nz_bot, nz_bot], color=COLORS['wall_blue'], lw=2.0, zorder=6)
    ax.plot([div_x+0.6, div_x+2.0], [nz_bot, nz_bot], color=COLORS['print_wall'], lw=2.0, zorder=6)
    ax.plot([div_x+3.2, bx1-0.23], [nz_bot, nz_bot], color=COLORS['print_wall'], lw=2.0, zorder=6)
    ax.text(bx0+2.8, nz_bot-0.3, "1.6m", ha='center', va='top', fontsize=3.5, color='#333333')
    ax.text(div_x+2.6, nz_bot-0.3, "1.2m lobby", ha='center', va='top', fontsize=3.5, color='#6A1B9A')

    # ---------- MIDDLE HALL: machines ----------
    # central aisle
    aisle_w0, aisle_w1 = bx0+3.9, bx0+6.27
    ax.add_patch(Rectangle((aisle_w0, sz_top+0.1), aisle_w1-aisle_w0, nz_bot-sz_top-0.2, facecolor='#F1F8E9', edgecolor='#AED581', linewidth=0.6, linestyle=(0,(4,3)), zorder=1))
    ax.text((aisle_w0+aisle_w1)/2, (sz_top+nz_bot)/2, "CENTRAL AISLE\n2.37m", ha='center', va='center', fontsize=4, color='#558B2F', rotation=90, alpha=0.9, zorder=3)

    # West row: M1 mixing + M2-M4 extrusion towers (tall)
    # y positions from north to south: M1 near raw, then M2,M3,M4
    west_x = bx0+0.55
    west_w = 2.95
    machines_w = [
        (nz_bot-4.1, 3.4, "M1", "MIX / WEIGH", False),
        (nz_bot-8.3, 3.4, "M2", "EXTRUSION T1", True),
        (nz_bot-12.9, 3.4, "M3", "EXTRUSION T2", True),
        (nz_bot-17.5, 3.4, "M4", "EXTRUSION T3", True),
    ]
    for (yy, hh, lab, sub, tall) in machines_w:
        draw_machine(ax, west_x, yy, west_w, hh, lab, sub, tall=tall)
    # East row: M7-M9 cutting/sealing + M11 granulator/recycling
    east_x = bx1-0.55-2.95
    east_w = 2.95
    machines_e = [
        (nz_bot-4.1, 3.4, "M7", "CUT / SEAL 1", False),
        (nz_bot-8.3, 3.4, "M8", "CUT / SEAL 2", False),
        (nz_bot-12.9, 3.4, "M9", "CUT / SEAL 3", False),
        (nz_bot-17.5, 3.4, "M11", "GRANULATOR", False),
    ]
    for (yy, hh, lab, sub, tall) in machines_e:
        draw_machine(ax, east_x, yy, east_w, hh, lab, sub, tall=tall)

    # flow arrows N->S along aisle + branches
    # main spine
    spine_x = (aisle_w0+aisle_w1)/2
    for i in range(6):
        y_top = nz_bot - 1.2 - i*3.1
        y_bot = y_top - 1.9
        if y_bot < sz_top+0.8: break
        flow_arrow(ax, (spine_x, y_top), (spine_x, y_bot), color='#2E7D32', lw=1.5)
    # branches to machines (small)
    for (yy, hh, lab, sub, tall) in machines_w:
        flow_arrow(ax, (spine_x-0.4, yy+hh/2), (west_x+west_w+0.05, yy+hh/2), color='#66BB6A', lw=1.0)
    for (yy, hh, lab, sub, tall) in machines_e:
        flow_arrow(ax, (spine_x+0.4, yy+hh/2), (east_x-0.05, yy+hh/2), color='#66BB6A', lw=1.0)
    # raw -> M1, print -> M7 loop
    flow_arrow(ax, ((bx0+div_x)/2, nz_bot+0.4), (spine_x, nz_bot-1.0), color='#2E7D32', lw=1.5)
    flow_arrow(ax, ((div_x+bx1)/2, nz_bot+0.4), (east_x+east_w/2, nz_bot-0.7), color='#6A1B9A', lw=1.4)
    ax.text(spine_x+0.35, nz_bot-0.9, "PRINT→CUT", ha='left', va='center', fontsize=3.5, color='#6A1B9A', weight='bold', rotation=0,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#6A1B9A"), zorder=8)
    # south to QC/FG
    flow_arrow(ax, (spine_x, sz_top+1.6), ((bx0+mid_x)/2+0.5, sz_top-0.4), color='#2E7D32', lw=1.5)
    flow_arrow(ax, (spine_x+0.3, sz_top+1.2), (mid_x+1.5, sz_top-0.4), color='#1565C0', lw=1.5)
    ax.text(spine_x-1.6, sz_top+0.9, "TO QC", ha='center', va='center', fontsize=3.8, weight='bold', color='#00796B',
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#00796B"))
    ax.text(spine_x+1.7, sz_top+0.7, "TO FG", ha='center', va='center', fontsize=3.8, weight='bold', color='#1565C0',
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#1565C0"))

    # ---------- DOORS / ENTRANCES ----------
    # E1 WEST to RAW (roller 2.4 + personnel)
    e1y = by1 - 3.0
    # opening in wall: white gap
    ax.add_patch(Rectangle((bx0-0.12, e1y-1.2), 0.35, 2.4, facecolor='white', edgecolor='none', zorder=7))
    draw_roller(ax, bx0-0.08, e1y-1.2, 0.28, 2.4, horizontal=False)
    ax.text(bx0-1.5, e1y, "E1\nRAW\nROLLER 2.4m", ha='center', va='center', fontsize=3.8, weight='bold', color='#1B5E20',
            bbox=dict(boxstyle="round,pad=0.2", fc="#E8F5E9", ec="#2E7D32"), zorder=9)
    # E2 WEST to QC
    e2y = rec_top + 2.2
    ax.add_patch(Rectangle((bx0-0.12, e2y-0.6), 0.35, 1.2, facecolor='white', edgecolor='none', zorder=7))
    draw_door_swing(ax, (bx0+0.1, e2y-0.6), 1.1, 0, 90, 90)
    ax.text(bx0-1.6, e2y, "E2\nQC ENTRY\n1.2m", ha='center', va='center', fontsize=3.8, weight='bold', color='#00695C',
            bbox=dict(boxstyle="round,pad=0.2", fc="#E0F2F1", ec="#00796B"), zorder=9)
    # E3 WEST to Reception (main)
    e3y = by0 + 2.2
    ax.add_patch(Rectangle((bx0-0.12, e3y-0.75), 0.35, 1.5, facecolor='white', edgecolor='none', zorder=7))
    draw_door_swing(ax, (bx0+0.1, e3y-0.75), 1.4, 0, 90, 90)
    # canopy
    ax.add_patch(Rectangle((bx0-1.3, e3y-1.0), 1.2, 2.0, facecolor='none', edgecolor='#F9A825', linewidth=0.8, linestyle=(0,(3,2)), zorder=6))
    ax.text(bx0-1.9, e3y+1.5, "E3  MAIN ENTRY\n1.5m + canopy", ha='center', va='center', fontsize=3.8, weight='bold', color='#E65100',
            bbox=dict(boxstyle="round,pad=0.2", fc="#FFF8E1", ec="#F9A825"), zorder=9)
    # E4 EAST to PRINTING (own entrance)
    e4y = by1 - 3.0
    ax.add_patch(Rectangle((bx1-0.23, e4y-0.6), 0.35, 1.2, facecolor='white', edgecolor='none', zorder=7))
    draw_door_swing(ax, (bx1-0.1, e4y+0.6), 1.1, 180, 270, 180)
    ax.text(bx1+1.7, e4y, "E4  PRINT ONLY\n1.2m + lobby", ha='center', va='center', fontsize=3.8, weight='bold', color='#6A1B9A',
            bbox=dict(boxstyle="round,pad=0.2", fc="#F3E5F5", ec="#7B1FA2"), zorder=9)
    # E5 SOUTH to FG dispatch (roller 2.5)
    e5x = mid_x + 2.2
    ax.add_patch(Rectangle((e5x-1.25, by0-0.12), 2.5, 0.35, facecolor='white', edgecolor='none', zorder=7))
    draw_roller(ax, e5x-1.25, by0-0.08, 2.5, 0.28, horizontal=True)
    ax.text(e5x, by0-1.7, "E5  DISPATCH  ROLLER 2.5m", ha='center', va='center', fontsize=4, weight='bold', color='#0D47A1',
            bbox=dict(boxstyle="round,pad=0.2", fc="#E3F2FD", ec="#1565C0"), zorder=9)
    # E6 SOUTH personnel to reception
    e6x = bx0 + 3.2
    ax.add_patch(Rectangle((e6x-0.5, by0-0.12), 1.0, 0.35, facecolor='white', edgecolor='none', zorder=7))
    draw_door_swing(ax, (e6x-0.5, by0+0.1), 0.95, 0, 90, 45)
    ax.text(e6x, by0-1.1, "E6  1.0m", ha='center', va='center', fontsize=3.5, color='#5D4037',
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#8D6E63"), zorder=9)
    # E7 EAST to hall (emergency/loading mid)
    e7y = by0 + 16.0
    ax.add_patch(Rectangle((bx1-0.23, e7y-0.6), 0.35, 1.2, facecolor='white', edgecolor='none', zorder=7))
    draw_door_swing(ax, (bx1-0.1, e7y-0.6), 1.1, 90, 180, 180)
    ax.text(bx1+1.4, e7y, "E7\nEXIT", ha='center', va='center', fontsize=3.5, weight='bold', color='#37474F',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#37474F"), zorder=9)

    # windows (high louvre) hints on walls
    for wy in [by0+12, by0+20, by0+28]:
        # west
        ax.add_patch(Rectangle((bx0-0.06, wy), 0.22, 1.8, facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=0.6, zorder=8))
        # east
        ax.add_patch(Rectangle((bx1-0.16, wy+3), 0.22, 1.8, facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=0.6, zorder=8))
    ax.text(bx1+1.4, by0+32, "HIGH\nLOUVRES", ha='center', va='center', fontsize=3.5, color='#0288D1')

    # dims
    dim_linear(ax, (bx0, by1), (bx1, by1), offset=2.2, text="10.17", fontsize=6, color=COLORS['wall_blue'])
    dim_linear(ax, (bx1, by0), (bx1, by1), offset=-2.4, text="39.40", fontsize=6, color=COLORS['wall_blue'])
    dim_linear(ax, (bx0, by0), (bx0, by0+9.4), offset=2.0, text="9.40 MEZZ ZONE", fontsize=5, color='#4A148C')
    dim_linear(ax, (bx0, by1-6.0), (bx0, by1), offset=2.0, text="6.00 N-ZONE", fontsize=5, color='#1B5E20')
    dim_linear(ax, (bx0, by0+9.4), (bx0, by1-6.0), offset=2.0, text="24.00 HALL", fontsize=5, color=COLORS['steel'])

    # section marks
    draw_section_mark(ax, (bx0+bx1)/2, by0-2.8, 'up', "A")
    ax.text((bx0+bx1)/2+0.8, by0-2.8, "A—A LONGITUDINAL (see A301)", ha='left', va='center', fontsize=4, color='#0F2A52')
    draw_section_mark(ax, bx1+2.9, by0+18.5, 'left', "B")
    ax.text(bx1+2.9, by0+17.2, "B—B CROSS", ha='center', va='top', fontsize=4, color='#0F2A52')

    draw_north(ax, 17.5, 40, s=1.1)

    # machine list panel (right)
    px, py = 15.2, 8
    ax.add_patch(Rectangle((px, py), 4.2, 28.5, facecolor='#FAFAFA', edgecolor='#0F2A52', linewidth=1.0, zorder=4))
    ax.add_patch(Rectangle((px, py+26.8), 4.2, 1.7, facecolor=COLORS['title_bg'], edgecolor='none', zorder=5))
    ax.text(px+2.1, py+27.65, "MACHINE / AREA LIST", ha='center', va='center', fontsize=5.5, weight='bold', color='white', zorder=6)
    sched = [
        ("M1", "Mixing / Weighing"),
        ("M2-M4", "Blown-film Extrusion"),
        ("", "Towers (H≈9m)"),
        ("M5-M6", "Flexo Printing (in"),
        ("", "walled room)"),
        ("M7-M9", "Cutting / Heat-seal"),
        ("M10", "QC test bench"),
        ("M11", "Recycling granulator"),
        ("", ""),
        ("1", "Raw Mat. Store"),
        ("2", "Mix / Extrude hall"),
        ("3", "Printing (walled)"),
        ("4", "Cut / Seal hall"),
        ("5", "QC Lab / Office"),
        ("6", "FG Store"),
        ("7", "Reception / Stair"),
        ("8", "Dispatch (S roller)"),
    ]
    for i, (k, v) in enumerate(sched):
        yy = py+25.8-i*1.05
        if k and not k[0].isdigit():
            ax.text(px+0.3, yy, k, ha='left', va='center', fontsize=4.2, weight='bold', color=COLORS['machine_red'])
        elif k:
            ax.add_patch(Circle((px+0.55, yy), 0.28, facecolor='#0F2A52', edgecolor='none', zorder=6))
            ax.text(px+0.55, yy, k, ha='center', va='center', fontsize=4, weight='bold', color='white', zorder=7)
        ax.text(px+1.25, yy, v, ha='left', va='center', fontsize=4.2, color='#212121')

    # flow legend bottom-right
    lx, ly = 15.2, 0.5
    ax.add_patch(Rectangle((lx, ly), 4.2, 6.5, facecolor='white', edgecolor='#2E7D32', linewidth=1.0, zorder=4))
    ax.text(lx+2.1, ly+6.0, "FLOW LEGEND", ha='center', va='center', fontsize=5.5, weight='bold', color='#2E7D32')
    flow_arrow(ax, (lx+0.5, ly+5.0), (lx+1.5, ly+5.0), color='#2E7D32', lw=1.5)
    ax.text(lx+1.7, ly+5.0, "Material N→S", ha='left', va='center', fontsize=4.2, color='#212121')
    flow_arrow(ax, (lx+0.5, ly+4.2), (lx+1.5, ly+4.2), color='#6A1B9A', lw=1.4)
    ax.text(lx+1.7, ly+4.2, "Print → Cut", ha='left', va='center', fontsize=4.2, color='#212121')
    ax.add_patch(Rectangle((lx+0.5, ly+3.2), 1.0, 0.5, facecolor=COLORS['machine_fill'], edgecolor=COLORS['machine_red'], linewidth=1.0, zorder=5))
    ax.text(lx+1.7, ly+3.45, "Machine (red = NOT wall)", ha='left', va='center', fontsize=4.2, color='#212121')
    ax.add_patch(Rectangle((lx+0.5, ly+2.3), 1.0, 0.5, facecolor=COLORS['print_fill'], edgecolor=COLORS['print_wall'], linewidth=1.2, zorder=5))
    ax.text(lx+1.7, ly+2.55, "Walled room", ha='left', va='center', fontsize=4.2, color='#212121')
    ax.add_patch(Rectangle((lx+0.5, ly+1.4), 1.0, 0.5, facecolor=COLORS['steel'], edgecolor='white', linewidth=0.5, zorder=5))
    ax.text(lx+1.7, ly+1.65, "Steel stanchion", ha='left', va='center', fontsize=4.2, color='#212121')
    ax.text(lx+2.1, ly+0.6, "E1-E7 = entrances", ha='center', va='center', fontsize=4, style='italic', color='#555555')

    bring_text_to_front(ax)
    save_sheet(fig, "A102_ground_floor")
    plt.close(fig)

if __name__ == "__main__":
    build()
