# A101 - Site Plan
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle
import numpy as np
from arch_lib import *

def build():
    fig, ax = setup_sheet(figsize=(11.9, 16.8))
    # drawing extents in meters (site coords) -> map to axes coords
    # We'll use data coords = meters, set xlim/ylim to fit plot + road + title
    # Layout: main plan on left 2/3, info panel on right 1/3? Actually keep plan centered left, title bottom-right.
    # Use data limits:
    ax.set_xlim(-8, 30)
    ax.set_ylim(-10, 58)

    draw_border(ax, -8, -10, 38, 68)
    draw_title_block(ax, 8.5, -9.2, 20.5, "A101", "SITE & LOCATION PLAN  •  GATEHOUSE  •  SETBACKS", "1:200 (SITE)")

    # Title heading
    ax.text(11, 55.5, "SITE PLAN  —  806.896 m²  (LAA/195/29/2025/LA)", ha='center', va='center', fontsize=11, weight='bold', color='#0F2A52')
    ax.text(11, 54.3, "Production hall 10.17 × 39.40m  •  Gate/Security/Power block decked  •  Steel portal @6.0m  •  Eaves +8.0m / Ridge +12.0m", ha='center', va='center', fontsize=6, color='#333333')

    # ---- ROAD (south) ----
    ax.add_patch(Rectangle((-7.7, -4.6), 37.4, 4.1, facecolor='#E0E0E0', edgecolor='#9E9E9E', linewidth=0.8, zorder=1))
    # road center dashes
    for xx in np.arange(-7, 29, 2):
        ax.plot([xx, xx+1], [-2.6, -2.6], color='white', lw=1.5, zorder=2)
    ax.text(0.5, -3.9, "ILOGBO / FOUNDATION  ROAD  (MAIN ROAD)", ha='left', va='center', fontsize=7, weight='bold', color='#424242')
    ax.text(0.5, -3.1, "Main Gate  →  4.6m sliding gate + pedestrian gate", ha='left', va='center', fontsize=5, color='#616161')

    # ---- PLOT (red line) ----
    SW = (0,0); SE=(17.25,0); NE=(15.42,51.8); NW=(0,46.8)
    plot = Polygon([SW, SE, NE, NW], closed=True, facecolor='#FFF8F1', edgecolor=COLORS['plot_red'], linewidth=2.2, zorder=3)
    ax.add_patch(plot)
    # (plot watermark removed - overlapped hall label)

    # beacons
    for pt, lab in [(SW,"AN 4564\nLW"), (SE,"AN 4563"), (NE,"AN 4566\nLW"), (NW,"AN 4565\nLW")]:
        ax.add_patch(Circle(pt, 0.45, facecolor='white', edgecolor=COLORS['plot_red'], linewidth=1.4, zorder=6))
        ax.add_patch(Circle(pt, 0.12, facecolor=COLORS['plot_red'], edgecolor='none', zorder=7))
        ax.text(pt[0], pt[1]+0.9 if pt[1]<25 else pt[1]-1.1, lab, ha='center', va='center', fontsize=4, color=COLORS['plot_red'], weight='bold',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=COLORS['plot_red'], alpha=0.95), zorder=8)

    # plot dimensions (red)
    dim_linear(ax, SW, SE, offset=-1.2, text="17.25  (FRONT)", fontsize=6, color=COLORS['plot_red'])
    dim_linear(ax, NW, (15.42,51.8), offset=1.0, text="16.17  (REAR)", fontsize=6, color=COLORS['plot_red'])
    dim_linear(ax, SW, NW, offset=1.4, text="46.80", fontsize=6, color=COLORS['plot_red'])
    dim_linear(ax, SE, NE, offset=-1.4, text="51.82", fontsize=6, color=COLORS['plot_red'])

    # ---- FENCE ----
    # show fence just inside plot (thin dashed)
    fence = Polygon([(0.25,0.5),(16.95,0.5),(15.15,51.2),(0.25,46.35)], closed=True, facecolor='none', edgecolor='#616161', linewidth=0.7, linestyle=(0,(4,3)), zorder=4)
    ax.add_patch(fence)
    ax.text(19.5, 30, "FENCE\n(on boundary)", ha='left', va='center', fontsize=4.5, color='#616161')

    # ---- PRODUCTION BUILDING footprint (blue) ----
    bx0, by0 = 4.0, 5.4  # SW corner
    bw, bl = 10.17, 39.40
    ax.add_patch(Rectangle((bx0, by0), bw, bl, facecolor=COLORS['wall_fill'], edgecolor=COLORS['wall_blue'], linewidth=2.0, zorder=5))
    # grid lines @6m (7 bays: 6+6+6+6+6+6+3.4 from north? Let's put 3.4 at south)
    # South y=5.4, then bays northwards: 3.4,6,6,6,6,6,6 = 39.4
    grid_ys = [by0]
    bays = [3.4,6,6,6,6,6,6]
    yy = by0
    for b in bays:
        yy += b
        grid_ys.append(yy)
    for i, gy in enumerate(grid_ys):
        # stanchion ticks on both walls
        for gx in [bx0, bx0+bw]:
            ax.add_patch(Rectangle((gx-0.25, gy-0.25), 0.5, 0.5, facecolor=COLORS['steel'], edgecolor='white', linewidth=0.5, zorder=7))
        if 0 < i < len(grid_ys):
            ax.plot([bx0, bx0+bw], [gy, gy], color=COLORS['steel'], lw=0.4, linestyle=(0,(3,3)), alpha=0.5, zorder=4)
    # grid bubbles west
    for i, gy in enumerate(grid_ys):
        draw_grid_bubble(ax, bx0-0.9, gy, f"{i+1}")
    # grid bubbles south/north for A-B?
    draw_grid_bubble(ax, bx0, by0-0.9, "A")
    draw_grid_bubble(ax, bx0+bw, by0-0.9, "B")

    ax.text(bx0+bw/2, by0+bl/2+2, "PRODUCTION HALL\n10.17 × 39.40m", ha='center', va='center', fontsize=7, weight='bold', color=COLORS['wall_blue'], zorder=6)
    ax.text(bx0+bw/2, by0+bl/2+0.2, "Steel portal @6.0m\nEaves +8.0m  •  Ridge +12.0m", ha='center', va='center', fontsize=4.5, color='#333333', zorder=6)
    ax.text(bx0+bw/2, by0+4.7, "MEZZANINE ABOVE\n(south 9.40m)", ha='center', va='center', fontsize=4.5, weight='bold', color='#4A148C',
            bbox=dict(boxstyle="round,pad=0.25", fc="#F3E5F5", ec="#7B1FA2"), zorder=8)
    ax.text(bx0+bw/2, by0+bl-3, "PRINT (walled)  |  RAW STORE", ha='center', va='center', fontsize=4, color='#333333',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#999999"), zorder=8)

    # building dims (blue)
    dim_linear(ax, (bx0, by0), (bx0+bw, by0), offset=-0.9, text="10.17", fontsize=6, color=COLORS['wall_blue'])
    dim_linear(ax, (bx0+bw, by0), (bx0+bw, by0+bl), offset=-1.6, text="39.40  (= 41.80 − 2.40 security)", fontsize=5, color=COLORS['wall_blue'])
    # setbacks (green/grey)
    dim_linear(ax, (0.25, 20), (bx0, 20), offset=0.0, text="4.0", fontsize=5, color='#2E7D32')
    ax.text(2.1, 22.2, "DRIVEWAY /\n3 ENTRANCES (W)", ha='center', va='center', fontsize=4, color='#2E7D32', weight='bold')
    dim_linear(ax, (bx0+bw, 20), (16.6, 20), offset=0.0, text="≈2.0", fontsize=5, color='#2E7D32')
    dim_linear(ax, (bx0, by0+bl), (bx0, 46.8), offset=-0.7, text="2.0 min", fontsize=5, color='#2E7D32')
    dim_linear(ax, (bx0, 3.0), (bx0, by0), offset=0.9, text="2.4 court", fontsize=4.5, color='#2E7D32')

    # driveway arrows
    flow_arrow(ax, (2.1, 2.0), (2.1, 8.0), color='#2E7D32', lw=1.4)
    ax.text(2.1, 1.2, "IN", ha='center', va='center', fontsize=5, weight='bold', color='#2E7D32',
            bbox=dict(boxstyle="circle,pad=0.3", fc="white", ec="#2E7D32"))

    # ---- GATE / SECURITY / POWER BLOCK (front) ----
    gx0, gy0, gw, gd = 5.2, 0.6, 11.2, 2.4
    ax.add_patch(Rectangle((gx0, gy0), gw, gd, facecolor='#FFFDE7', edgecolor='#F57F17', linewidth=1.6, zorder=5))
    # partitions: Security 3.2 | Lobby 2.0 | Store 2.0 | Power 4.0
    px = [gx0, gx0+3.2, gx0+5.2, gx0+7.2, gx0+gw]
    labels = ["SECURITY\n2.4m deep", "LOBBY/\nPASSAGE", "STORE", "POWER /\nUTILITIES"]
    for i in range(4):
        if i>0:
            ax.plot([px[i], px[i]], [gy0, gy0+gd], color='#F57F17', lw=1.0, zorder=6)
        ax.text((px[i]+px[i+1])/2, gy0+gd/2, labels[i], ha='center', va='center', fontsize=4, weight='bold', color='#5D4037', zorder=7)
    ax.text(gx0+gw/2, gy0+gd+0.35, "GATEHOUSE + POWER BLOCK  —  decked concrete roof @+3.0m carrying tanks  (see A104)", ha='center', va='bottom', fontsize=4.5, color='#5D4037', style='italic',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#F57F17"), zorder=8)
    dim_linear(ax, (gx0, gy0), (gx0+gw, gy0), offset=-0.7, text="≈11.20", fontsize=5, color='#5D4037')
    dim_linear(ax, (gx0+gw, gy0), (gx0+gw, gy0+gd), offset=-0.7, text="2.40", fontsize=5, color='#5D4037')

    # gate
    ax.add_patch(Rectangle((0.5, 0.35), 4.4, 0.35, facecolor='#37474F', edgecolor='black', linewidth=1.0, zorder=7))
    ax.text(2.7, 0.05, "4.6m SLIDING GATE", ha='center', va='top', fontsize=4, weight='bold', color='#212121', zorder=8)
    # pedestrian gate
    ax.add_patch(Rectangle((0.5, 0.7), 0.9, 0.12, facecolor='none', edgecolor='#212121', linewidth=0.8, zorder=7))
    ax.text(0.95, 1.05, "PED.", ha='center', va='bottom', fontsize=3.5, color='#212121')

    # ---- BOREHOLE (NW setback) ----
    bore = (1.5, 44.0)
    ax.add_patch(Circle(bore, 0.5, facecolor='#B3E5FC', edgecolor='#01579B', linewidth=1.2, zorder=7))
    ax.text(bore[0], bore[1], "BH", ha='center', va='center', fontsize=4, weight='bold', color='#01579B', zorder=8)
    ax.plot([bore[0], bore[0]], [bore[1]-0.5, bore[1]-1.2], color='#01579B', lw=0.7, linestyle=(0,(2,2)), zorder=7)
    ax.text(bore[0], bore[1]-1.9, "BOREHOLE (exist.)", ha='center', va='center', fontsize=4, color='#01579B', weight='bold',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#01579B"), zorder=8)

    # septic / soakaway hint (SE corner?)
    ax.add_patch(Rectangle((15.0, 3.6), 1.4, 1.0, facecolor='none', edgecolor='#6D4C41', linewidth=0.7, linestyle=(0,(3,2)), zorder=5))
    ax.text(15.7, 3.45, "SEPTIC (prop.)", ha='center', va='top', fontsize=3.5, color='#6D4C41')

    # north arrow + scale bar
    draw_north(ax, 25.5, 48, s=1.4)
    # scale bar 0-5-10m (at 1:200 on paper, but here data units = m, bar in m)
    sbx, sby = 18.5, 2.0
    ax.text(sbx+5.0, sby+1.0, "SCALE BAR (m)", ha='center', va='bottom', fontsize=5, weight='bold', color='#333333')
    for i in range(5):
        fc = '#0F2A52' if i%2==0 else 'white'
        ax.add_patch(Rectangle((sbx+i*2, sby), 2, 0.5, facecolor=fc, edgecolor='black', linewidth=0.7, zorder=6))
    for i in range(6):
        ax.text(sbx+i*2, sby-0.15, f"{i*2}", ha='center', va='top', fontsize=4, color='#333333')
    ax.text(sbx+10.4, sby+0.25, "m", ha='left', va='center', fontsize=5, color='#333333')

    # ---- NOTES panel (right side) ----
    nx, ny = 20.5, 8
    ax.add_patch(Rectangle((nx, ny), 8.0, 30.5, facecolor='#F5F7FA', edgecolor='#0F2A52', linewidth=1.0, zorder=4))
    ax.add_patch(Rectangle((nx, ny+28.5), 8.0, 2.0, facecolor=COLORS['title_bg'], edgecolor='none', zorder=5))
    ax.text(nx+4.0, ny+29.5, "SITE NOTES & AREAS", ha='center', va='center', fontsize=6.5, weight='bold', color='white', zorder=6)
    notes = [
        "1. RED line = plot boundary (survey).",
        "2. BLUE = production walls + steel",
        "    stanchions @6.0m c/c.",
        "3. Production shortened 2.40m to",
        "    allow gate/security/power block.",
        "4. West driveway 4.0m: 3 entrances",
        "    (Raw store / QC / Reception).",
        "5. Printing room walled + own east",
        "    entrance (chemicals).",
        "6. Mezzanine over south 9.40m;",
        "    decked for offices + utilities.",
        "7. Gate/power decked @+3.0m for",
        "    2× water tanks + header.",
        "8. Eaves +8.0m, ridge +12.0m;",
        "    skylights + ridge vents.",
        "9. Borehole retained (NW).",
        "10. All dims in metres; verify on site.",
    ]
    for i, t in enumerate(notes):
        ax.text(nx+0.4, ny+27.3-i*1.15, t, ha='left', va='top', fontsize=4.6, color='#212121', family='monospace')
    # area table
    ax.add_patch(Rectangle((nx+0.3, ny+0.4), 7.4, 7.2, facecolor='white', edgecolor='#0F2A52', linewidth=0.7, zorder=6))
    ax.text(nx+4.0, ny+7.2, "AREA SCHEDULE", ha='center', va='center', fontsize=5.5, weight='bold', color='#0F2A52', zorder=7)
    rows = [
        ("Plot", "806.90 m²"),
        ("Production G/F", "400.70 m²"),
        ("Mezzanine", "95.60 m²"),
        ("Gate/Power", "27.60 m²"),
        ("Total GFA", "523.90 m²"),
        ("Coverage", "49.7%"),
    ]
    for i, (k,v) in enumerate(rows):
        yy = ny+6.3-i*0.9
        ax.text(nx+0.7, yy, k, ha='left', va='center', fontsize=4.5, color='#333333', zorder=7)
        ax.text(nx+7.3, yy, v, ha='right', va='center', fontsize=4.5, weight='bold', color='#0F2A52', zorder=7)
        if i < 5:
            ax.plot([nx+0.5, nx+7.5], [yy-0.45, yy-0.45], color='#E0E0E0', lw=0.5, zorder=7)

    # legend
    lx, ly = 20.5, 39.5
    ax.add_patch(Rectangle((lx, ly), 8.0, 6.5, facecolor='white', edgecolor='#0F2A52', linewidth=1.0, zorder=4))
    ax.text(lx+4.0, ly+6.0, "LEGEND", ha='center', va='center', fontsize=6, weight='bold', color='#0F2A52')
    leg = [
        (COLORS['plot_red'], "Plot boundary"),
        (COLORS['wall_blue'], "Production walls"),
        (COLORS['steel'], "Steel stanchion"),
        ('#F57F17', "Gate / power block"),
        ('#2E7D32', "Flow / driveway"),
    ]
    for i, (c, t) in enumerate(leg):
        yy = ly+5.0-i*0.9
        ax.add_patch(Rectangle((lx+0.5, yy-0.25), 0.9, 0.5, facecolor=c, edgecolor='black', linewidth=0.5, zorder=6))
        ax.text(lx+1.7, yy, t, ha='left', va='center', fontsize=4.5, color='#333333')

    bring_text_to_front(ax)
    save_sheet(fig, "A101_site_plan")
    plt.close(fig)

if __name__ == "__main__":
    build()
