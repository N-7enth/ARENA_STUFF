# A103 - Mezzanine Floor Plan @+4.0m
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import numpy as np
from arch_lib import *

def build():
    fig, ax = setup_sheet(figsize=(11.9, 16.8))
    ax.set_xlim(-7, 20)
    ax.set_ylim(-7.5, 47)
    draw_border(ax, -7, -7.5, 27, 54.5)
    draw_title_block(ax, 0.5, -6.8, 18.5, "A103", "MEZZANINE FLOOR PLAN @+4.0m  •  OFFICES + UTILITIES", "1:100")

    ax.text(6.5, 45.3, "MEZZANINE FLOOR PLAN  @+4.00m  —  OVER SOUTH 9.40m  (95.6 m²)", ha='center', va='center', fontsize=11, weight='bold', color='#0F2A52')
    ax.text(6.5, 44.1, "Decked RC slab on steel beams  •  Offices + Staff + WCs + Utilities  •  Gallery overlooking hall  •  External fire-escape stair (E)", ha='center', va='center', fontsize=5.5, color='#333333')

    bx0, by0 = 1.5, 0.0
    bw, bl = 10.17, 39.40
    bx1, by1 = bx0+bw, by0+bl
    mz_top = by0+9.4

    # outer walls (same as ground, but north part is void)
    ax.add_patch(Rectangle((bx0, by0), bw, bl, facecolor='white', edgecolor=COLORS['wall_blue'], linewidth=2.4, zorder=3))
    ax.add_patch(Rectangle((bx0+0.23, by0+0.23), bw-0.46, bl-0.46, facecolor='none', edgecolor=COLORS['wall_blue'], linewidth=0.6, zorder=4))

    # grid (same)
    bays = [3.4,6,6,6,6,6,6]
    grid_ys = [by0]
    yy=by0
    for b in bays:
        yy+=b; grid_ys.append(yy)
    for i, gy in enumerate(grid_ys):
        ax.plot([bx0,bx1],[gy,gy], color=COLORS['steel'], lw=0.35, linestyle=(0,(4,3)), alpha=0.45, zorder=2)
        for gx in [bx0,bx1]:
            ax.add_patch(Rectangle((gx-0.22,gy-0.22),0.44,0.44, facecolor=COLORS['steel'], edgecolor='white', linewidth=0.6, zorder=8))
        draw_grid_bubble(ax, bx0-0.85, gy, f"{i+1}", r=0.32)
    draw_grid_bubble(ax, bx0, by0-0.85, "A", r=0.32)
    draw_grid_bubble(ax, bx1, by0-0.85, "B", r=0.32)

    # ---- VOID (north of mezz) ----
    ax.add_patch(Rectangle((bx0+0.23, mz_top+0.1), bw-0.46, by1-mz_top-0.33, facecolor='#F5F5F5', edgecolor='#9E9E9E', linewidth=0.8, linestyle=(0,(5,4)), zorder=2))
    # diagonal cross to show void
    for xx in np.arange(bx0+1, bx1-0.5, 2.0):
        ax.plot([xx, xx+1.2], [mz_top+1, mz_top+2.2], color='#BDBDBD', lw=0.5, zorder=3)
    ax.text((bx0+bx1)/2, (mz_top+by1)/2+4, "OPEN TO BELOW", ha='center', va='center', fontsize=10, weight='bold', color='#9E9E9E', alpha=0.9, rotation=90, zorder=3)
    ax.text((bx0+bx1)/2, (mz_top+by1)/2-2, "Production hall below\n(Eaves +8.0m • Extrusion towers H≈9m)\nRoof + skylights above (see A104)", ha='center', va='center', fontsize=5, color='#616161', style='italic', zorder=4,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#9E9E9E"))
    # north zone walls below (dashed, seen from above? Actually raw/print rooms full height? Show as below)
    # Indicate printing room extends full height? No, printing single storey with own ceiling? Note: printing room height 4m with ceiling + extract duct to roof. Show dashed.
    nz_bot = by1-6.0
    div_x = bx0+5.50
    ax.add_patch(Rectangle((bx0+0.23, nz_bot), div_x-bx0-0.46, 6.0-0.46, facecolor='none', edgecolor='#A5D6A7', linewidth=0.7, linestyle=(0,(3,3)), zorder=4))
    ax.text((bx0+div_x)/2, by1-1.0, "RAW STORE BELOW", ha='center', va='center', fontsize=4, color='#2E7D32', style='italic', zorder=5)
    ax.add_patch(Rectangle((div_x, nz_bot), bx1-div_x-0.23, 6.0-0.46, facecolor='none', edgecolor='#CE93D8', linewidth=0.7, linestyle=(0,(3,3)), zorder=4))
    ax.text((div_x+bx1)/2, by1-1.0, "PRINTING BELOW\n(+ extract duct to roof)", ha='center', va='center', fontsize=4, color='#6A1B9A', style='italic', zorder=5)

    # ---- MEZZ SLAB ----
    # slab edge + beams
    ax.add_patch(Rectangle((bx0+0.23, by0+0.23), bw-0.46, 9.4-0.46, facecolor='#FFF8E1', edgecolor='#FF8F00', linewidth=1.4, zorder=4))
    ax.text(bx0+bw/2, by0+0.55, "150mm RC SLAB on steel beams  •  FFL +4.00m  •  Live: 3.0 kN/m² (offices) / 5.0 (utilities)", ha='center', va='center', fontsize=3.6, color='#5D4037', style='italic', zorder=6,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#FFB300", alpha=0.95))
    # beams (dashed E-W)
    for by in [by0+4.0, by0+8.0]:
        ax.plot([bx0+0.3, bx1-0.3], [by, by], color='#8D6E63', lw=0.8, linestyle=(0,(6,3)), zorder=5)
        ax.text(bx1-0.5, by+0.15, "UB", ha='center', va='bottom', fontsize=3.5, color='#8D6E63', style='italic', zorder=6)

    # partitions:
    # South band y0-4.0: Lobby/Stair (W 0-2.8), Admin (2.8-5.8), MD (5.8-10.17)
    # Mid band y4.0-8.0: Staff (W 0-3.5), WC/Store (3.5-6.0), Utilities (6.0-10.17)
    # Gallery y8.0-9.4 full width
    # Walls:
    # Horizontal walls at y=4.0 and y=8.0 (with openings)
    # y=4.0: openings: lobby->staff? door 0.9 at x~1.5, admin->WC? etc.
    ax.plot([bx0+0.23, bx0+1.0], [by0+4.0, by0+4.0], color='#5D4037', lw=1.2, zorder=6)
    ax.plot([bx0+1.9, bx0+2.8], [by0+4.0, by0+4.0], color='#5D4037', lw=1.2, zorder=6)
    ax.plot([bx0+3.7, bx1-0.23], [by0+4.0, by0+4.0], color='#5D4037', lw=1.2, zorder=6)
    # y=8.0: gallery partition with 2 openings
    ax.plot([bx0+0.23, bx0+2.0], [by0+8.0, by0+8.0], color='#5D4037', lw=1.2, zorder=6)
    ax.plot([bx0+3.0, bx0+7.0], [by0+8.0, by0+8.0], color='#5D4037', lw=1.2, zorder=6)
    ax.plot([bx0+8.0, bx1-0.23], [by0+8.0, by0+8.0], color='#5D4037', lw=1.2, zorder=6)
    # Vertical walls south band
    ax.plot([bx0+2.8, bx0+2.8], [by0+0.23, by0+4.0], color='#5D4037', lw=1.2, zorder=6)
    ax.plot([bx0+5.8, bx0+5.8], [by0+0.23, by0+4.0], color='#5D4037', lw=1.2, zorder=6)
    # Vertical mid band
    ax.plot([bx0+3.5, bx0+3.5], [by0+4.0, by0+8.0], color='#5D4037', lw=1.2, zorder=6)
    ax.plot([bx0+6.0, bx0+6.0], [by0+4.0, by0+8.0], color='#5D4037', lw=1.2, zorder=6)
    # WC subdivisions: at x3.5-6.0, y4.0-8.0: split: WC M (3.5-4.75,4.0-6.0), WC F (4.75-6.0,4.0-6.0), Store (3.5-6.0,6.0-8.0)
    ax.plot([bx0+3.5, bx0+6.0], [by0+6.0, by0+6.0], color='#0288D1', lw=1.0, zorder=6)
    ax.plot([bx0+4.75, bx0+4.75], [by0+4.0, by0+6.0], color='#0288D1', lw=1.0, zorder=6)

    # Room labels + furniture
    # Lobby/Stair
    ax.text(bx0+1.5, by0+3.3, "LOBBY", ha='center', va='center', fontsize=5, weight='bold', color='#4E342E', zorder=7)
    ax.text(bx0+1.5, by0+2.9, "stair arrival", ha='center', va='center', fontsize=3.6, color='#795548', zorder=7)
    # stairwell opening (same as ground stair + landing)
    # ground stair at bx0+0.5..1.9 (w1.4), y0.6..3.2 (h2.6). At mezz, opening with railing.
    ax.add_patch(Rectangle((bx0+0.5, by0+0.6), 1.4, 2.6, facecolor='white', edgecolor='#4E342E', linewidth=1.0, zorder=6))
    # stair down arrow (reverse)
    draw_stair(ax, bx0+0.5, by0+0.6, 1.4, 2.6, direction='down', n_steps=9)
    ax.text(bx0+1.2, by0+0.35, "", ha='center', va='top', fontsize=3.5, color='#4E342E')
    # railing around opening (north + east)
    ax.plot([bx0+0.5, bx0+1.9], [by0+3.2, by0+3.2], color='#D32F2F', lw=1.4, linestyle=(0,(4,2)), zorder=8)
    ax.plot([bx0+1.9, bx0+1.9], [by0+0.6, by0+3.2], color='#D32F2F', lw=1.4, linestyle=(0,(4,2)), zorder=8)
    ax.text(bx0+2.15, by0+1.9, "RAIL", ha='left', va='center', fontsize=3.2, color='#D32F2F', rotation=90, zorder=8)

    # Admin office
    ax.text(bx0+4.3, by0+3.2, "OFFICE 2", ha='center', va='center', fontsize=5.5, weight='bold', color='#1A237E', zorder=7)
    ax.text(bx0+4.3, by0+2.7, "Admin / QA", ha='center', va='center', fontsize=4, color='#3949AB', zorder=7)
    ax.text(bx0+4.3, by0+2.25, "≈12 m²", ha='center', va='center', fontsize=3.6, color='#616161', zorder=7)
    # desks
    for dx in [bx0+3.1, bx0+4.4]:
        ax.add_patch(Rectangle((dx, by0+0.9), 1.1, 0.6, facecolor='white', edgecolor='#1A237E', linewidth=0.7, zorder=7))
    # door Admin<->Lobby (in wall x=2.8)
    draw_door_swing(ax, (bx0+2.8, by0+1.8), 0.85, 270, 360, 0)

    # MD office
    ax.text(bx0+8.0, by0+3.2, "OFFICE 1 (MD)", ha='center', va='center', fontsize=5.5, weight='bold', color='#1A237E', zorder=7)
    ax.text(bx0+8.0, by0+2.7, "with S + E windows", ha='center', va='center', fontsize=3.8, color='#3949AB', zorder=7)
    ax.text(bx0+8.0, by0+2.25, "≈17.5 m²", ha='center', va='center', fontsize=3.6, color='#616161', zorder=7)
    ax.add_patch(Rectangle((bx0+7.3, by0+0.9), 1.6, 0.8, facecolor='white', edgecolor='#1A237E', linewidth=0.7, zorder=7))
    ax.text(bx0+8.1, by0+1.3, "EXEC DESK", ha='center', va='center', fontsize=3.2, color='#1A237E', zorder=8)
    # door MD<->Admin? via lobby? Put door in wall x=5.8
    draw_door_swing(ax, (bx0+5.8, by0+2.2), 0.85, 90, 180, 180)

    # Staff
    ax.text(bx0+1.9, by0+7.3, "STAFF / CANTEEN", ha='center', va='center', fontsize=5, weight='bold', color='#33691E', zorder=7)
    ax.text(bx0+1.9, by0+6.85, "≈14 m² + lockers", ha='center', va='center', fontsize=3.6, color='#558B2F', zorder=7)
    # tables
    ax.add_patch(Rectangle((bx0+0.7, by0+5.0), 1.2, 0.8, facecolor='white', edgecolor='#33691E', linewidth=0.7, zorder=7))
    ax.add_patch(Rectangle((bx0+2.0, by0+5.0), 1.2, 0.8, facecolor='white', edgecolor='#33691E', linewidth=0.7, zorder=7))
    ax.text(bx0+1.9, by0+5.4, "TABLES", ha='center', va='center', fontsize=3.2, color='#33691E', zorder=8)
    # lockers along west wall
    for i in range(3):
        ax.add_patch(Rectangle((bx0+0.35, by0+6.2+i*0.45), 0.5, 0.4, facecolor='#DCEDC8', edgecolor='#33691E', linewidth=0.5, zorder=7))

    # WCs
    ax.text(bx0+4.12, by0+5.0, "WC-M", ha='center', va='center', fontsize=4, weight='bold', color='#01579B', zorder=7)
    ax.add_patch(Rectangle((bx0+3.7, by0+4.3), 0.5, 0.7, facecolor='white', edgecolor='#01579B', linewidth=0.6, zorder=7))  # WC pan
    ax.text(bx0+5.37, by0+5.0, "WC-F", ha='center', va='center', fontsize=4, weight='bold', color='#880E4F', zorder=7)
    ax.add_patch(Rectangle((bx0+5.0, by0+4.3), 0.5, 0.7, facecolor='white', edgecolor='#880E4F', linewidth=0.6, zorder=7))
    ax.text(bx0+4.75, by0+7.0, "STORE", ha='center', va='center', fontsize=4.5, weight='bold', color='#4E342E', zorder=7)
    ax.text(bx0+4.75, by0+6.55, "files / station.", ha='center', va='center', fontsize=3.4, color='#795548', zorder=7)

    # Utilities
    ax.text(bx0+8.1, by0+7.3, "UTILITIES", ha='center', va='center', fontsize=5.5, weight='bold', color='#BF360C', zorder=7)
    ax.text(bx0+8.1, by0+6.85, "electrical • UPS • data", ha='center', va='center', fontsize=3.6, color='#E65100', zorder=7)
    # panels
    for i in range(3):
        ax.add_patch(Rectangle((bx0+6.4+i*1.1, by0+5.0), 0.9, 0.5, facecolor='#FFE0B2', edgecolor='#BF360C', linewidth=0.7, zorder=7))
    ax.text(bx0+8.1, by0+5.65, "PANELS", ha='center', va='center', fontsize=3.4, weight='bold', color='#BF360C', zorder=8)
    ax.text(bx0+8.1, by0+4.6, "5.0 kN/m² • vented", ha='center', va='center', fontsize=3.4, color='#795548', style='italic', zorder=7)

    # Gallery
    ax.add_patch(Rectangle((bx0+0.23, by0+8.0), bw-0.46, 1.4-0.23, facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=0.8, linestyle=(0,(4,3)), zorder=5))
    ax.text(bx0+bw/2, by0+8.7, "GALLERY  1.40m — overlooking hall  •  RAILING 1.10m @ north edge", ha='center', va='center', fontsize=4.2, weight='bold', color='#1B5E20', zorder=7)
    # railing north edge (mezz edge)
    ax.plot([bx0+0.23, bx1-0.23], [mz_top-0.05, mz_top-0.05], color='#D32F2F', lw=2.0, linestyle=(0,(4,2)), zorder=8)
    ax.text(bx0+bw/2, mz_top+0.35, "RAIL 1.10m (steel balustrade)", ha='center', va='bottom', fontsize=3.6, color='#D32F2F', zorder=8,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#D32F2F"))

    # Windows (south + west + east at mezz)
    # south windows for offices
    for wx in [bx0+3.3, bx0+4.8, bx0+6.8, bx0+8.8]:
        ax.add_patch(Rectangle((wx-0.6, by0-0.06), 1.2, 0.22, facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=0.7, zorder=9))
    ax.text(bx0+bw/2, by0-0.65, "Alum. sliding windows (S)", ha='center', va='top', fontsize=3.5, color='#0288D1', zorder=9)
    # west windows staff/lobby
    for wy in [by0+2.0, by0+6.0]:
        ax.add_patch(Rectangle((bx0-0.06, wy), 0.22, 1.4, facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=0.7, zorder=9))
    # east windows MD/utilities + fire door
    for wy in [by0+2.0, by0+5.5]:
        ax.add_patch(Rectangle((bx1-0.16, wy), 0.22, 1.4, facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=0.7, zorder=9))
    # fire escape door east at gallery level
    fdy = by0+8.5
    ax.add_patch(Rectangle((bx1-0.12, fdy-0.5), 0.35, 1.0, facecolor='white', edgecolor='none', zorder=7))
    ax.add_patch(Rectangle((bx1-0.08, fdy-0.5), 0.2, 1.0, facecolor='#FFCDD2', edgecolor='#C62828', linewidth=1.0, zorder=8))
    ax.text(bx1+1.3, fdy, "FIRE EXIT\n0.9m", ha='center', va='center', fontsize=3.6, weight='bold', color='#C62828', zorder=9,
            bbox=dict(boxstyle="round,pad=0.2", fc="#FFEBEE", ec="#C62828"))
    # external steel stair (E) down to ground — schematic
    # landing outside + stair flight southwards down
    ax.add_patch(Rectangle((bx1+0.1, fdy-0.6), 1.2, 1.4, facecolor='none', edgecolor='#37474F', linewidth=0.9, linestyle=(0,(3,2)), zorder=6))
    ax.text(bx1+0.7, fdy+1.1, "LANDING", ha='center', va='bottom', fontsize=3.2, color='#37474F', zorder=7)
    # flight
    sx0, sy0 = bx1+0.2, by0+1.0
    ax.add_patch(Polygon([(sx0, sy0), (sx0+1.0, sy0), (sx0+1.0, fdy-0.6), (sx0, fdy-0.6)], closed=True, facecolor='#ECEFF1', edgecolor='#37474F', linewidth=0.9, zorder=5))
    # steps hint
    for i in range(1, 8):
        yy = sy0 + (fdy-0.6-sy0)*i/8
        ax.plot([sx0, sx0+1.0], [yy, yy], color='#78909C', lw=0.4, zorder=6)
    ax.text(bx1+0.7, (sy0+fdy)/2, "STEEL\nSTAIR\nDOWN", ha='center', va='center', fontsize=3.2, weight='bold', color='#37474F', rotation=0, zorder=7,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#78909C"))
    flow_arrow(ax, (bx1+0.7, fdy-1.0), (bx1+0.7, sy0+0.5), color='#37474F', lw=1.2)
    ax.text(bx1+0.7, sy0-0.3, "TO GROUND", ha='center', va='top', fontsize=3.2, color='#37474F', weight='bold')

    # dims
    dim_linear(ax, (bx0, by0), (bx1, by0), offset=-1.6, text="10.17", fontsize=6, color=COLORS['wall_blue'])
    dim_linear(ax, (bx1, by0), (bx1, mz_top), offset=-1.8, text="9.40 MEZZ", fontsize=5, color='#4A148C')
    dim_linear(ax, (bx0, mz_top), (bx0, by1), offset=2.0, text="29. ... VOID", fontsize=5, color='#757575')  # 39.4-9.4=30.0
    # fix label
    # (we'll overwrite by drawing again? Just add correct)
    # actually 39.40-9.40 = 30.00
    # The above text "29. ... VOID" is placeholder - replace by redrawing white box + correct text
    ax.text(bx0-2.0, (mz_top+by1)/2, "30.00 VOID", ha='center', va='center', fontsize=5, color='#757575', rotation=90,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=12)

    draw_north(ax, 17.5, 40, s=1.1)

    # area panel (right)
    px, py = 15.0, 18
    ax.add_patch(Rectangle((px, py), 4.4, 16.5, facecolor='#FAFAFA', edgecolor='#0F2A52', linewidth=1.0, zorder=4))
    ax.add_patch(Rectangle((px, py+14.8), 4.4, 1.7, facecolor='#4A148C', edgecolor='none', zorder=5))
    ax.text(px+2.2, py+15.65, "MEZZ AREAS", ha='center', va='center', fontsize=5.5, weight='bold', color='white', zorder=6)
    areas = [("Lobby/Stair", "≈11 m²"), ("Office 1 MD", "≈17.5 m²"), ("Office 2", "≈12 m²"), ("Staff", "≈14 m²"), ("WCs+Store", "≈10 m²"), ("Utilities", "≈16.5 m²"), ("Gallery", "≈14 m²"), ("TOTAL", "≈95.6 m²")]
    for i, (k, v) in enumerate(areas):
        yy = py+13.7-i*1.25
        bold = (k=="TOTAL")
        ax.text(px+0.3, yy, k, ha='left', va='center', fontsize=4.3, weight='bold' if bold else 'normal', color='#4A148C' if bold else '#212121', zorder=7)
        ax.text(px+4.1, yy, v, ha='right', va='center', fontsize=4.3, weight='bold', color='#4A148C' if bold else '#333333', zorder=7)
        if i<7:
            ax.plot([px+0.3, px+4.1], [yy-0.6, yy-0.6], color='#E0E0E0', lw=0.5, zorder=7)

    # notes panel (right lower)
    nx, ny = 15.0, 1.5
    ax.add_patch(Rectangle((nx, ny), 4.4, 15.5, facecolor='#F3E5F5', edgecolor='#4A148C', linewidth=1.0, zorder=4))
    ax.text(nx+2.2, ny+14.7, "MEZZ NOTES", ha='center', va='center', fontsize=5.5, weight='bold', color='#4A148C', zorder=7)
    notes = [
        "• Slab 150 RC + screed,",
        "  steel UB/APFC beams.",
        "• Headroom: 4.0 below,",
        "  4.0 to eaves above.",
        "• Railing 1.10m steel.",
        "• Stair 1.20 wide, 2 flights,",
        "  riser ≈175, going 250.",
        "• Fire exit E + external",
        "  steel stair to ground.",
        "• Offices: AC + data,",
        " 337lux; Utilities vented.",
        "• WC soil to septic (E).",
        "• Verify structure with",
        "  engineer before build.",
    ]
    for i, t in enumerate(notes):
        ax.text(nx+0.3, ny+13.5-i*0.85, t, ha='left', va='center', fontsize=4.0, color='#212121', zorder=7)

    bring_text_to_front(ax)
    save_sheet(fig, "A103_mezzanine")
    plt.close(fig)

if __name__ == "__main__":
    build()
