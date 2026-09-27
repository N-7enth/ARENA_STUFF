# A104 - Roof Plan (+8.0 eaves / +12.0 ridge) + Gate deck + Tanks
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import numpy as np
from arch_lib import *

def build():
    fig, ax = setup_sheet(figsize=(11.9, 16.8))
    ax.set_xlim(-7, 20)
    ax.set_ylim(-10, 47)
    draw_border(ax, -7, -10, 27, 57)
    draw_title_block(ax, 0.5, -9.3, 18.5, "A104", "ROOF PLAN  •  SKYLIGHTS + VENTS  •  GATE DECK + TANKS", "1:100")

    ax.text(6.5, 45.3, "ROOF PLAN  —  GABLE  EAVES +8.00m  •  RIDGE +12.00m  (RISE 4.00m)", ha='center', va='center', fontsize=10.5, weight='bold', color='#0F2A52')
    ax.text(6.5, 44.1, "Pitched metal sheeting + translucent skylight strips + ridge ventilators  •  Gate/power decked concrete @+3.0m with 2× water tanks", ha='center', va='center', fontsize=5.2, color='#333333')

    bx0, by0 = 1.5, 3.0   # building south (roof overhang 0.45)
    bw, bl = 10.17, 39.40
    bx1, by1 = bx0+bw, by0+bl
    ov = 0.45
    # roof outline with overhang
    rx0, ry0, rx1, ry1 = bx0-ov, by0-ov, bx1+ov, by1+ov

    # grid
    bays = [3.4,6,6,6,6,6,6]
    grid_ys = [by0]
    yy=by0
    for b in bays:
        yy+=b; grid_ys.append(yy)
    for i, gy in enumerate(grid_ys):
        draw_grid_bubble(ax, bx0-0.85, gy, f"{i+1}", r=0.32)

    # roof slopes: west slope (left of ridge) + east slope (right), ridge N-S at center
    ridge_x = bx0+bw/2
    # west slope
    ax.add_patch(Polygon([(rx0,ry0),(ridge_x,ry0),(ridge_x,ry1),(rx0,ry1)], closed=True, facecolor='#8FA8C8', edgecolor=COLORS['wall_blue'], linewidth=1.6, zorder=3))
    # east slope (slightly darker for depth)
    ax.add_patch(Polygon([(ridge_x,ry0),(rx1,ry0),(rx1,ry1),(ridge_x,ry1)], closed=True, facecolor='#6E8AB0', edgecolor=COLORS['wall_blue'], linewidth=1.6, zorder=3))
    # ridge line
    ax.plot([ridge_x, ridge_x], [ry0, ry1], color='#0F2A52', lw=2.2, zorder=6)
    ax.text(ridge_x, ry1+0.4, "RIDGE +12.00m (N–S)", ha='center', va='bottom', fontsize=5, weight='bold', color='#0F2A52',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#0F2A52"), zorder=8)
    # eaves labels
    ax.text(rx0-0.15, (ry0+ry1)/2, "EAVES +8.00m", ha='center', va='center', fontsize=5, weight='bold', color='#0F2A52', rotation=90,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#0F2A52"), zorder=8)
    ax.text(rx1+0.15, (ry0+ry1)/2, "EAVES +8.00m", ha='center', va='center', fontsize=5, weight='bold', color='#0F2A52', rotation=90,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#0F2A52"), zorder=8)
    # slope arrows (fall direction)
    for gy in [by0+6, by0+18, by0+30]:
        flow_arrow(ax, (ridge_x-0.6, gy), (rx0+0.9, gy), color='white', lw=1.6)
        flow_arrow(ax, (ridge_x+0.6, gy), (rx1-0.9, gy), color='white', lw=1.6)
    ax.text((rx0+ridge_x)/2, by0+2.2 if False else ry0+0.9, "38° PITCH (4.0 rise / 5.085 half-span)", ha='center', va='center', fontsize=4, color='white', weight='bold', zorder=7)
    ax.text((ridge_x+rx1)/2, ry0+0.9, "38° PITCH", ha='center', va='center', fontsize=4, color='white', weight='bold', zorder=7)

    # purlin lines (horizontal faint)
    for gy in grid_ys:
        ax.plot([rx0, rx1], [gy, gy], color='white', lw=0.4, alpha=0.35, zorder=4)

    # skylight strips: 2 per slope, 1.0m wide, full length with breaks at ridge vents? Continuous with gaps at frames?
    # West slope: strips at 1/3 and 2/3 of half-span
    half = bw/2
    for frac in [0.33, 0.66]:
        # west
        wx_c = ridge_x - half*frac
        ax.add_patch(Rectangle((wx_c-0.5, ry0+0.6), 1.0, (ry1-ry0)-1.2, facecolor=COLORS['skylight'], edgecolor='#0288D1', linewidth=0.9, zorder=5))
        # east
        ex_c = ridge_x + half*frac
        ax.add_patch(Rectangle((ex_c-0.5, ry0+0.6), 1.0, (ry1-ry0)-1.2, facecolor=COLORS['skylight'], edgecolor='#0288D1', linewidth=0.9, zorder=5))
    ax.text((rx0+ridge_x)/2, ry1-1.2, "TRANSLUCENT\nSKYLIGHTS ×2", ha='center', va='center', fontsize=4.2, weight='bold', color='#01579B',
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#0288D1", alpha=0.95), zorder=8)
    ax.text((ridge_x+rx1)/2, ry1-1.2, "TRANSLUCENT\nSKYLIGHTS ×2", ha='center', va='center', fontsize=4.2, weight='bold', color='#01579B',
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#0288D1", alpha=0.95), zorder=8)

    # ridge ventilators: 6 nos along ridge @~6m (skip south bay?)
    vent_ys = [by0+6.4, by0+12.4, by0+18.4, by0+24.4, by0+30.4, by0+36.4]
    for vy in vent_ys:
        ax.add_patch(Rectangle((ridge_x-0.7, vy-0.5), 1.4, 1.0, facecolor='#37474F', edgecolor='white', linewidth=0.8, zorder=7))
        ax.add_patch(Circle((ridge_x, vy), 0.28, facecolor='#ECEFF1', edgecolor='white', linewidth=0.6, zorder=8))
    ax.text(ridge_x+1.1, vent_ys[3], "RIDGE VENTS ×6\n(hot-air exhaust)", ha='left', va='center', fontsize=4, color='#212121', weight='bold',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#37474F"), zorder=9)
    # gutters + downspouts
    ax.plot([rx0+0.1, rx0+0.1], [ry0, ry1], color='#263238', lw=1.8, zorder=6)
    ax.plot([rx1-0.1, rx1-0.1], [ry0, ry1], color='#263238', lw=1.8, zorder=6)
    ax.text(rx0+0.1, ry0-0.35, "GUTTER + RWP @6m to drain", ha='left', va='top', fontsize=3.6, color='#263238', style='italic')
    ax.text(rx1-0.1, ry0-0.35, "GUTTER + RWP @6m", ha='right', va='top', fontsize=3.6, color='#263238', style='italic')
    for gy in grid_ys[1:-1]:
        ax.add_patch(Circle((rx0+0.1, gy), 0.12, facecolor='#263238', edgecolor='white', linewidth=0.4, zorder=7))
        ax.add_patch(Circle((rx1-0.1, gy), 0.12, facecolor='#263238', edgecolor='white', linewidth=0.4, zorder=7))

    # printing extract duct (from printing room to roof)
    duct_x, duct_y = bx0+8.2, by1-3.0
    ax.add_patch(Circle((duct_x, duct_y), 0.45, facecolor='#6A1B9A', edgecolor='white', linewidth=1.0, zorder=8))
    ax.text(duct_x, duct_y, "EX", ha='center', va='center', fontsize=4, weight='bold', color='white', zorder=9)
    ax.text(duct_x+0.7, duct_y+0.3, "PRINT fume\n extract", ha='left', va='center', fontsize=3.6, color='#6A1B9A', weight='bold',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#6A1B9A"), zorder=9)

    # dims
    dim_linear(ax, (rx0, ry1), (rx1, ry1), offset=1.4, text="11.07 o/a (10.17 + 2×0.45 o/h)", fontsize=5, color=COLORS['wall_blue'])
    dim_linear(ax, (rx1, ry0), (rx1, ry1), offset=-1.6, text="40.30 o/a", fontsize=5, color=COLORS['wall_blue'])

    # ---- GATE / POWER DECK (below building, south) ----
    # site coords: building south by0=3.0 in this sheet's local? Actually sheet local: building y 3.0-42.4. Gate block south of building: y 0.0-2.4? Let's place gate deck at y -0.5..1.9? Simpler: show gate deck plan + side detail below roof.
    gx0, gy0, gw, gd = bx0+1.2, -1.8, 11.2, 2.4  # note: extends east beyond building (site wider)
    # clip to fit? bx0+1.2=2.7, +11.2=13.9, xlim -7..20, fits.
    ax.text((gx0+gx0+gw)/2, gy0+gd+0.7, "GATE / SECURITY / POWER — DECKED CONCRETE ROOF @+3.00m (TANKS ABOVE)", ha='center', va='bottom', fontsize=5.5, weight='bold', color='#5D4037')
    # deck slab
    ax.add_patch(Rectangle((gx0, gy0), gw, gd, facecolor='#D7CCC8', edgecolor='#4E342E', linewidth=1.6, zorder=5))
    # parapet
    ax.add_patch(Rectangle((gx0+0.15, gy0+0.15), gw-0.3, gd-0.3, facecolor='none', edgecolor='#4E342E', linewidth=0.6, linestyle=(0,(3,2)), zorder=6))
    ax.text(gx0+gw/2, gy0+0.35, "150 RC DECK + screed + parapet 450 high", ha='center', va='center', fontsize=3.6, color='#4E342E', style='italic', zorder=7)
    # tanks on deck (plan circles)
    draw_tank(ax, gx0+2.0, gy0+1.45, 0.55, "2000L\nWATER")
    draw_tank(ax, gx0+4.0, gy0+1.45, 0.55, "2000L\nWATER")
    draw_tank(ax, gx0+9.2, gy0+1.45, 0.40, "HEADER")
    # access ladder
    ax.add_patch(Rectangle((gx0+gw-0.7, gy0-1.0), 0.5, 1.0, facecolor='none', edgecolor='#37474F', linewidth=0.9, zorder=6))
    for i in range(3):
        ax.plot([gx0+gw-0.7, gx0+gw-0.2], [gy0-0.8+i*0.3, gy0-0.8+i*0.3], color='#37474F', lw=0.6, zorder=7)
    ax.text(gx0+gw-0.45, gy0-1.25, "STEEL LADDER", ha='center', va='top', fontsize=3.4, color='#37474F', weight='bold')
    # rooms below (dashed)
    for px in [gx0+3.2, gx0+5.2, gx0+7.2]:
        ax.plot([px, px], [gy0, gy0+gd], color='#8D6E63', lw=0.7, linestyle=(0,(3,3)), zorder=6)
    ax.text(gx0+1.6, gy0+0.7 if False else gy0+gd-0.25, "SEC", ha='center', va='center', fontsize=3.4, color='#5D4037', zorder=7)
    # overflow + feed arrows
    flow_arrow(ax, (gx0+2.0, gy0+0.9), (gx0+2.0, gy0+0.2), color='#0288D1', lw=1.2)
    ax.text(gx0+0.4, gy0+1.45, "TANKS\nON DECK", ha='center', va='center', fontsize=3.6, weight='bold', color='#01579B',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#0288D1"), zorder=8)
    dim_linear(ax, (gx0, gy0), (gx0+gw, gy0), offset=-0.8, text="≈11.20", fontsize=5, color='#5D4037')

    # courtyard gap between gate deck and building
    ax.annotate("", xy=(bx0+0.5, by0-0.45), xytext=(bx0+0.5, gy0+gd),
                arrowprops=dict(arrowstyle="<->", color='#2E7D32', linewidth=1.0), zorder=7)
    ax.text(bx0-0.3, (gy0+gd+by0)/2, "2.4m\nCOURT", ha='center', va='center', fontsize=4, color='#2E7D32', weight='bold')

    draw_north(ax, 17.5, 40, s=1.1)

    # spec panel (right)
    px, py = 15.0, 14
    ax.add_patch(Rectangle((px, py), 4.4, 22.5, facecolor='#ECEFF1', edgecolor='#0F2A52', linewidth=1.0, zorder=4))
    ax.add_patch(Rectangle((px, py+20.8), 4.4, 1.7, facecolor=COLORS['title_bg'], edgecolor='none', zorder=5))
    ax.text(px+2.2, py+21.65, "ROOF SPEC", ha='center', va='center', fontsize=5.5, weight='bold', color='white', zorder=6)
    spec = [
        "• 0.55 aluminium-zinc",
        "  metal sheeting,",
        "  fixed to steel purlins.",
        "• Pitch 38° (4.0/5.085).",
        "• Skylights: translucent",
        "  GRP/polycarbonate,",
        "  1.0 wide ×2/slope.",
        "• Ridge vents ×6 +",
        "  eaves gap vent.",
        "• Gutters 150 uPVC +",
        "  RWP @6m to soakaway.",
        "• Purlins RHS + sag rods.",
        "• Portal rafters UB/RSJ",
        "  @6.0m (7 frames).",
        "• Eaves HDG fascia.",
        "• Print extract: 300Ø",
        "  duct + cowl + fan.",
        "• Lightning tape + rods.",
    ]
    for i, t in enumerate(spec):
        ax.text(px+0.3, py+19.6-i*0.95, t, ha='left', va='center', fontsize=4.1, color='#212121', zorder=7)

    # deck spec (right lower)
    dx, dy = 15.0, 4.5
    ax.add_patch(Rectangle((dx, dy), 4.4, 8.5, facecolor='#FFF8E1', edgecolor='#F57F17', linewidth=1.0, zorder=4))
    ax.text(dx+2.2, dy+7.9, "DECK + TANKS", ha='center', va='center', fontsize=5.5, weight='bold', color='#E65100', zorder=7)
    ds = [
        "• Deck 150 RC + Falls.",
        "• 2× 2000L water + header.",
        "• Borehole → tanks →",
        "  points (gravity).",
        "• Overflow to drain.",
        "• Parapet 450 + rail.",
        "• Ladder access (E).",
    ]
    for i, t in enumerate(ds):
        ax.text(dx+0.3, dy+6.9-i*0.9, t, ha='left', va='center', fontsize=4.1, color='#4E342E', zorder=7)

    bring_text_to_front(ax)
    save_sheet(fig, "A104_roof")
    plt.close(fig)

if __name__ == "__main__":
    build()
