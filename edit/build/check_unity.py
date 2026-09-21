"""Compare the chrome of a series sheet against poster 4, pixel-exactly.

Renders 2_環境的影子 with a stand-in still (still content cannot move a box)
and 4_陳外科醫院, then reports every horizontal/vertical rule and box edge and
the exact RGB used for each. Any difference in box size or colour shows up as a
mismatched row.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SP = Path(__file__).resolve().parent
sys.path.insert(0, str(SP))

import make_posters as M


def chrome_rows(a: np.ndarray, colour, min_run=200):
    """y -> (x0, x1) for every row containing a long run of `colour`."""
    hit = np.all(a == np.array(colour, dtype=a.dtype), axis=-1)
    out = {}
    for y in np.where(hit.sum(axis=1) >= min_run)[0]:
        xs = np.where(hit[y])[0]
        out[int(y)] = (int(xs.min()), int(xs.max()))
    return out


def bands(rows):
    """Collapse consecutive y's into (y0, y1, x0, x1) bands."""
    out, ys = [], sorted(rows)
    if not ys:
        return out
    s = p = ys[0]
    for y in ys[1:]:
        if y == p + 1 and rows[y] == rows[p]:
            p = y
            continue
        out.append((s, p, *rows[s]))
        s = p = y
    out.append((s, p, *rows[s]))
    return out


def describe(png):
    a = np.array(Image.open(png).convert("RGB"))
    return {
        "size": a.shape[:2],
        "LINE": bands(chrome_rows(a, M.LINE)),
        "AMBER": bands(chrome_rows(a, M.AMBER, min_run=100)),
        "palette": sorted({tuple(c) for c in a.reshape(-1, 3)[
            np.random.default_rng(0).integers(0, a.shape[0] * a.shape[1], 400000)]
        } & {M.PAPER, M.INK, M.MUTED, M.AMBER, M.LINE, M.QRINK}),
    }


def main():
    ref, new = describe(sys.argv[1]), describe(sys.argv[2])
    print(f"page size   series={ref['size']}  poster4={new['size']}  "
          f"{'MATCH' if ref['size'] == new['size'] else 'DIFFER'}\n")

    for key in ("LINE", "AMBER"):
        print(f"--- {key} rules / box edges (y0,y1,x0,x1) ---")
        r, n = ref[key], new[key]
        for i in range(max(len(r), len(n))):
            rv = r[i] if i < len(r) else None
            nv = n[i] if i < len(n) else None
            same = "  " if rv == nv else "<<"
            print(f"{same} series={rv}   poster4={nv}")
        print()

    print("--- exact palette colours present on each page ---")
    print(f"series : {ref['palette']}")
    print(f"poster4: {new['palette']}")
    print("MATCH" if ref["palette"] == new["palette"] else "DIFFER")


if __name__ == "__main__":
    main()
