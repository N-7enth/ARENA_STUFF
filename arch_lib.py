# Architectural drawing helpers - Nylon Production & Packaging Plant
# Plot: Ilogbo/Foundation Road, Oko-Afo, Badagry, Lagos
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch, Circle, Wedge, FancyArrowPatch, PathPatch
from matplotlib.path import Path
import matplotlib.patheffects as pe
import numpy as np

# ---------- STYLE ----------
COLORS = {
    'plot_red': '#C1272D',
    'wall_blue': '#1B3A6B',
    'wall_fill': '#EAF0FA',
    'steel': '#2F5597',
    'machine_red': '#C1272D',
    'machine_fill': '#FDECEC',
    'print_wall': '#7B2D8B',
    'print_fill': '#F5E6F7',
    'store': '#E8F5E9',
    'office': '#FFF8E1',
    'qc': '#E0F2F1',
    'fg': '#E3F2FD',
    'stair': '#FFE0B2',
    'toilet': '#E1F5FE',
    'road': '#9E9E9E',
    'asphalt': '#E0E0E0',
    'grass': '#C8E6C9',
    'roof': '#5B7DB1',
    'roof_dark': '#3D5A80',
    'skylight': '#B3E5FC',
    'concrete': '#CFD8DC',
    'tank': '#0288D1',
    'dim': '#333333',
    'grid': '#90A4AE',
    'title_bg': '#0F2A52',
    'title_accent': '#1E88E5',
    'text': '#1A1A1A',
}

TITLE = "NYLON PRODUCTION & PACKAGING PLANT"
SUBTITLE = "Along Ilogbo / Foundation Road, Oko-Afo, Badagry LGA, Lagos State"
CLIENT = "Mr. Dibie Chukwuweike Cyril  |  Survey: LAA/195/29/2025/LA  |  Area: 806.896 m²"

def setup_sheet(figsize=(11.9, 16.8)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    # use almost full figure so border fills page
    ax.set_position([0.02, 0.02, 0.96, 0.96])
    return fig, ax

def mm_to_inch(x): return x/25.4

def draw_border(ax, x0, y0, w, h, lw=1.2):
    ax.add_patch(Rectangle((x0, y0), w, h, fill=False, edgecolor='#0F2A52', linewidth=lw, zorder=1))
    ax.add_patch(Rectangle((x0+0.3, y0+0.3), w-0.6, h-0.6, fill=False, edgecolor='#0F2A52', linewidth=0.6, zorder=1))

def draw_title_block(ax, x0, y0, w, sheet_no, sheet_title, scale_txt, date_txt="27-09-2026", status="PRELIMINARY - FOR DISCUSSION"):
    """Title block at bottom-right inside border. x0,y0 = bottom-left of block."""
    bh = 3.4
    ax.add_patch(Rectangle((x0, y0), w, bh, facecolor='white', edgecolor='#0F2A52', linewidth=1.0, zorder=5))
    ax.add_patch(Rectangle((x0, y0+bh-0.85), w, 0.85, facecolor=COLORS['title_bg'], edgecolor='none', zorder=6))
    ax.text(x0+w/2, y0+bh-0.42, TITLE, ha='center', va='center', fontsize=7, weight='bold', color='white', zorder=7)
    ax.text(x0+w/2, y0+bh-1.20, SUBTITLE, ha='center', va='center', fontsize=4.3, color='#333333', style='italic', zorder=7)
    ax.plot([x0, x0+w], [y0+1.35, y0+1.35], color='#0F2A52', lw=0.7, zorder=6)
    ax.text(x0+0.3, y0+0.95, f"{sheet_no}  |  {sheet_title}", ha='left', va='center', fontsize=5.2, weight='bold', color='#0F2A52', zorder=7)
    ax.text(x0+w-0.3, y0+0.95, f"{scale_txt}  |  {date_txt}", ha='right', va='center', fontsize=4.3, color='#333333', zorder=7)
    ax.add_patch(Rectangle((x0+0.12, y0+0.12), w-0.24, 0.5, facecolor='#FFF3E0', edgecolor='#E65100', linewidth=0.7, zorder=6))
    ax.text(x0+w/2, y0+0.37, status, ha='center', va='center', fontsize=4.8, weight='bold', color='#BF360C', zorder=7)

def draw_north(ax, x, y, s=1.0, label="N"):
    circ = Circle((x, y), 0.55*s, fill=False, edgecolor='#0F2A52', linewidth=1.2, zorder=6)
    ax.add_patch(circ)
    # arrow
    ax.annotate("", xy=(x, y+0.5*s), xytext=(x, y-0.4*s),
                arrowprops=dict(facecolor='#0F2A52', edgecolor='#0F2A52', width=1.5, headwidth=7, headlength=7), zorder=7)
    ax.text(x, y+0.75*s, label, ha='center', va='center', fontsize=8, weight='bold', color='#0F2A52', zorder=7)

def dim_linear(ax, p1, p2, offset=0.8, text="", fontsize=5, color='#333333', ext=True, text_offset=0.25):
    """Draw a linear dimension between p1 and p2 (tuples), offset perpendicular."""
    p1 = np.array(p1, float); p2 = np.array(p2, float)
    d = p2 - p1
    L = np.linalg.norm(d)
    if L == 0: return
    u = d / L
    n = np.array([-u[1], u[0]])
    q1 = p1 + n*offset
    q2 = p2 + n*offset
    # extension lines
    if ext:
        ax.plot([p1[0]+n*0.1, q1[0]+n*0.15], [p1[1]+n[1]*0.1, q1[1]+n[1]*0.15], color=color, lw=0.5, zorder=4)
        ax.plot([p2[0]+n*0.1, q2[0]+n*0.15], [p2[1]+n[1]*0.1, q2[1]+n[1]*0.15], color=color, lw=0.5, zorder=4)
    # main line
    ax.plot([q1[0], q2[0]], [q1[1], q2[1]], color=color, lw=0.7, zorder=4)
    # ticks (arrow)
    ax.plot([q1[0]], [q1[1]], marker='|', color=color, markersize=5, markeredgewidth=0.8, zorder=4)
    ax.plot([q2[0]], [q2[1]], color=color, markersize=5, markeredgewidth=0.8, marker='|', zorder=4)
    # text
    mid = (q1+q2)/2 + n*text_offset
    ang = np.degrees(np.arctan2(d[1], d[0]))
    # keep text readable
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    ax.text(mid[0], mid[1], text, ha='center', va='center', fontsize=fontsize, color=color,
            rotation=ang, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9), zorder=5)

def draw_door_swing(ax, hinge, r, a0, a1, leaf_angle, color='#1B3A6B', lw=1.0):
    """hinge=(x,y), r=leaf length, a0-a1=arc span deg, leaf_angle=leaf direction deg."""
    import math
    # arc
    arc = Wedge(hinge, r, a0, a1, facecolor='none', edgecolor=color, linewidth=0.6, linestyle=(0,(2,2)), zorder=6)
    ax.add_patch(arc)
    # leaf
    lx = hinge[0] + r*math.cos(math.radians(leaf_angle))
    ly = hinge[1] + r*math.radians(leaf_angle)*0 if False else hinge[1] + r*math.sin(math.radians(leaf_angle))
    ax.plot([hinge[0], lx], [hinge[1], ly], color=color, lw=lw, zorder=6)

def draw_roller(ax, x, y, w, h, horizontal=True):
    # roller shutter: double line + diagonal hatch
    ax.add_patch(Rectangle((x, y), w, h, facecolor='#B0BEC5', edgecolor='#37474F', linewidth=1.0, zorder=5))
    if horizontal:
        for i in range(1, 4):
            yy = y + h*i/4
            ax.plot([x, x+w], [yy, yy], color='#78909C', lw=0.4, zorder=6)
    else:
        for i in range(1, 4):
            xx = x + w*i/4
            ax.plot([xx, xx], [y, y+h], color='#78909C', lw=0.4, zorder=6)

def draw_stair(ax, x, y, w, h, direction='up', n_steps=10, color='#5D4037'):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=COLORS['stair'], edgecolor=color, linewidth=1.0, zorder=4))
    if direction in ('up', 'down'):
        for i in range(1, n_steps):
            yy = y + h*i/n_steps
            ax.plot([x, x+w], [yy, yy], color=color, lw=0.4, zorder=5)
        # arrow
        midx = x+w/2
        if direction == 'up':
            ax.annotate("", xy=(midx, y+h-0.3), xytext=(midx, y+0.3),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.2), zorder=6)
            ax.text(midx+0.15, y+h/2, "UP", fontsize=4.5, rotation=90, va='center', color=color, weight='bold')
        else:
            ax.annotate("", xy=(midx, y+0.3), xytext=(midx, y+h-0.3),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.2), zorder=6)
    else:
        for i in range(1, n_steps):
            xx = x + w*i/n_steps
            ax.plot([xx, xx], [y, y+h], color=color, lw=0.4, zorder=5)

def draw_machine(ax, x, y, w, h, label, sublabel="", tall=False, color=None):
    fc = COLORS['machine_fill'] if not tall else '#E8EAF6'
    ec = COLORS['machine_red'] if not tall else '#283593'
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=1.4, zorder=5))
    # corner bolts
    for cx, cy in [(x+0.12, y+0.12), (x+w-0.12, y+0.12), (x+0.12, y+h-0.12), (x+w-0.12, y+h-0.12)]:
        ax.add_patch(Circle((cx, cy), 0.06, facecolor=ec, edgecolor='none', zorder=6))
    ax.text(x+w/2, y+h/2+0.15, label, ha='center', va='center', fontsize=5, weight='bold', color=ec, zorder=7)
    if sublabel:
        ax.text(x+w/2, y+h/2-0.28, sublabel, ha='center', va='center', fontsize=4, color='#555555', zorder=7)
    if tall:
        # height indicator
        ax.text(x+w/2, y+h+0.12, "H≈9m", ha='center', va='bottom', fontsize=3.5, color='#283593', style='italic', zorder=7)

def draw_pallets(ax, x, y, cols, rows, pw=1.0, pd=1.0, gap=0.12, facecolor='#D7CCC8', edgecolor='#5D4037'):
    for i in range(cols):
        for j in range(rows):
            xx = x + i*(pw+gap); yy = y + j*(pd+gap)
            ax.add_patch(Rectangle((xx, yy), pw, pd, facecolor=facecolor, edgecolor=edgecolor, linewidth=0.5, zorder=4))
            # cross
            ax.plot([xx, xx+pw], [yy, yy+pd], color=edgecolor, lw=0.3, zorder=5)
            ax.plot([xx, xx+pw], [yy+pd, yy], color=edgecolor, lw=0.3, zorder=5)

def draw_tank(ax, x, y, r, label="2000L"):
    ax.add_patch(Circle((x, y), r, facecolor=COLORS['tank'], edgecolor='#01579B', linewidth=1.0, zorder=6))
    ax.add_patch(Circle((x, y), r*0.55, facecolor='#B3E5FC', edgecolor='#01579B', linewidth=0.6, zorder=7))
    ax.text(x, y-r-0.25, label, ha='center', va='top', fontsize=4, color='#01579B', weight='bold')

def flow_arrow(ax, p1, p2, color='#2E7D32', lw=1.6, style='->'):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle=style, color=color, linewidth=lw,
                connectionstyle="arc3,rad=0", shrinkA=1, shrinkB=3), zorder=6)

def label_room(ax, x, y, w, h, name, area="", fontsize=6, color='#1A1A1A', bg_alpha=0.0):
    ax.text(x+w/2, y+h/2+0.15, name, ha='center', va='center', fontsize=fontsize, weight='bold', color=color, zorder=7,
            wrap=True)
    if area:
        ax.text(x+w/2, y+h/2-0.35, area, ha='center', va='center', fontsize=4.5, color='#555555', zorder=7)

def draw_grid_bubble(ax, x, y, text, r=0.35):
    ax.add_patch(Circle((x, y), r, facecolor='white', edgecolor='#0F2A52', linewidth=0.8, zorder=8))
    ax.text(x, y, text, ha='center', va='center', fontsize=5, weight='bold', color='#0F2A52', zorder=9)

def draw_section_mark(ax, x, y, direction, label):
    # direction: 'right','left','up','down' = viewing direction
    s = 0.5
    ax.add_patch(Circle((x, y), s*0.55, facecolor='#0F2A52', edgecolor='#0F2A52', zorder=8))
    ax.text(x, y, label, ha='center', va='center', fontsize=5, weight='bold', color='white', zorder=9)
    if direction == 'right':
        ax.annotate("", xy=(x+1.2, y), xytext=(x+0.3, y), arrowprops=dict(arrowstyle="-|>", color='#0F2A52', lw=1.2), zorder=8)
    elif direction == 'left':
        ax.annotate("", xy=(x-1.2, y), xytext=(x-0.3, y), arrowprops=dict(arrowstyle="-|>", color='#0F2A52', lw=1.2), zorder=8)
    elif direction == 'up':
        ax.annotate("", xy=(x, y+1.2), xytext=(x, y+0.3), arrowprops=dict(arrowstyle="-|>", color='#0F2A52', lw=1.2), zorder=8)
    elif direction == 'down':
        ax.annotate("", xy=(x, y-1.2), xytext=(x, y-0.3), arrowprops=dict(arrowstyle="-|>", color='#0F2A52', lw=1.2), zorder=8)

def bring_text_to_front(ax):
    for txt in ax.texts:
        txt.set_zorder(12)
    for ann in getattr(ax, 'texts', []):
        pass

def save_sheet(fig, basename, dpi_png=170):
    import os
    os.makedirs("drawings", exist_ok=True)
    # NOTE: no bbox_inches='tight' - it crops portrait sheets wrongly. Use full-figure save.
    fig.savefig(f"drawings/{basename}.png", dpi=dpi_png, facecolor='white')
    print(f"saved drawings/{basename}.png")
    fig.savefig(f"drawings/{basename}.pdf", facecolor='white')
    print(f"saved drawings/{basename}.pdf")
    fig.savefig(f"drawings/{basename}.svg", facecolor='white')
    print(f"saved drawings/{basename}.svg")
