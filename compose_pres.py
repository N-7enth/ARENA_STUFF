# Presentation sheets in sample visual format (rendered)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

NAVY = '#0F2A52'
ACCENT = '#1E88E5'
GREEN = '#2E7D32'
RED = '#C1272D'
PURPLE = '#6A1B9A'

def load_crop(path, y0=0.0, y1=1.0, x0=0.0, x1=1.0):
    img = mpimg.imread(path)
    h, w = img.shape[0], img.shape[1]
    return img[int(h*y0):int(h*y1), int(w*x0):int(w*x1)]

def place_img(fig, img, left, top, width, figW, figH):
    a = img.shape[1] / img.shape[0]
    hfrac = (width * figW / a) / figH
    bottom = top - hfrac
    ax = fig.add_axes([left, bottom, width, hfrac])
    ax.imshow(img)
    ax.axis('off')
    return ax, bottom, hfrac

def badge(ax, x, y, txt, fs=9, color=NAVY):
    ax.text(x, y, txt, transform=ax.transAxes, ha='center', va='center', fontsize=fs,
            weight='bold', color='white',
            bbox=dict(boxstyle='circle,pad=0.45', fc=color, ec='white', lw=1.2), zorder=10)

def tag(ax, x, y, txt, fs=7, color='#212121', ha='center'):
    ax.text(x, y, txt, transform=ax.transAxes, ha=ha, va='center', fontsize=fs,
            weight='bold', color=color,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=color, alpha=0.95), zorder=10)

# ================= P1 (landscape, 84m-sample style) =================
def build_P1():
    FW, FH = 16.8, 11.9
    fig = plt.figure(figsize=(FW, FH))
    fig.patch.set_facecolor('white')
    # border
    b = fig.add_axes([0.005, 0.01, 0.99, 0.98]); b.axis('off')
    b.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor=NAVY, lw=2, transform=b.transAxes))
    # header
    fig.text(0.5, 0.965, 'NYLON PRODUCTION & PACKAGING FACILITY', ha='center', va='center', fontsize=17, weight='bold', color=NAVY)
    fig.text(0.5, 0.94, 'PLANNED FOR EFFICIENT FLOW, QUALITY & SUSTAINABLE OPERATIONS  •  10.17m × 39.40m HALL  •  EAVES +8.0m / RIDGE +12.0m', ha='center', va='center', fontsize=8, color='#333333')

    # ---- Row 1: rendered plan ----
    plan = load_crop('renders/pres_plan_topdown.jpg', 0.27, 0.72)
    fig.text(0.015, 0.915, 'GROUND FLOOR PLAN', ha='left', va='center', fontsize=9, weight='bold', color=NAVY)
    fig.text(0.148, 0.915, 'SCALE INDICATIVE (see A102 for 1:100)', ha='left', va='center', fontsize=7, color='#555555')
    # north (plan rotated: N = left)
    from matplotlib.patches import FancyArrowPatch
    fig.patches.append(FancyArrowPatch((0.055, 0.895), (0.035, 0.895), arrowstyle='-|>', color=NAVY, lw=1.5, transform=fig.transFigure))
    fig.text(0.028, 0.895, 'N', ha='center', va='center', fontsize=9, weight='bold', color=NAVY)
    ax1, pbot, ph = place_img(fig, plan, 0.015, 0.885, 0.64, FW, FH)
    fig.text(0.335, 0.89, '39,400', ha='center', va='bottom', fontsize=8, weight='bold', color=NAVY)
    fig.text(0.662, (0.885 + pbot) / 2, '10,170', ha='center', va='center', fontsize=8, weight='bold', color=NAVY, rotation=90)
    # badges 1-8
    zones_x = [0.075, 0.215, 0.335, 0.475, 0.60, 0.705, 0.805, 0.945]
    for i, zx in enumerate(zones_x):
        badge(ax1, zx, 0.72, str(i + 1), fs=9)
    # flow arrows between badges
    for a, c in zip(zones_x[:-1], zones_x[1:]):
        ax1.annotate('', xy=(c - 0.035, 0.30), xytext=(a + 0.035, 0.30),
                     xycoords=ax1.transAxes, arrowprops=dict(arrowstyle='-|>', color=GREEN, lw=1.8))
    # utility core box
    ux = fig.add_axes([0.675, pbot, 0.31, ph]); ux.axis('off')
    ux.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor='#F5F7FA', edgecolor=NAVY, lw=1.2, transform=ux.transAxes))
    ux.text(0.5, 0.93, 'UTILITY CORE (SOUTH END)', ha='center', va='center', fontsize=8, weight='bold', color=NAVY, transform=ux.transAxes)
    for j, t in enumerate(['GATEHOUSE + 4.6m SLIDING GATE', 'SECURITY + LOBBY + STORE', 'POWER ROOM + GENERATOR', 'MEZZ UTILITIES + PANELS (U1)', 'BOREHOLE → TANKS (GRAVITY)', 'SEPTIC + SOAKAWAY (EAST)']):
        ux.text(0.06, 0.80 - j * 0.125, '•  ' + t, ha='left', va='center', fontsize=7, color='#212121', transform=ux.transAxes)
    # zone strip
    znames = ['RAW MATERIALS\nSTORE', 'MIXING &\nWEIGHING', 'BLOWN-FILM\nEXTRUSION', 'FLEXO PRINTING\n(WALLED)', 'CUTTING &\nHEAT-SEALING', 'QUALITY CONTROL\nLABORATORY', 'FINISHED GOODS\nSTORE', 'DISPATCH\n& LOADING']
    zy = pbot - 0.015
    for i, (zx, zn) in enumerate(zip(np.linspace(0.05, 0.62, 8), znames)):
        fig.text(zx, zy, str(i + 1), ha='center', va='top', fontsize=8, weight='bold', color='white',
                 bbox=dict(boxstyle='circle,pad=0.35', fc=NAVY, ec='none'))
        fig.text(zx, zy - 0.028, zn, ha='center', va='top', fontsize=6, weight='bold', color='#333333')
        if i < 7:
            fig.patches.append(FancyArrowPatch((zx + 0.022, zy - 0.012), (zx + 0.042, zy - 0.012), arrowstyle='-|>', color=ACCENT, lw=1.6, transform=fig.transFigure))

    # ---- Row 2: 3D cutaway band ----
    cut = load_crop('renders/pres_cutaway.jpg', 0.22, 0.90)
    ctop = zy - 0.075
    # left annotation column
    for j, t in enumerate(['CONTINUOUS RIDGE\nVENTILATORS', 'TRANSLUCENT\nSKYLIGHT STRIPS', 'PITCHED METAL ROOF\n38° (8m → 12m)']):
        fig.text(0.015, ctop - 0.05 - j * 0.075, t, ha='left', va='center', fontsize=6.5, weight='bold', color=NAVY)
    ax2, cbot, ch = place_img(fig, cut, 0.115, ctop, 0.56, FW, FH)
    # exhaust arrows
    for ex in [0.20, 0.50, 0.80]:
        ax2.text(ex, 0.94, '↑', transform=ax2.transAxes, ha='center', va='center', fontsize=14, weight='bold', color=RED)
    ax2.text(0.50, 0.985, 'HOT AIR EXHAUST', transform=ax2.transAxes, ha='center', va='bottom', fontsize=6, weight='bold', color=RED)
    tag(ax2, 0.27, 0.30, 'M2–M4 EXTRUSION', fs=6, color=NAVY)
    tag(ax2, 0.44, 0.30, 'PRINTING (WALLED)', fs=6, color=PURPLE)
    tag(ax2, 0.90, 0.42, 'MEZZANINE OFFICES', fs=6, color=NAVY)
    # right column
    fig.text(0.69, ctop - 0.04, 'MEZZANINE OFFICES\n+ DISPATCH (SOUTH)', ha='left', va='center', fontsize=6.5, weight='bold', color=NAVY,
             bbox=dict(boxstyle='round,pad=0.3', fc='#E3F2FD', ec=NAVY))
    fig.text(0.69, ctop - 0.11, 'WALLED PRINTING ROOM\n(chemicals, own entry E4)', ha='left', va='center', fontsize=6.5, weight='bold', color=PURPLE,
             bbox=dict(boxstyle='round,pad=0.3', fc='#F3E5F5', ec=PURPLE))
    fig.text(0.69, ctop - 0.18, 'STEEL PORTAL @6.0m\n7 FRAMES, 39.40m', ha='left', va='center', fontsize=6.5, weight='bold', color='#333333',
             bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#999999'))

    # ---- Row 3 ----
    rtop = cbot - 0.02
    side = load_crop('renders/pres_side.jpg', 0.02, 0.98)
    sec = load_crop('renders/pres_section.jpg', 0.02, 0.98)
    fig.text(0.015, rtop, 'SIDE ELEVATION', ha='left', va='bottom', fontsize=8, weight='bold', color=NAVY)
    axs, sbot, sh = place_img(fig, side, 0.015, rtop - 0.005, 0.24, FW, FH)
    fig.text(0.265, rtop, 'CROSS SECTION B–B (through extrusion)', ha='left', va='bottom', fontsize=8, weight='bold', color=NAVY)
    axc, _, _ = place_img(fig, sec, 0.265, rtop - 0.005, 0.24, FW, FH)
    tag(axs, 0.5, 0.06, '39,400', fs=7, color=NAVY)
    tag(axc, 0.5, 0.09, '10,170 SPAN • 12,000 APEX', fs=6, color=NAVY)
    # data + legend
    dx = fig.add_axes([0.515, sbot, 0.20, sh]); dx.axis('off')
    dx.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor='white', edgecolor=NAVY, lw=1.2, transform=dx.transAxes))
    dx.text(0.5, 0.94, 'BUILDING & DESIGN DATA', ha='center', va='center', fontsize=7.5, weight='bold', color=NAVY, transform=dx.transAxes)
    data = [('TOTAL SIZE', '39.40 × 10.17m'), ('EAVE HEIGHT', '8.0m'), ('RIDGE HEIGHT', '12.0m'), ('MEZZANINE', '+4.0m (95.6m²)'),
            ('STRUCTURE', 'STEEL PORTAL @6m'), ('ROOF', 'METAL + SKYLIGHTS'), ('VENTILATION', 'RIDGE VENTS'), ('FLOOR', 'POWER-FLOAT'), ('FIRE', 'HOSE REELS + EXT.')]
    for j, (k, v) in enumerate(data):
        yy = 0.85 - j * 0.088
        dx.text(0.05, yy, k, ha='left', va='center', fontsize=6, color='#555555', transform=dx.transAxes)
        dx.text(0.95, yy, v, ha='right', va='center', fontsize=6, weight='bold', color=NAVY, transform=dx.transAxes)
    lx = fig.add_axes([0.745, sbot, 0.24, sh]); lx.axis('off')
    lx.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor='white', edgecolor=NAVY, lw=1.2, transform=lx.transAxes))
    lx.text(0.5, 0.94, 'LEGEND – PRODUCTION FLOW', ha='center', va='center', fontsize=7.5, weight='bold', color=NAVY, transform=lx.transAxes)
    leg = ['RAW MATERIALS STORE', 'MIXING & WEIGHING', 'BLOWN-FILM EXTRUSION', 'FLEXO PRINTING (WALLED)', 'CUTTING & HEAT-SEALING', 'QUALITY CONTROL LAB', 'FINISHED GOODS STORE', 'DISPATCH & LOADING']
    for j, t in enumerate(leg):
        yy = 0.85 - j * 0.088
        lx.text(0.08, yy, str(j + 1), ha='center', va='center', fontsize=6, weight='bold', color='white', transform=lx.transAxes,
                bbox=dict(boxstyle='circle,pad=0.3', fc=NAVY, ec='none'))
        lx.text(0.16, yy, t, ha='left', va='center', fontsize=6, color='#212121', transform=lx.transAxes)
    lx.annotate('', xy=(0.88, 0.045), xytext=(0.60, 0.045), arrowprops=dict(arrowstyle='-|>', color=GREEN, lw=1.8))
    lx.text(0.55, 0.045, 'FLOW', ha='right', va='center', fontsize=6, weight='bold', color=GREEN, transform=lx.transAxes)

    fig.text(0.5, 0.022, 'ILLUSTRATIVE PRESENTATION SHEET (indicative visuals) — EXACT DIMENSIONS, LEVELS & CONSTRUCTION PER CAD SET A101–A301  •  VERIFY ON SITE', ha='center', va='center', fontsize=6.5, style='italic', color='#555555')
    fig.text(0.985, 0.022, 'P1 • P01', ha='right', va='center', fontsize=7, weight='bold', color=NAVY)
    fig.savefig('drawings/P1_presentation_facility.png', dpi=170, facecolor='white')
    fig.savefig('drawings/P1_presentation_facility.pdf', facecolor='white')
    print('saved P1')
    plt.close(fig)


# ================= P2 (portrait, 30m-sample style) =================
def build_P2():
    FW, FH = 11.9, 16.8
    fig = plt.figure(figsize=(FW, FH))
    fig.patch.set_facecolor('white')
    b = fig.add_axes([0.01, 0.008, 0.98, 0.984]); b.axis('off')
    b.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor=NAVY, lw=2, transform=b.transAxes))
    fig.text(0.5, 0.972, 'NYLON PRODUCTION & PACKAGING PLANT', ha='center', va='center', fontsize=15, weight='bold', color=NAVY)
    fig.text(0.5, 0.955, 'Quality Packaging for a Sustainable Future  •  Ilogbo / Foundation Road, Oko-Afo, Badagry, Lagos', ha='center', va='center', fontsize=8, style='italic', color='#333333')

    # ---- full-width plan ----
    plan = load_crop('renders/pres_plan_topdown.jpg', 0.27, 0.72)
    fig.text(0.03, 0.938, 'GROUND FLOOR PLAN (Production hall 39.40 × 10.17m — N on left)', ha='left', va='center', fontsize=9, weight='bold', color=NAVY)
    axp, pbot, _ = place_img(fig, plan, 0.03, 0.928, 0.94, FW, FH)
    for i, zx in enumerate([0.075, 0.215, 0.335, 0.475, 0.60, 0.705, 0.805, 0.945]):
        badge(axp, zx, 0.70, str(i + 1), fs=8)
    fig.text(0.03, pbot - 0.008, '→  Material flow N→S (1→8)      ◆  Printing (4) walled + own entry E4      ■  Machine (red = equipment, not walls)      E1–E7 = entrances (see A102)',
             ha='left', va='top', fontsize=6.5, color='#333333')

    # ---- mid row: front + side ----
    mtop = pbot - 0.035
    fig.text(0.03, mtop, 'FRONT ELEVATION (south, from main road)', ha='left', va='bottom', fontsize=9, weight='bold', color=NAVY)
    front = load_crop('renders/pres_front.jpg', 0.02, 0.98)
    axf, fbot, fh = place_img(fig, front, 0.03, mtop - 0.005, 0.455, FW, FH)
    # sign text on blank band
    axf.text(0.5, 0.50, 'NYLON PRODUCTION & PACKAGING PLANT', transform=axf.transAxes, ha='center', va='center', fontsize=9.5, weight='bold', color=NAVY)
    fig.text(0.515, mtop, 'RIGHT SIDE ELEVATION (east, 39.40m)', ha='left', va='bottom', fontsize=9, weight='bold', color=NAVY)
    side = load_crop('renders/pres_side.jpg', 0.02, 0.98)
    axs2, _, _ = place_img(fig, side, 0.515, mtop - 0.005, 0.455, FW, FH)
    tag(axs2, 0.12, 0.30, 'MEZZ WINDOWS', fs=6, color=NAVY)
    tag(axs2, 0.88, 0.30, 'E4 PRINT ENTRY', fs=6, color=PURPLE)

    # ---- bottom row: longitudinal + 3D ----
    btop = fbot - 0.035
    fig.text(0.03, btop, 'LONGITUDINAL SECTION (A–A, indicative)', ha='left', va='bottom', fontsize=9, weight='bold', color=NAVY)
    cut = load_crop('renders/pres_cutaway.jpg', 0.08, 0.94)
    axl, lbot, _ = place_img(fig, cut, 0.03, btop - 0.005, 0.455, FW, FH)
    axl.text(0.03, 0.88, 'APEX +12.0', transform=axl.transAxes, ha='left', va='center', fontsize=6, weight='bold', color='white',
             bbox=dict(boxstyle='round,pad=0.25', fc=NAVY, ec='none'))
    axl.text(0.03, 0.62, 'EAVES +8.0', transform=axl.transAxes, ha='left', va='center', fontsize=6, weight='bold', color='white',
             bbox=dict(boxstyle='round,pad=0.25', fc=NAVY, ec='none'))
    axl.text(0.97, 0.30, 'MEZZ +4.0', transform=axl.transAxes, ha='right', va='center', fontsize=6, weight='bold', color='white',
             bbox=dict(boxstyle='round,pad=0.25', fc=NAVY, ec='none'))
    fig.text(0.515, btop, '3D CUTAWAY VIEW (without roof)', ha='left', va='bottom', fontsize=9, weight='bold', color=NAVY)
    axo = load_crop('renders/pres_axono2.jpg', 0.02, 0.98)
    ax3, abot, _ = place_img(fig, axo, 0.515, btop - 0.005, 0.455, FW, FH)
    lbot = min(lbot, abot)
    calls = [((0.10, 0.60), (0.03, 0.78), 'RAW STORE'), ((0.24, 0.50), (0.20, 0.72), 'MIXING'),
             ((0.37, 0.55), (0.36, 0.76), 'EXTRUSION'), ((0.50, 0.44), (0.50, 0.24), 'PRINTING'),
             ((0.60, 0.36), (0.63, 0.18), 'CUT / SEAL'), ((0.72, 0.28), (0.76, 0.12), 'QC LAB'),
             ((0.79, 0.44), (0.88, 0.62), 'FG STORE'), ((0.90, 0.40), (0.97, 0.55), 'MEZZ + DISPATCH')]
    for (fx, fy), (tx, ty), lab in calls:
        ax3.plot([fx], [fy], marker='o', ms=4, mfc=RED, mec='white', mew=1, transform=ax3.transAxes, zorder=9)
        ax3.annotate(lab, xy=(fx, fy), xytext=(tx, ty), xycoords=ax3.transAxes, textcoords=ax3.transAxes,
                     ha='center', va='center', fontsize=5.5, weight='bold', color=NAVY,
                     bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=NAVY, alpha=0.95),
                     arrowprops=dict(arrowstyle='-', color=NAVY, lw=0.8), zorder=10)

    # ---- extra views row: cross section + aerial ----
    xtop = lbot - 0.03
    fig.text(0.03, xtop, 'CROSS SECTION B–B (indicative)', ha='left', va='bottom', fontsize=9, weight='bold', color=NAVY)
    csec = load_crop('renders/pres_section_long.jpg', 0.05, 0.95)
    axx1, xbot1, _ = place_img(fig, csec, 0.03, xtop - 0.005, 0.455, FW, FH)
    tag(axx1, 0.5, 0.08, '10,170 SPAN • 12,000 APEX', fs=6, color=NAVY)
    fig.text(0.515, xtop, 'AERIAL VIEW (from main road — gate + tanks)', ha='left', va='bottom', fontsize=9, weight='bold', color=NAVY)
    aer = load_crop('renders/exterior_front.jpg', 0.25, 0.85)
    axx2, xbot2, _ = place_img(fig, aer, 0.515, xtop - 0.005, 0.455, FW, FH)
    tag(axx2, 0.18, 0.30, 'GATE + TANKS', fs=6, color=NAVY)
    xbot = min(xbot1, xbot2)

    # ---- bottom bars ----
    bar_top, bar_h = xbot - 0.02, 0.10
    # key features
    k = fig.add_axes([0.03, bar_top - bar_h, 0.30, bar_h]); k.axis('off')
    k.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor='#E8F0FE', edgecolor=NAVY, lw=1.2, transform=k.transAxes))
    k.text(0.5, 0.90, 'KEY FEATURES', ha='center', va='center', fontsize=8, weight='bold', color=NAVY, transform=k.transAxes)
    for j, t in enumerate(['✓  Linear N→S production flow', '✓  Walled print room + own entry', '✓  Mezz offices + utilities', '✓  Skylights + ridge ventilation', '✓  Decked gate/power + tanks']):
        k.text(0.06, 0.74 - j * 0.145, t, ha='left', va='center', fontsize=6.5, color='#212121', transform=k.transAxes)
    # machine list
    m = fig.add_axes([0.345, bar_top - bar_h, 0.30, bar_h]); m.axis('off')
    m.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor='white', edgecolor=NAVY, lw=1.2, transform=m.transAxes))
    m.text(0.5, 0.90, 'MACHINE / AREA LIST', ha='center', va='center', fontsize=8, weight='bold', color=NAVY, transform=m.transAxes)
    for j, t in enumerate(['M1 Mixing / Weighing', 'M2–M4 Blown-film extrusion', 'M5–M6 Flexo printing (walled)', 'M7–M9 Cutting / Heat-seal', 'M10 QC bench • M11 Granulator', 'Raw / QC / FG stores • Dispatch']):
        m.text(0.06, 0.76 - j * 0.125, '•  ' + t, ha='left', va='center', fontsize=6.5, color='#212121', transform=m.transAxes)
    # floor summary
    s = fig.add_axes([0.66, bar_top - bar_h, 0.31, bar_h]); s.axis('off')
    s.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor='#0F2A52', edgecolor=NAVY, lw=1.2, transform=s.transAxes))
    s.text(0.5, 0.90, 'FLOOR SUMMARY', ha='center', va='center', fontsize=8, weight='bold', color='white', transform=s.transAxes)
    for j, (kk, vv) in enumerate([('Plot', '806.9 m²'), ('Production G/F', '400.7 m²'), ('Mezzanine', '95.6 m²'), ('Gate / Power', '27.6 m²'), ('Total GFA', '523.9 m²'), ('Eaves / Ridge', '+8.0 / +12.0m')]):
        s.text(0.08, 0.76 - j * 0.125, kk, ha='left', va='center', fontsize=6.5, color='#BBDEFB', transform=s.transAxes)
        s.text(0.92, 0.76 - j * 0.125, vv, ha='right', va='center', fontsize=6.5, weight='bold', color='white', transform=s.transAxes)
    # footer band
    f = fig.add_axes([0.03, 0.015, 0.94, 0.028]); f.axis('off')
    f.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor=NAVY, edgecolor='none', transform=f.transAxes))
    f.text(0.5, 0.5, 'Integrated  •  Efficient  •  Sustainable      —      From Raw Materials to Quality Packaging', ha='center', va='center', fontsize=8, weight='bold', color='white', transform=f.transAxes)

    fig.savefig('drawings/P2_presentation_concept.png', dpi=170, facecolor='white')
    fig.savefig('drawings/P2_presentation_concept.pdf', facecolor='white')
    print('saved P2')
    plt.close(fig)

if __name__ == '__main__':
    build_P1()
    build_P2()
