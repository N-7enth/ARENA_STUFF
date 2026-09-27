# A301 - Sections: A-A Longitudinal (N-S) + B-B Cross (E-W)
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import numpy as np
from arch_lib import *

L = 39.40
W = 10.17
EAVES = 8.0
RIDGE = 12.0

def draw_longitudinal(ax, ox, oy):
    # Section A-A: cut N-S through centre (ridge). Length L (S left, N right), height to ridge 12.
    # Ground
    ax.plot([ox-1.5, ox+L+1.5], [oy, oy], color='#212121', lw=1.4, zorder=6)
    for xx in np.arange(ox-1.5, ox+L+1.5, 1.2):
        ax.plot([xx, xx-0.4], [oy, oy-0.5], color='#9E9E9E', lw=0.5, zorder=5)
    # Foundation hint (strip + pads at frames)
    ax.add_patch(Rectangle((ox, oy-0.8), L, 0.8, facecolor='#BCAAA4', edgecolor='#4E342E', linewidth=0.7, zorder=3))
    ax.text(ox+L/2, oy-0.4, "STRIP / PAD FOUNDATIONS (TBC by engineer)  •  150 DPM + 150 power-float slab", ha='center', va='center', fontsize=3.4, color='#3E2723', style='italic', zorder=4)
    # South wall (left, G+mezz) + North wall (right)
    # South wall: ground to eaves? Actually gable end: to ridge? Section through centre cuts gable walls at ridge height (12m). So end walls go to 12m (triangular? No, section shows wall profile: south wall vertical to 12m (apex)? The gable end wall is triangular (apex at centre). Section through centre (apex line) cuts the apex, so wall height =12m. Similarly north wall 12m.
    # Draw end walls as 0.3 thick
    ax.add_patch(Rectangle((ox, oy), 0.3, RIDGE, facecolor='#B0BEC5', edgecolor='#0F2A52', linewidth=1.2, zorder=5))
    ax.add_patch(Rectangle((ox+L-0.3, oy), 0.3, RIDGE, facecolor='#B0BEC5', edgecolor='#0F2A52', linewidth=1.2, zorder=5))
    ax.text(ox+0.15, oy+6, "S\nWALL", ha='center', va='center', fontsize=3.2, weight='bold', color='#0F2A52', rotation=90, zorder=7)
    ax.text(ox+L-0.15, oy+6, "N\nWALL", ha='center', va='center', fontsize=3.2, weight='bold', color='#0F2A52', rotation=90, zorder=7)
    # Roof (ridge line at 12m, purlins). Show as double line (sheet + purlin) + vents.
    ax.plot([ox, ox+L], [oy+RIDGE, oy+RIDGE], color='#0F2A52', lw=2.0, zorder=7)
    ax.plot([ox, ox+L], [oy+RIDGE-0.3, oy+RIDGE-0.3], color='#78909C', lw=0.8, zorder=6)
    ax.text(ox+L/2, oy+RIDGE+0.3, "RIDGE +12.00 (section on centre-line)  •  PURLINS + VENTS", ha='center', va='bottom', fontsize=3.8, color='#0F2A52', style='italic',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#0F2A52"), zorder=8)
    # vents (on ridge)
    for vx in [6.4, 12.4, 18.4, 24.4, 30.4, 36.4]:
        ax.add_patch(Rectangle((ox+vx-0.5, oy+RIDGE-0.1), 1.0, 0.7, facecolor='#37474F', edgecolor='white', linewidth=0.6, zorder=8))
        ax.annotate("", xy=(ox+vx, oy+RIDGE+1.2), xytext=(ox+vx, oy+RIDGE+0.6),
                    arrowprops=dict(arrowstyle="->", color='#E53935', lw=1.2), zorder=9)
    ax.text(ox+18.4, oy+RIDGE+1.5, "HOT AIR EXHAUST", ha='center', va='bottom', fontsize=3.6, weight='bold', color='#C62828', zorder=9)
    # Portal frames (transverse, seen edge-on as verticals? Actually frames span E-W, section N-S shows them as vertical lines at grid positions? The columns are at sides (E/W), not on centre-line, so section doesn't cut them. Show as dashed (behind/ahead)? Better show as faint verticals with note "portal frames @6m (behind)".
    bays = [3.4,6,6,6,6,6,6]
    gx = ox
    grid_xs = [gx]
    for b in bays:
        gx+=b; grid_xs.append(gx)
    for i, gxx in enumerate(grid_xs):
        ax.plot([gxx, gxx], [oy, oy+EAVES], color=COLORS['steel'], lw=0.6, linestyle=(0,(4,3)), alpha=0.5, zorder=4)
        # rafter hint? (from eaves sides to ridge centre - in longitudinal, rafters run E-W, seen end-on? Show as small triangle? Skip.)
        draw_grid_bubble(ax, gxx, oy-1.1, f"{i+1}", r=0.32)
    ax.text(ox-0.6, oy-1.1, "S", ha='right', va='center', fontsize=4, weight='bold', color='#0F2A52')
    ax.text(ox+L+0.6, oy-1.1, "N", ha='left', va='center', fontsize=4, weight='bold', color='#0F2A52')

    # Mezzanine (south 9.4m): slab at +4.0 + rooms + railing + stair
    mz_end = ox+9.4
    # slab
    ax.add_patch(Rectangle((ox+0.3, oy+4.0-0.2), 9.4-0.6, 0.2, facecolor='#FF8F00', edgecolor='#4E342E', linewidth=0.8, zorder=7))
    ax.text(ox+4.7, oy+3.6, "MEZZ SLAB +4.00 (150 RC)", ha='center', va='top', fontsize=3.4, color='#4E342E', weight='bold', zorder=8)
    # mezz rooms: show partitions (offices below? Actually section cuts through? Assume cut through lobby/admin/MD? Show generic: south wall to roof, mid partitions)
    # office partitions (vertical)
    ax.plot([ox+4.0, ox+4.0], [oy+4.0, oy+7.0], color='#5D4037', lw=1.0, zorder=7)  # between lobby/admin?
    ax.text(ox+2.0, oy+5.5, "LOBBY", ha='center', va='center', fontsize=3.4, color='#4E342E', zorder=8)
    ax.text(ox+6.5, oy+5.5, "OFFICES", ha='center', va='center', fontsize=3.4, color='#1A237E', zorder=8)
    # mezz ceiling? Open to roof (no ceiling, exposed). Show height dim 4.0 to eaves? Actually mezz at 4.0, eaves at 8.0 (side walls), ridge at 12.0. In longitudinal (centre), roof at 12.0, so mezz to roof =8.0m. Spacious. Note: offices open to roof? Better with ceiling at +7.0 (3.0 above mezz) + roof void above for services. Show suspended ceiling at +7.0.
    ax.plot([ox+0.3, mz_end], [oy+7.0, oy+7.0], color='#78909C', lw=0.7, linestyle=(0,(5,3)), zorder=6)
    ax.text(ox+4.7, oy+7.2, "SUSP. CEILING +7.00 (offices)", ha='center', va='bottom', fontsize=3.2, color='#546E7A', style='italic', zorder=8)
    # railing at mezz edge (north edge)
    ax.plot([mz_end, mz_end], [oy+4.0, oy+5.1], color='#D32F2F', lw=1.6, zorder=8)
    ax.text(mz_end+0.3, oy+4.55, "RAIL 1.1", ha='left', va='center', fontsize=3.2, color='#D32F2F', weight='bold', zorder=8)
    # stair (south end, schematic side view: flight up from ground to mezz)
    # stair run: from x=ox+1.0 (ground) up to x=ox+3.5 (mezz)? Rise 4.0, going ~? Show steps.
    st_x0, st_x1 = ox+0.8, ox+3.8
    n_steps = 12
    for i in range(n_steps+1):
        xx = st_x0 + (st_x1-st_x0)*i/n_steps
        yy = oy + 4.0*i/n_steps
        if i < n_steps:
            xx2 = st_x0 + (st_x1-st_x0)*(i+1)/n_steps
            ax.plot([xx, xx2], [yy, yy], color='#4E342E', lw=0.8, zorder=7)
            ax.plot([xx2, xx2], [yy, yy+4.0/n_steps], color='#4E342E', lw=0.8, zorder=7)
    flow_arrow(ax, (st_x0+0.3, oy+0.5), (st_x1-0.3, oy+3.5), color='#4E342E', lw=1.2)
    ax.text((st_x0+st_x1)/2, oy+1.2, "STAIR UP", ha='center', va='center', fontsize=3.2, weight='bold', color='#4E342E', rotation=35, zorder=8)
    # ground rooms south: reception (below lobby) + QC (below staff?) + FG (below utilities? Section through centre: cuts QC? QC at x W (0-5.5), FG at E (5.5-10.17). Centre x=5.085 is just west of divider (5.5), so section cuts QC/reception (west side), not FG. Show reception + QC.
    ax.plot([ox+5.0, ox+5.0], [oy, oy+4.0], color='#00796B', lw=1.0, zorder=6)  # reception/QC wall (at plan y=5.0 from S)
    ax.text(ox+2.5, oy+2.0, "RECEPTION", ha='center', va='center', fontsize=3.6, weight='bold', color='#5D4037', zorder=7)
    ax.text(ox+7.2, oy+2.0, "QC LAB", ha='center', va='center', fontsize=3.6, weight='bold', color='#00695C', zorder=7)
    # FG note (beside section, east): dashed
    ax.text(ox+7.2, oy+0.8, "(FG STORE alongside, E)", ha='center', va='center', fontsize=3.0, color='#1565C0', style='italic', zorder=7)

    # Machines along hall (west row cut? Section through centre (aisle), machines are to sides (W/E), so show as background (dashed/elevations)? Better: show extrusion towers (west) as background elevations (tall), cutting (east) as background. Draw as light outlines behind.
    # Extrusion towers at plan y (from S): M1 ~29.3? Let's compute plan y from ground sheet: nz_bot = by0+33.4? Actually ground: by0=0, nz_bot=33.4, machines at nz_bot-4.1 etc. So plan y (from S): M1 y=29.3-32.7? Wait machines_w yy = nz_bot-4.1=29.3 (bottom), h=3.4, top=32.7. In section, x = ox + plan_y (S left). So M1 x=ox+29.3..32.7. Similarly M2 y=25.1-28.5, M3 y=20.5-23.9, M4 y=15.9-19.3. East row same y.
    # Draw west towers (tall 9m) as background (light blue, dashed front?)
    for (py_bot, lab) in [(29.3,"M1"),(25.1,"M2"),(20.5,"M3"),(15.9,"M4")]:
        mx0, mx1 = ox+py_bot, ox+py_bot+3.4
        h = 4.0 if lab=="M1" else 9.0  # M1 mixing 4m, extrusion 9m
        ec = '#283593' if lab!="M1" else '#C1272D'
        fc = '#E8EAF6' if lab!="M1" else '#FFEBEE'
        ax.add_patch(Rectangle((mx0, oy), mx1-mx0, h, facecolor=fc, edgecolor=ec, linewidth=1.0, linestyle=(0,(4,2)) if lab!="M1" else '-', zorder=5))
        ax.text((mx0+mx1)/2, oy+h/2, lab, ha='center', va='center', fontsize=3.8, weight='bold', color=ec, zorder=6)
        if lab != "M1":
            # tower top (narrow)
            ax.add_patch(Rectangle(((mx0+mx1)/2-0.5, oy+h), 1.0, 0.8, facecolor=ec, edgecolor='none', alpha=0.3, zorder=5))
            ax.text((mx0+mx1)/2, oy+h+1.0, "≈9m", ha='center', va='bottom', fontsize=3.0, color=ec, style='italic', zorder=6)
    # East row (cutting, lower 2.5m) as foreground? Draw solid red, lower height, in front (darker).
    for (py_bot, lab) in [(29.3,"M7"),(25.1,"M8"),(20.5,"M9"),(15.9,"M11")]:
        mx0, mx1 = ox+py_bot+0.4, ox+py_bot+3.0  # slightly inset to distinguish from west
        ax.add_patch(Rectangle((mx0, oy), mx1-mx0, 2.5, facecolor='#FFEBEE', edgecolor='#C1272D', linewidth=1.0, zorder=6))
        ax.text((mx0+mx1)/2, oy+1.25, lab, ha='center', va='center', fontsize=3.2, weight='bold', color='#C1272D', zorder=7)
    ax.text(ox+24, oy+10.5, "M2–M4 EXTRUSION TOWERS (W, behind)  •  M7–M9 CUT/SEAL (E, front)", ha='center', va='center', fontsize=3.6, color='#333333', style='italic',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#999999"), zorder=8)

    # North zone: raw store (W) + printing (E). Section through centre (x=5.085, just W of divider 5.5) cuts raw store (W). Show raw store wall + pallets + printing beyond (dashed).
    nz_bot = ox+L-6.0
    ax.plot([nz_bot, nz_bot], [oy, oy+4.0], color='#2E7D32', lw=1.2, zorder=6)  # raw south wall (4m high? Full height? Raw store full height to eaves? Show to 4m with open above? Actually stores full height? Keep 4m partition + open above for ventilation? Better full height? For fire, full height? Let's show 3m partition + mesh above? Simplify: full height to eaves? Draw to 8m? Hmm section shows wall to eaves (8m)? But longitudinal section at centre: raw store divider? The raw south wall spans E-W at plan y=33.4, section cuts it, height? Partition 3m? Or full? Let's show 3m + note.
    ax.text(nz_bot+3.0, oy+2.0, "RAW STORE", ha='center', va='center', fontsize=3.6, weight='bold', color='#1B5E20', zorder=7)
    # pallets in raw
    for i in range(3):
        ax.add_patch(Rectangle((nz_bot+0.8+i*1.4, oy), 1.1, 1.0, facecolor='#D7CCC8', edgecolor='#5D4037', linewidth=0.6, zorder=7))
    # printing (east, beyond section): dashed box + extract duct up to roof
    ax.add_patch(Rectangle((nz_bot+0.5, oy), 5.0, 4.0, facecolor='none', edgecolor='#7B1FA2', linewidth=0.8, linestyle=(0,(4,3)), zorder=5))
    ax.text(nz_bot+3.0, oy+4.4, "PRINTING (E, beyond) + duct", ha='center', va='bottom', fontsize=3.2, color='#6A1B9A', style='italic', zorder=7)
    # duct vertical to roof
    ax.plot([nz_bot+3.0, nz_bot+3.0], [oy+4.0, oy+RIDGE], color='#6A1B9A', lw=1.2, linestyle=(0,(4,2)), zorder=6)
    ax.add_patch(Circle((nz_bot+3.0, oy+RIDGE+0.3), 0.3, facecolor='#6A1B9A', edgecolor='white', linewidth=0.6, zorder=8))

    # flow arrow along hall (southward? Actually flow N→S, so arrow right-to-left (N right, S left))
    flow_arrow(ax, (ox+L-2, oy+3.2), (ox+11, oy+3.2), color='#2E7D32', lw=1.6)
    ax.text(ox+22, oy+3.6, "MATERIAL FLOW  N → S  (Raw → FG)", ha='center', va='bottom', fontsize=4, weight='bold', color='#2E7D32',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2E7D32"), zorder=9)

    # levels left
    for lev, lab in [(0,"+0.00"),(4.0,"+4.00 MEZZ"),(7.0,"+7.00 CLG"),(8.0,"+8.00 EAVES*"),(12.0,"+12.00 RIDGE")]:
        ax.plot([ox-1.5, ox], [oy+lev, oy+lev], color='#0F2A52', lw=0.7, zorder=6)
        ax.text(ox-1.7, oy+lev, lab, ha='right', va='center', fontsize=3.4, color='#0F2A52', zorder=8)
    ax.text(ox-1.7, oy+9.5, "*EAVES at sides;\nridge on centre", ha='right', va='center', fontsize=3.0, color='#546E7A', style='italic')
    # length dim
    dim_linear(ax, (ox, oy), (ox+L, oy), offset=-2.4, text=f"{L:.2f}  (9.40 mezz + 24.00 hall + 6.00 N-zone)", fontsize=5, color='#0F2A52')
    # title
    ax.text(ox+L/2, oy-3.8, "SECTION A—A  •  LONGITUDINAL  (N–S through centre, looking EAST)", ha='center', va='top', fontsize=6.5, weight='bold', color='#0F2A52')
    ax.text(ox+L/2, oy-4.6, "S (left) → N (right)  •  Mezz south + extrusion towers + raw/print north  •  Ridge +12.0 constant on centre-line", ha='center', va='top', fontsize=4, color='#555555', style='italic')

def draw_cross(ax, ox, oy):
    # Section B-B: cut E-W through extrusion (looking NORTH). Width W (W left, E right), height to ridge 12.
    # Ground + foundations (pad footings at columns)
    ax.plot([ox-1.5, ox+W+1.5], [oy, oy], color='#212121', lw=1.4, zorder=6)
    for xx in np.arange(ox-1.5, ox+W+1.5, 0.8):
        ax.plot([xx, xx-0.4], [oy, oy-0.5], color='#9E9E9E', lw=0.5, zorder=5)
    # pads
    for px in [ox, ox+W]:
        ax.add_patch(Rectangle((px-0.9, oy-1.0), 1.8, 0.6, facecolor='#BCAAA4', edgecolor='#4E342E', linewidth=0.7, zorder=4))
        ax.add_patch(Rectangle((px-0.4, oy-0.4), 0.8, 0.4, facecolor='#8D6E63', edgecolor='#4E342E', linewidth=0.6, zorder=5))
    ax.text(ox+W/2, oy-0.7, "PAD FOUNDATIONS 1.8×1.8 (TBC)", ha='center', va='center', fontsize=3.4, color='#3E2723', style='italic', zorder=6)
    # Columns (steel UB, 8m)
    col_w = 0.3
    ax.add_patch(Rectangle((ox-0.05, oy), col_w, EAVES, facecolor=COLORS['steel'], edgecolor='white', linewidth=0.6, zorder=7))
    ax.add_patch(Rectangle((ox+W-0.25, oy), col_w, EAVES, facecolor=COLORS['steel'], edgecolor='white', linewidth=0.6, zorder=7))
    ax.text(ox+0.1, oy+4, "UB\nCOLUMN", ha='center', va='center', fontsize=3.2, weight='bold', color='white', rotation=90, zorder=8)
    ax.text(ox+W-0.1, oy+4, "UB\nCOLUMN", ha='center', va='center', fontsize=3.2, weight='bold', color='white', rotation=90, zorder=8)
    # Walls (block + cladding, outside columns)
    ax.add_patch(Rectangle((ox-0.35, oy), 0.25, EAVES, facecolor='#B0BEC5', edgecolor='#0F2A52', linewidth=0.9, zorder=6))
    ax.add_patch(Rectangle((ox+W+0.1, oy), 0.25, EAVES, facecolor='#B0BEC5', edgecolor='#0F2A52', linewidth=0.9, zorder=6))
    # Rafters (from eaves to ridge)
    cx = ox+W/2
    ax.plot([ox, cx], [oy+EAVES, oy+RIDGE], color=COLORS['steel'], lw=2.4, zorder=7)
    ax.plot([cx, ox+W], [oy+RIDGE, oy+EAVES], color=COLORS['steel'], lw=2.4, zorder=7)
    # haunch hints
    ax.plot([ox, ox+1.2], [oy+EAVES, oy+EAVES-0.8], color=COLORS['steel'], lw=1.4, zorder=7)
    ax.plot([ox+W, ox+W-1.2], [oy+EAVES, oy+EAVES-0.8], color=COLORS['steel'], lw=1.4, zorder=7)
    # Roof sheets (parallel above rafters)
    ax.plot([ox-0.45, cx], [oy+EAVES+0.15, oy+RIDGE+0.15], color='#0F2A52', lw=1.6, zorder=8)
    ax.plot([cx, ox+W+0.45], [oy+RIDGE+0.15, oy+EAVES+0.15], color='#0F2A52', lw=1.6, zorder=8)
    # purlins (small squares on rafters)
    for frac in [0.2, 0.4, 0.6, 0.8]:
        # west
        wx = ox + (cx-ox)*frac
        wy = oy+EAVES + (RIDGE-EAVES)*frac
        ax.add_patch(Rectangle((wx-0.12, wy-0.05), 0.24, 0.15, facecolor='#78909C', edgecolor='white', linewidth=0.4, zorder=8))
        # east
        ex = cx + (ox+W-cx)*frac
        ax.add_patch(Rectangle((ex-0.12, wy-0.05), 0.24, 0.15, facecolor='#78909C', edgecolor='white', linewidth=0.4, zorder=8))
    # skylights (translucent segments on slopes at 1/3,2/3)
    for frac in [0.33, 0.66]:
        # west: segment 1.0m along slope? In cross-section, skylight width 1.0m (E-W horizontal projection? Actually strip 1.0m wide across slope). Slope length 6.47, horizontal 5.085. 1.0m across slope ≈0.786 horizontal? Simplify: draw 0.9m segment along slope.
        # compute slope points
        import math
        slope_len = math.hypot(W/2, RIDGE-EAVES)
        # distance along slope from eaves: frac*slope_len
        for side in [-1, 1]:
            # side -1 west, +1 east
            d = frac*slope_len
            # unit along slope from eaves to ridge: west: (+W/2, +4)/slope_len; east: (-W/2, +4)/slope_len
            if side == -1:
                ux, uy = (W/2)/slope_len, (RIDGE-EAVES)/slope_len
                ex0, ey0 = ox, oy+EAVES
            else:
                ux, uy = -(W/2)/slope_len, (RIDGE-EAVES)/slope_len
                ex0, ey0 = ox+W, oy+EAVES
            seg = 1.0  # along slope
            x1, y1 = ex0+ux*(d-seg/2), ey0+uy*(d-seg/2)
            x2, y2 = ex0+ux*(d+seg/2), ey0+uy*(d+seg/2)
            ax.plot([x1, x2], [y1, y2], color='#0288D1', lw=4.5, solid_capstyle='butt', zorder=9)
            ax.plot([x1, x2], [y1+0.15, y2+0.15], color='#B3E5FC', lw=2.0, zorder=10)
    ax.text(ox+1.5, oy+10.2, "SKYLIGHTS", ha='center', va='center', fontsize=3.2, color='#01579B', weight='bold',
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#0288D1"), zorder=11)
    ax.text(ox+W-1.5, oy+10.2, "SKYLIGHTS", ha='center', va='center', fontsize=3.2, color='#01579B', weight='bold',
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#0288D1"), zorder=11)
    # ridge vent (section through vent? Show one)
    ax.add_patch(Rectangle((cx-0.5, oy+RIDGE+0.15), 1.0, 0.6, facecolor='#37474F', edgecolor='white', linewidth=0.6, zorder=9))
    ax.annotate("", xy=(cx, oy+RIDGE+1.4), xytext=(cx, oy+RIDGE+0.75),
                arrowprops=dict(arrowstyle="->", color='#E53935', lw=1.2), zorder=10)
    ax.text(cx+0.8, oy+RIDGE+1.1, "VENT", ha='left', va='center', fontsize=3.4, weight='bold', color='#C62828', zorder=10)
    # gutters
    for gx in [ox-0.35, ox+W+0.1]:
        ax.add_patch(Rectangle((gx-0.15, oy+EAVES-0.3), 0.4, 0.3, facecolor='#263238', edgecolor='white', linewidth=0.4, zorder=8))
    # crane beam? (optional, 5T at +6m?) Show dashed + note "optional crane beam (TBC)"
    ax.plot([ox+0.3, ox+W-0.3], [oy+6.0, oy+6.0], color='#8D6E63', lw=1.0, linestyle=(0,(5,3)), zorder=5)
    ax.text(ox+W/2, oy+6.2, "OPTIONAL CRANE BEAM 5T @+6.0 (TBC)", ha='center', va='bottom', fontsize=3.2, color='#8D6E63', style='italic', zorder=6)

    # Machines in cross: west extrusion tower (tall 9m, but eaves 8m? Tower 9m exceeds eaves, fits under ridge? At west side (x near wall), roof height =8m (eaves). Tower 9m would poke through roof! Problem: extrusion towers H≈9m need 9m clear, but eaves 8m at walls. Towers must be inset from walls where roof is higher. At distance d from wall (west), roof height =8 + (4/5.085)*(5.085-d)? Wait ridge centre, eaves sides. Height at distance x from west wall (0 at wall, 5.085 at ridge): h(x)=8 + (4/5.085)*x. For h≥9.5 (tower 9 + clearance 0.5), need x≥(1.5/4)*5.085=1.907m from wall. Our west machines at x=0.55-3.5 from wall (west_x=0.55, w=2.95, so x 0.55-3.5). Front edge 0.55 (h=8.43), back edge 3.5 (h=10.75). Tower footprint 2.95 wide, tallest part should be on east side (toward ridge) where higher. Okay if towers placed with tall mast on east side. Note this in section: show tower with mast on east (ridge side).
    # Draw west tower: base 2.95 wide, height 3m (base) + mast 1.0 wide, 9m total on east side.
    wx0 = ox+0.55
    wx1 = ox+0.55+2.95
    # base
    ax.add_patch(Rectangle((wx0, oy), wx1-wx0, 3.0, facecolor='#E8EAF6', edgecolor='#283593', linewidth=1.2, zorder=6))
    ax.text((wx0+wx1)/2, oy+1.5, "M2\nEXTRUSION", ha='center', va='center', fontsize=3.6, weight='bold', color='#283593', zorder=7)
    # mast (east side, tall)
    mast_x0, mast_x1 = wx1-1.0, wx1
    ax.add_patch(Rectangle((mast_x0, oy), mast_x1-mast_x0, 9.0, facecolor='#C5CAE9', edgecolor='#283593', linewidth=1.0, zorder=7))
    ax.text((mast_x0+mast_x1)/2, oy+6.5, "MAST\n9m", ha='center', va='center', fontsize=3.0, weight='bold', color='#1A237E', rotation=90, zorder=8)
    # clearance dim: mast top 9.0, roof above at x=mast (≈2.5-3.5 from wall, h≈9.97-10.75), clearance ~1-1.75m. Show arrow.
    roof_at_mast = EAVES + (RIDGE-EAVES)*( (mast_x0+mast_x1)/2 - ox )/(W/2)
    ax.annotate("", xy=((mast_x0+mast_x1)/2, roof_at_mast+oy-0.2), xytext=((mast_x0+mast_x1)/2, oy+9.0+0.1),
                arrowprops=dict(arrowstyle="<->", color='#2E7D32', linewidth=1.0), zorder=8)
    ax.text((mast_x0+mast_x1)/2+0.4, (oy+9.0+oy+roof_at_mast)/2, "CLR", ha='left', va='center', fontsize=3.0, color='#2E7D32', weight='bold', zorder=8)

    # East cutting machine (low 2.5m)
    ex1 = ox+W-0.55
    ex0 = ex1-2.95
    ax.add_patch(Rectangle((ex0, oy), ex1-ex0, 2.5, facecolor='#FFEBEE', edgecolor='#C1272D', linewidth=1.2, zorder=6))
    ax.text((ex0+ex1)/2, oy+1.25, "M8\nCUT/SEAL", ha='center', va='center', fontsize=3.6, weight='bold', color='#C1272D', zorder=7)

    # Central aisle + forklift hint
    aisle_c = ox+W/2
    ax.add_patch(Rectangle((aisle_c-1.18, oy), 2.37, 0.08, facecolor='#AED581', edgecolor='#558B2F', linewidth=0.6, zorder=7))
    ax.text(aisle_c, oy+0.35, "AISLE 2.37m", ha='center', va='bottom', fontsize=3.2, color='#33691E', weight='bold', zorder=8)
    # eaves height dim (left)
    # levels
    for lev, lab in [(0,"+0.00"),(4.0,"+4.00*"),(6.0,"+6.00 CRANE?"),(8.0,"+8.00 EAVES"),(9.0,"+9.00 MAST"),(12.0,"+12.00 RIDGE")]:
        ax.plot([ox-1.4, ox-0.35], [oy+lev, oy+lev], color='#0F2A52', lw=0.6, zorder=6)
        ax.text(ox-1.6, oy+lev, lab, ha='right', va='center', fontsize=3.2, color='#0F2A52', zorder=8)
    ax.text(ox-1.6, oy+2.0, "*mezz only\nat S end", ha='right', va='center', fontsize=2.8, color='#795548', style='italic')
    # span dim
    dim_linear(ax, (ox, oy), (ox+W, oy), offset=-1.8, text=f"{W:.2f}  (portal span)", fontsize=5, color='#0F2A52')
    # pitch note
    ax.text(cx, oy+RIDGE-1.2, "38°\n(4.0 / 5.085)", ha='center', va='center', fontsize=3.6, weight='bold', color='#0F2A52',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#0F2A52"), zorder=10)
    # title
    ax.text(ox+W/2, oy-3.0, "SECTION B—B  •  CROSS  (E–W through extrusion, looking NORTH)", ha='center', va='top', fontsize=6.5, weight='bold', color='#0F2A52')
    ax.text(ox+W/2, oy-3.8, "W (left) → E (right)  •  Portal frame + extrusion mast (W) + cut/seal (E)  •  Note mast clearance under slope", ha='center', va='top', fontsize=4, color='#555555', style='italic')

def build():
    fig, ax = setup_sheet(figsize=(16.8, 11.9))
    ax.set_xlim(0, 62)
    ax.set_ylim(0, 45)
    draw_border(ax, 0, 0, 62, 45)
    draw_title_block(ax, 30, 0.7, 31, "A301", "SECTIONS  •  A-A LONGITUDINAL + B-B CROSS", "1:100")

    ax.text(31, 43.3, "SECTIONS  —  A-A LONGITUDINAL (39.40m)  •  B-B CROSS (10.17m span)", ha='center', va='center', fontsize=11, weight='bold', color='#0F2A52')
    ax.text(31, 42.3, "Portal steel @6.0m  •  Mezz +4.0 south  •  Extrusion masts ≈9m (check clearance)  •  Ridge vents + skylights + print extract", ha='center', va='center', fontsize=5.5, color='#333333')

    # Longitudinal on top (long, needs 39.4 + margins). Place at ox=4, oy=24 (height to 12+vents ~14, top y=38). Fits below header (42.3).
    draw_longitudinal(ax, 4, 24)
    # Cross below-left + notes below-right
    draw_cross(ax, 4, 6)

    # Structural notes (bottom-right, beside cross)
    nx, ny = 20, 6
    ax.add_patch(Rectangle((nx, ny), 20, 13.5, facecolor='#ECEFF1', edgecolor='#0F2A52', linewidth=1.0, zorder=4))
    ax.add_patch(Rectangle((nx, ny+11.8), 20, 1.7, facecolor=COLORS['title_bg'], edgecolor='none', zorder=5))
    ax.text(nx+10, ny+12.65, "STRUCTURE & BUILD NOTES", ha='center', va='center', fontsize=5.5, weight='bold', color='white', zorder=6)
    notes = [
        "• Portal frames: UB columns + rafters @6.0m (7 frames).",
        "• Eaves +8.0, ridge +12.0 (38°). Purlins RHS + sag rods.",
        "• Walls: block 1.2m + cladding; printing room 215 block full ht.",
        "• Floor: 150 slab + DPM + power-float; saw cuts @3m.",
        "• Mezz: 150 RC on UB/APFC + 1.1 rail; pad/strip footings.",
        "• Extrusion masts 9m: keep tall side to ridge (see B-B).",
        "• Crane beam 5T optional @+6.0 (confirm with vendor).",
        "• Fire: extinguishers + hose reels + exit signs; print room 2hr.",
        "• Elect: 3-ph to machines + panels on mezz; earthing + LPS.",
        "• Drain: gutters→RWP→soakaway; WCs→septic (E); bund chemicals.",
        "• Verify ALL with structural/M&E engineers + Lagos approvals.",
    ]
    for i, t in enumerate(notes):
        ax.text(nx+0.5, ny+10.7-i*0.92, t, ha='left', va='center', fontsize=3.9, color='#212121', zorder=7)

    # Key (bottom-left, below cross title? Actually cross title at y=3? Overlaps finishes? Let's place key top-right?)
    # Place section key (cut locations) mini plan at top-right
    kx, ky = 48, 24
    ax.add_patch(Rectangle((kx, ky), 12, 14.5, facecolor='white', edgecolor='#0F2A52', linewidth=1.0, zorder=4))
    ax.text(kx+6, ky+13.7, "KEY  (cuts)", ha='center', va='center', fontsize=5.5, weight='bold', color='#0F2A52', zorder=6)
    # mini building
    mx0, my0, mw, mh = kx+4.2, ky+2.5, 3.6, 9.5
    ax.add_patch(Rectangle((mx0, my0), mw, mh, facecolor='#EAF0FA', edgecolor='#0F2A52', linewidth=1.0, zorder=5))
    # A-A line (N-S centre, arrows east)
    ax.plot([mx0+mw/2, mx0+mw/2], [my0-0.5, my0+mh+0.5], color='#0F2A52', lw=1.4, zorder=6)
    for yy in [my0-0.5, my0+mh+0.5]:
        ax.annotate("", xy=(mx0+mw/2+0.8, yy), xytext=(mx0+mw/2, yy),
                    arrowprops=dict(arrowstyle="-|>", color='#0F2A52', lw=1.0), zorder=7)
    ax.text(mx0+mw/2, my0-1.0, "A", ha='center', va='center', fontsize=5, weight='bold', color='white',
            bbox=dict(boxstyle="circle,pad=0.3", fc="#0F2A52", ec="none"), zorder=8)
    ax.text(mx0+mw/2, my0+mh+1.0, "A", ha='center', va='center', fontsize=5, weight='bold', color='white',
            bbox=dict(boxstyle="circle,pad=0.3", fc="#0F2A52", ec="none"), zorder=8)
    # B-B line (E-W at extrusion, arrows north)
    bby = my0+4.5
    ax.plot([mx0-0.8, mx0+mw+0.8], [bby, bby], color='#0F2A52', lw=1.4, zorder=6)
    for xx in [mx0-0.8, mx0+mw+0.8]:
        ax.annotate("", xy=(xx, bby+0.8), xytext=(xx, bby),
                    arrowprops=dict(arrowstyle="-|>", color='#0F2A52', lw=1.0), zorder=7)
    ax.text(mx0-1.3, bby, "B", ha='center', va='center', fontsize=5, weight='bold', color='white',
            bbox=dict(boxstyle="circle,pad=0.3", fc="#0F2A52", ec="none"), zorder=8)
    ax.text(mx0+mw+1.3, bby, "B", ha='center', va='center', fontsize=5, weight='bold', color='white',
            bbox=dict(boxstyle="circle,pad=0.3", fc="#0F2A52", ec="none"), zorder=8)
    ax.text(mx0+mw/2, my0+mh-1.0, "N", ha='center', va='center', fontsize=4, weight='bold', color='#0F2A52')
    ax.text(kx+6, ky+0.9, "A-A: centre N-S\nB-B: extrusion E-W", ha='center', va='center', fontsize=3.8, color='#333333', style='italic')

    bring_text_to_front(ax)
    save_sheet(fig, "A301_sections")
    plt.close(fig)

if __name__ == "__main__":
    build()
