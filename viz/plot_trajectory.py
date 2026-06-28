#!/usr/bin/env python3
"""plot_trajectory.py — render the maturity trajectory as a chart.

PURE function of docs/trajectory.json — needs NO engine, so it renders anywhere
(inside or outside the container). Uses matplotlib if available, otherwise emits
a minimal dependency-free SVG.

  python3 viz/plot_trajectory.py [path/to/trajectory.json] [out.png]
"""
import os
import sys
import json


def _load(json_path):
    with open(json_path, encoding="utf-8") as fh:
        return json.load(fh)


def _series(data):
    xs = [s["slice"] for s in data["slices"]]
    theory = [s["theory"]["f"] for s in data["slices"]]
    consc = [s["conscience"]["f"] for s in data["slices"]]
    return xs, theory, consc


def _plot_matplotlib(data, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    xs, theory, consc = _series(data)
    cross = data.get("crossover_slice")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(xs, theory, "o-", color="#c0392b", linewidth=2, label="theory: above-ordinary-morality (f)")
    ax.plot(xs, consc, "o-", color="#27ae60", linewidth=2, label="conscience: bound-by-conscience (f)")
    if cross:
        ax.axvline(cross, color="#7f8c8d", linestyle="--", linewidth=1)
        ax.annotate("перелом", xy=(cross, 0.5), xytext=(cross + 0.05, 0.85),
                    color="#7f8c8d", fontsize=10)
    ax.set_xticks(xs)
    ax.set_xlabel("срез романа (1 → эпилог)")
    ax.set_ylabel("strength f")
    ax.set_ylim(0, 1)
    ax.set_title("The Honest Mirror — Raskolnikov maturity trajectory")
    ax.legend(loc="center right", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)
    return out_png


def _plot_svg(data, out_svg):
    xs, theory, consc = _series(data)
    cross = data.get("crossover_slice")
    W, H, pad = 760, 440, 60
    x0, y0, x1, y1 = pad, H - pad, W - pad, pad

    def px(i):
        return x0 + (x1 - x0) * (xs[i] - xs[0]) / (xs[-1] - xs[0])

    def py(v):
        return y0 + (y1 - y0) * v  # v in 0..1, y1<y0

    def poly(vals, color):
        pts = " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(vals))
        dots = "".join(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="4" fill="{color}"/>'
                       for i, v in enumerate(vals))
        return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3"/>{dots}'

    grid = ""
    for g in (0.0, 0.25, 0.5, 0.75, 1.0):
        gy = py(g)
        grid += (f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" '
                 f'stroke="#e0e0e0" stroke-width="1"/>'
                 f'<text x="{x0 - 8}" y="{gy + 4:.1f}" font-size="11" '
                 f'text-anchor="end" fill="#888">{g:.2f}</text>')
    xticks = ""
    for i, s in enumerate(xs):
        xticks += (f'<text x="{px(i):.1f}" y="{y0 + 20}" font-size="11" '
                   f'text-anchor="middle" fill="#888">{s}</text>')
    crossline = ""
    if cross:
        ci = xs.index(cross)
        crossline = (f'<line x1="{px(ci):.1f}" y1="{y1}" x2="{px(ci):.1f}" y2="{y0}" '
                     f'stroke="#7f8c8d" stroke-width="1" stroke-dasharray="5,4"/>'
                     f'<text x="{px(ci) + 6:.1f}" y="{y1 + 14}" font-size="12" '
                     f'fill="#7f8c8d">перелом (срез {cross})</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="sans-serif">
<rect width="{W}" height="{H}" fill="white"/>
<text x="{W/2}" y="30" font-size="16" text-anchor="middle" fill="#222">The Honest Mirror — Raskolnikov maturity trajectory</text>
{grid}
<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#888" stroke-width="1"/>
{xticks}{crossline}
{poly(theory, "#c0392b")}
{poly(consc, "#27ae60")}
<rect x="{x1-250}" y="{y1}" width="12" height="12" fill="#c0392b"/>
<text x="{x1-233}" y="{y1+11}" font-size="12" fill="#333">theory (above-ordinary-morality)</text>
<rect x="{x1-250}" y="{y1+18}" width="12" height="12" fill="#27ae60"/>
<text x="{x1-233}" y="{y1+29}" font-size="12" fill="#333">conscience (bound-by-conscience)</text>
<text x="{W/2}" y="{H-12}" font-size="12" text-anchor="middle" fill="#666">срез романа (1 → эпилог)</text>
</svg>'''
    with open(out_svg, "w", encoding="utf-8") as fh:
        fh.write(svg)
    return out_svg


def plot(json_path, out_path=None):
    """Render the trajectory. Returns the path written (.png via matplotlib, else .svg)."""
    data = _load(json_path)
    base = out_path or os.path.join(os.path.dirname(os.path.abspath(json_path)), "trajectory.png")
    stem = os.path.splitext(base)[0]
    try:
        return _plot_matplotlib(data, stem + ".png")
    except Exception:
        return _plot_svg(data, stem + ".svg")


def main():
    json_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "trajectory.json")
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    print("wrote:", plot(json_path, out_path))


if __name__ == "__main__":
    main()
