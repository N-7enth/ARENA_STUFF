# A201 - Elevations (Front/Rear/Sides)
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import numpy as np
from arch_lib import *

W = 10.17
EAVES = 8.0
RIDGE = 12.0
L = 39.40

def wall_hatch(ax, ox, oy, w, h):
    # block to 1.2 + cladding above: show horizontal line at 1.2 + vertical seams
    ax.plot([ox, ox+w], [oy+1.2, oy+1.2], color='#78909C', lw=0.6, linestyle=(0,(4,3)), zorder=5)
    ax.text(ox+w/2, oy+0.6, "BLOCK 1.2m", ha='center', va='center', fontsize=3.2, color='#78909C', style='italic', zorder=6)
    ax.text(ox+w/2, oy+(1.2+h)/2 if h>4 else oy+2.5, "METAL CLADDING", ha='center', va='center', fontsize=3.5, color='#546E7A', alpha=0.7, zorder=5)
    # vertical seams every ~1m
    for xx in np.arange(ox+1, ox+w, 1.0):
        ax.plot([xx, xx], [oy+1.2, oy+h], color='#B0BEC5', lw=0.25, zorder=4)

def draw_gable(ax, ox, oy, w, eaves, ridge, title, subtitle, doors, windows, louvres, show_gate=False):
    # ground
    ax.plot([ox-2, ox+w+2], [oy, oy], color='#212121', lw=1.2, zorder=6)
    # hatch ground
    for xx in np.arange(ox-2, ox+w+2, 0.8):
        ax.plot([xx, xx-0.4], [oy, oy-0.4], color='#9E9E9E', lw=0.5, zorder=5)
    # walls
    ax.add_patch(Rectangle((ox, oy), w, eaves, facecolor='#ECEFF1', edgecolor='#0F2A52', linewidth=1.4, zorder=4))
    wall_hatch(ax, ox, oy, w, eaves)
    # gable triangle (above eaves to ridge)
    cx = ox+w/2
    ax.add_patch(Polygon([(ox, oy+eaves), (cx, oy+ridge), (ox+w, oy+eaves)], closed=True, facecolor='#CFD8DC', edgecolor='#0F2A52', linewidth=1.4, zorder=4))
    # roof edge (barge) overhang
    ax.plot([ox-0.4, cx], [oy+eaves-0.1, oy+ridge+0.15], color='#0F2A52', lw=1.8, zorder=6)
    ax.plot([cx, ox+w+0.4], [oy+ridge+0.15, oy+eaves-0.1], color='#0F2A52', lw=1.8, zorder=6)
    # ridge cap
    ax.add_patch(Rectangle((cx-0.35, oy+ridge-0.05), 0.7, 0.35, facecolor='#37474F', edgecolor='white', linewidth=0.5, zorder=7))
    # doors
    for (dx, dw, dh, label, is_roller) in doors:
        if is_roller:
            draw_roller(ax, ox+dx, oy, dw, dh, horizontal=True)
        else:
            ax.add_patch(Rectangle((ox+dx, oy), dw, dh, facecolor='#90A4AE', edgecolor='#263238', linewidth=1.0, zorder=6))
        ax.text(ox+dx+dw/2, oy+dh+0.25, label, ha='center', va='bottom', fontsize=3.4, color='#263238', weight='bold', zorder=8,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#78909C"))
    # windows (mezz level)
    for (wx, ww, wy, wh) in windows:
        ax.add_patch(Rectangle((ox+wx, oy+wy), ww, wh, facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=0.9, zorder=6))
        ax.plot([ox+wx+ww/2, ox+wx+ww/2], [oy+wy, oy+wy+wh], color='#0288D1', lw=0.6, zorder=7)
    # louvres (high)
    for (lx, lw, ly) in louvres:
        ax.add_patch(Rectangle((ox+lx, oy+ly), lw, 0.9, facecolor='#B0BEC5', edgecolor='#455A64', linewidth=0.7, zorder=6))
        for i in range(3):
            ax.plot([ox+lx, ox+lx+lw], [oy+ly+0.22+i*0.22, oy+ly+0.22+i*0.22], color='#455A64', lw=0.4, zorder=7)
    # gable vent
    ax.add_patch(Circle((cx, oy+eaves+1.5), 0.5, facecolor='#78909C', edgecolor='#37474F', linewidth=0.8, zorder=6))
    ax.text(cx, oy+eaves+1.5, "VENT", ha='center', va='center', fontsize=3.0, color='white', weight='bold', zorder=7)
    # levels (right side)
    for lev, lab in [(0, "+0.00"), (4.0, "+4.00 MEZZ"), (8.0, "+8.00 EAVES"), (12.0, "+12.00 RIDGE")]:
        ax.plot([ox+w, ox+w+1.2], [oy+lev, oy+lev], color='#0F2A52', lw=0.7, zorder=6)
        ax.add_patch(Polygon([(ox+w+1.2, oy+lev), (ox+w+1.5, oy+lev+0.18), (ox+w+1.5, oy+lev-0.18)], closed=True, facecolor='#0F2A52', edgecolor='none', zorder=7))
        ax.text(ox+w+1.7, oy+lev, lab, ha='left', va='center', fontsize=3.4, color='#0F2A52', zorder=8)
    # width dim
    dim_linear(ax, (ox, oy), (ox+w, oy), offset=-1.0, text=f"{w:.2f}", fontsize=5, color='#0F2A52')
    # title
    ax.text(ox+w/2, oy-2.0, title, ha='center', va='top', fontsize=6.5, weight='bold', color='#0F2A52')
    ax.text(ox+w/2, oy-2.7, subtitle, ha='center', va='top', fontsize=4, color='#555555', style='italic')

    if show_gate:
        # foreground gate block (simplified, in front of building, lower)
        # show as 3.0 high block with tanks above, spanning wider than building? Actually gate block 11.2 wide, building 10.17, similar. Show offset to indicate foreground.
        gx, gw2 = ox-1.5, w+3.0
        gy = oy
        ax.add_patch(Rectangle((gx, gy), gw2, 3.0, facecolor='#FFF8E1', edgecolor='#F57F17', linewidth=1.2, zorder=8))
        ax.text(gx+gw2/2, gy+1.5, "GATE / SECURITY / POWER  (foreground, @+3.0 deck + tanks)", ha='center', va='center', fontsize=3.6, weight='bold', color='#5D4037', zorder=9,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#F57F17", alpha=0.95))
        # deck + tanks
        ax.plot([gx, gx+gw2], [gy+3.0, gy+3.0], color='#4E342E', lw=1.6, zorder=9)
        for tx in [gx+2.5, gx+4.5]:
            ax.add_patch(Rectangle((tx-0.5, gy+3.0), 1.0, 1.0, facecolor='#0288D1', edgecolor='#01579B', linewidth=0.8, zorder=9))
        ax.text(gx+3.5, gy+4.3, "2× 2000L", ha='center', va='bottom', fontsize=3.4, color='#01579B', weight='bold', zorder=9)
        # gate opening
        ax.add_patch(Rectangle((gx+0.3, gy), 2.2, 2.2, facecolor='#37474F', edgecolor='black', linewidth=0.8, zorder=9))
        ax.text(gx+1.4, gy+0.4, "GATE", ha='center', va='center', fontsize=3.4, weight='bold', color='white', zorder=10)

def draw_side(ax, ox, oy, length, eaves, ridge, title, subtitle, entrances, is_west=True):
    # ground
    ax.plot([ox-1.5, ox+length+1.5], [oy, oy], color='#212121', lw=1.2, zorder=6)
    for xx in np.arange(ox-1.5, ox+length+1.5, 1.2):
        ax.plot([xx, xx-0.4], [oy, oy-0.4], color='#9E9E9E', lw=0.5, zorder=5)
    # wall
    ax.add_patch(Rectangle((ox, oy), length, eaves, facecolor='#ECEFF1', edgecolor='#0F2A52', linewidth=1.4, zorder=4))
    wall_hatch(ax, ox, oy, length, eaves)
    # stanchion grid ticks (bottom + top)
    bays = [3.4,6,6,6,6,6,6]  # from south (left in elevation? Let's put south left, north right for both W/E? For W viewed from W looking E, south is left? Facing east, south is right? Hmm orientation: Looking east (W elev), north is left? Actually facing east, north is to your left? No: facing east, north is left? Compass: N up, E right. Facing E (right), N (up) is to your left? Visualize: standard map N up, E right. Observer facing E (looking right). North (up) is to observer's left? If you face right (E), up (N) is to your left? Turn 90° clockwise from facing N to facing E: your left (was W) becomes N? Hmm confusing. Let's just label S left, N right for both sides and note viewing direction. Acceptable for preliminary.
    # We'll draw south at left (x=ox) for both.
    gx = ox
    grid_xs = [gx]
    for b in bays:
        gx += b
        grid_xs.append(gx)
    for i, gxx in enumerate(grid_xs):
        ax.plot([gxx, gxx], [oy, oy+eaves], color=COLORS['steel'], lw=0.5, linestyle=(0,(4,3)), alpha=0.6, zorder=5)
        ax.add_patch(Rectangle((gxx-0.15, oy+eaves-0.3), 0.3, 0.3, facecolor=COLORS['steel'], edgecolor='white', linewidth=0.4, zorder=7))
        if i < len(grid_xs)-1:
            mid = (gxx+grid_xs[i+1])/2 if i+1 < len(grid_xs) else gxx
            # bay dim (top)
            pass
        # bubbles bottom
        draw_grid_bubble(ax, gxx, oy-0.9, f"{i+1}", r=0.32)
    ax.text(ox-0.5, oy-0.9, "S", ha='right', va='center', fontsize=4, weight='bold', color='#0F2A52')
    ax.text(ox+length+0.5, oy-0.9, "N", ha='left', va='center', fontsize=4, weight='bold', color='#0F2A52')
    # roof band (slope seen from side): from eaves (front) to ridge (back, higher). Show as 4m band with skylight strips as horizontal bands.
    # eaves line (front edge)
    ax.plot([ox-0.4, ox+length+0.4], [oy+eaves, oy+eaves], color='#0F2A52', lw=2.0, zorder=7)
    # ridge line (behind, higher)
    ax.plot([ox-0.4, ox+length+0.4], [oy+ridge, oy+ridge], color='#0F2A52', lw=1.4, linestyle=(0,(6,2)), zorder=6)
    # slope fill between
    ax.add_patch(Polygon([(ox-0.4,oy+eaves),(ox+length+0.4,oy+eaves),(ox+length+0.4,oy+ridge),(ox-0.4,oy+ridge)], closed=True, facecolor='#8FA8C8', edgecolor='none', alpha=0.85, zorder=3))
    # skylight bands (2 horizontal translucent bands at 1/3,2/3 height)
    for frac in [0.33, 0.66]:
        yy = oy+eaves + (ridge-eaves)*frac
        ax.add_patch(Rectangle((ox, yy-0.35), length, 0.7, facecolor=COLORS['skylight'], edgecolor='#0288D1', linewidth=0.7, zorder=6))
    ax.text(ox+length/2, oy+ridge+0.25, "SKYLIGHTS ×2 + RIDGE VENTS ×6 (behind)", ha='center', va='bottom', fontsize=3.6, color='#0F2A52', style='italic',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#0F2A52"), zorder=8)
    # ridge vents (small rects on ridge line)
    vent_xs = [ox+6.4, ox+12.4, ox+18.4, ox+24.4, ox+30.4, ox+36.4]
    # our ox is south (y=0 in plan). Plan south y=0, north y=39.4. Vent plan y = by0+6.4 etc. Map plan y -> elevation x: x = ox + plan_y (south left). So vents at ox+6.4 etc. Good.
    for vx in vent_xs:
        ax.add_patch(Rectangle((vx-0.5, oy+ridge-0.3), 1.0, 0.6, facecolor='#37474F', edgecolor='white', linewidth=0.6, zorder=8))
    # gutters
    ax.plot([ox-0.4, ox+length+0.4], [oy+eaves-0.15, oy+eaves-0.15], color='#263238', lw=1.4, zorder=7)
    # downpipes
    for gxx in grid_xs[1:-1]:
        ax.plot([gxx, gxx], [oy, oy+eaves-0.15], color='#455A64', lw=0.8, zorder=6)
    # entrances (doors along wall)
    # entrances: list of (dist_from_south, width, height, label, is_roller)
    for (d, dw, dh, label, is_roller) in entrances:
        ex = ox + d - dw/2
        if is_roller:
            draw_roller(ax, ex, oy, dw, dh, horizontal=True)
        else:
            ax.add_patch(Rectangle((ex, oy), dw, dh, facecolor='#90A4AE', edgecolor='#263238', linewidth=1.0, zorder=7))
        ax.text(ex+dw/2, oy+dh+0.3, label, ha='center', va='bottom', fontsize=3.4, weight='bold', color='#263238', zorder=8,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#78909C"))
    # high louvres (between entrances)
    for d in [8, 14, 20, 26, 32]:
        ax.add_patch(Rectangle((ox+d-0.9, oy+5.5), 1.8, 0.9, facecolor='#B0BEC5', edgecolor='#455A64', linewidth=0.6, zorder=6))
    ax.text(ox+length-2, oy+5.0, "HIGH LOUVRES", ha='center', va='top', fontsize=3.2, color='#455A64', style='italic')
    # mezz windows (south end)
    for d in [1.5, 3.5, 6.5, 8.0]:
        if d < 9.4:
            ax.add_patch(Rectangle((ox+d-0.6, oy+4.8), 1.2, 1.2, facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=0.7, zorder=7))
    # levels left
    for lev, lab in [(0,"+0.00"),(4.0,"+4.00"),(8.0,"+8.00"),(12.0,"+12.00")]:
        ax.plot([ox-1.5, ox-0.4], [oy+lev, oy+lev], color='#0F2A52', lw=0.7, zorder=6)
        ax.text(ox-1.7, oy+lev, lab, ha='right', va='center', fontsize=3.4, color='#0F2A52', zorder=8)
    # length dim
    dim_linear(ax, (ox, oy), (ox+length, oy), offset=-2.2, text=f"{length:.2f}", fontsize=5.5, color='#0F2A52')
    # title
    ax.text(ox+length/2, oy-3.4, title, ha='center', va='top', fontsize=6.5, weight='bold', color='#0F2A52')
    ax.text(ox+length/2, oy-4.2, subtitle, ha='center', va='top', fontsize=4, color='#555555', style='italic')

def build():
    fig, ax = setup_sheet(figsize=(16.8, 11.9))
    ax.set_xlim(0, 62)
    ax.set_ylim(0, 45)
    draw_border(ax, 0, 0, 62, 45)
    draw_title_block(ax, 30, 0.7, 31, "A201", "ELEVATIONS  •  FRONT / REAR / SIDES", "1:100")

    ax.text(31, 43.3, "ELEVATIONS  —  EAVES +8.00m  •  RIDGE +12.00m  •  38° GABLE", ha='center', va='center', fontsize=11, weight='bold', color='#0F2A52')
    ax.text(31, 42.3, "Block 1.2m + metal cladding to eaves  •  Skylights + ridge vents  •  West: 3 entrances (E1/E2/E3)  •  East: print entry (E4) + fire stair", ha='center', va='center', fontsize=5.5, color='#333333')

    # WEST (top-left, long)
    # entrances: E3 (south, d=2.2 from S), E2 (d=7.2), E1 (north, d=36.4)
    draw_side(ax, 2, 28, L, EAVES, RIDGE,
              "LEFT / WEST ELEVATION  (from driveway — 4.0m setback)",
              "S (left) → N (right)  •  E3 Main + E2 QC + E1 Raw roller  •  Grid 1–8 @6.0m",
              entrances=[(2.2, 1.5, 2.4, "E3 MAIN 1.5m", False),
                         (7.2, 1.2, 2.2, "E2 QC 1.2m", False),
                         (36.4, 2.4, 3.0, "E1 RAW 2.4m", True)],
              is_west=True)
    # EAST (bottom-left, long)
    draw_side(ax, 2, 9, L, EAVES, RIDGE,
              "RIGHT / EAST ELEVATION  (from 2.0m setback)",
              "S (left) → N (right)  •  E4 Print-only + E7 Exit + fire-escape stair",
              entrances=[(8.5, 0.9, 2.2, "FIRE EXIT", False),
                         (16.0, 1.2, 2.2, "E7 EXIT", False),
                         (36.4, 1.2, 2.2, "E4 PRINT 1.2m", False)],
              is_west=False)
    # fire stair hint on east (south end, external)
    # external stair at plan y 1.0-8.5 (dist from S), height 0-4.0
    ex0 = 2
    sx0, sx1 = ex0+1.0, ex0+8.5
    ax.add_patch(Polygon([(sx0,9),(sx1,9),(sx1,13),(sx0,13)], closed=True, facecolor='none', edgecolor='#37474F', linewidth=1.0, linestyle=(0,(3,2)), zorder=7))
    ax.plot([sx0, sx1], [9, 13], color='#37474F', lw=1.2, zorder=8)
    ax.text((sx0+sx1)/2, 13.3, "EXT. STEEL STAIR (fire escape, see A103)", ha='center', va='bottom', fontsize=3.4, color='#37474F', style='italic',
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#78909C"), zorder=9)

    # FRONT / SOUTH (top-right, gable) with gate foreground
    draw_gable(ax, 46, 28, W, EAVES, RIDGE,
               "FRONT / SOUTH",
               "from Main Road (gate in foreground)",
               doors=[(3.2-1.25, 2.5, 3.0, "E5 DISPATCH 2.5m", True),
                      (1.0, 1.0, 2.2, "E6 1.0m", False)],
               windows=[(1.5, 1.4, 4.8, 1.2), (4.0, 1.4, 4.8, 1.2), (7.0, 1.4, 4.8, 1.2)],
               louvres=[(2.0, 2.0, 6.2), (6.2, 2.0, 6.2)],
               show_gate=True)
    # REAR / NORTH (bottom-right, gable)
    draw_gable(ax, 46, 9, W, EAVES, RIDGE,
               "REAR / NORTH",
               "from rear setback (borehole W)",
               doors=[(1.2, 1.0, 2.2, "STORE", False)],
               windows=[],
               louvres=[(1.5, 2.0, 6.2), (4.0, 2.0, 6.2), (6.5, 2.0, 6.2)],
               show_gate=False)
    # borehole hint
    ax.text(44.5, 9.5, "BH→", ha='right', va='center', fontsize=3.5, color='#01579B', weight='bold')
    # print extract on rear?
    ax.add_patch(Circle((46+8.2, 9+6.5), 0.35, facecolor='#6A1B9A', edgecolor='white', linewidth=0.7, zorder=8))
    ax.text(46+8.2, 9+7.2, "PRINT EX", ha='center', va='bottom', fontsize=3.2, color='#6A1B9A', weight='bold')

    # material legend (bottom-left)
    lx, ly = 2, 0.7
    ax.add_patch(Rectangle((lx, ly), 26, 4.2, facecolor='#F5F7FA', edgecolor='#0F2A52', linewidth=1.0, zorder=4))
    ax.text(lx+13, ly+3.7, "FINISHES & LEVELS", ha='center', va='center', fontsize=5.5, weight='bold', color='#0F2A52', zorder=6)
    ax.text(lx+0.5, ly+2.9, "• Walls: 150/215 block to 1.2m + insulated box-profile cladding to +8.0m.  • Roof: 0.55 Al-Zn sheets @38° + skylights + vents.", ha='left', va='center', fontsize=4, color='#212121', zorder=6)
    ax.text(lx+0.5, ly+2.1, "• Doors: steel personnel + roller shutters (see key E1–E7).  • Windows: alum. sliding (offices) + louvres (hall, high).", ha='left', va='center', fontsize=4, color='#212121', zorder=6)
    ax.text(lx+0.5, ly+1.3, "• Levels: +0.00 FFL (power-float) • +3.00 gate deck • +4.00 mezz • +8.00 eaves • +12.00 ridge.  • Colours: blues/greys (TBC).", ha='left', va='center', fontsize=4, color='#212121', zorder=6)

    bring_text_to_front(ax)
    save_sheet(fig, "A201_elevations")
    plt.close(fig)

if __name__ == "__main__":
    build()
