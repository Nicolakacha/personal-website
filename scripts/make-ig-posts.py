"""Put photos on a fixed light Instagram canvas.

Run from the repo root (needs opencv-python, numpy):
    python3 scripts/make-ig-posts.py                       # Found assets -> _originals_backup/ig/
    python3 scripts/make-ig-posts.py --size 1080x1350      # 4:5 instead of 3:4
    python3 scripts/make-ig-posts.py SRC_DIR OUT_DIR

The flat margin around each photo (the 4 mm, grey 238 margin scripts/process-found-scans.py puts
around every Found print) is trimmed off first, so it is the print itself that is scaled to the
largest size that fits — stopping when one side is --padding from the canvas edge, measured as it
looks in the Instagram app (points on a --view-width screen, not file pixels) — and centred. The canvas is that same grey, so whatever margin colour remains inside the print's
rectangle (worn/rounded corners) merges into it and the print's edge needs no cutting out.

The photo is only resampled (area averaging when shrinking, Lanczos when a small print has to be
enlarged to fill); no other change is made to it.
"""
import argparse, glob, os
import cv2, numpy as np

# Fixed swatch for every post, so the grid reads as one set: the Found assets' margin colour.
BG = 'EEEEEE'

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('src', nargs='?', default='src/assets/found')
p.add_argument('out', nargs='?', default='_originals_backup/ig')
# 3:4 by default: the profile grid shows posts as 3:4, so a 4:5 post loses ~34 px on each side there.
p.add_argument('--size', default='1080x1440', help='canvas WxH in px (3:4 = 1080x1440, 4:5 = 1080x1350, 1:1 = 1080x1080)')
p.add_argument('--padding', type=float, default=10, help='gap left on the side that fills first, in points as seen in the Instagram app')
p.add_argument('--view-width', type=float, default=390, help='width in points the post is shown at in the app (390 = a standard iPhone)')
p.add_argument('--margin-color', type=int, default=238, help='grey level of the flat margin to trim (-1 = no trim)')
p.add_argument('--bg', default=BG, help=f'background colour, hex RGB (default {BG})')
p.add_argument('--quality', type=int, default=95)
a = p.parse_args()

W, H = map(int, a.size.lower().split('x'))
bg = tuple(int(a.bg[i:i + 2], 16) for i in (4, 2, 0))  # hex RGB -> BGR
# +2: resampling and JPEG ringing spill the photo's edge a pixel or two into the canvas; keep that
# inside the padding too, so every side measures at least the padding
pad = round(a.padding * W / a.view_width)  # app points -> file px (10 pt on a 390 pt screen = 28 px of 1080)
boxW, boxH = W - 2 * (pad + 2), H - 2 * (pad + 2)
os.makedirs(a.out, exist_ok=True)

def print_box(im):
    """Bounding box of the print's body: the largest region that is not flat margin colour, after
    dropping anything thinner than ~1 mm (JPEG noise, specks, and the scanner's shadow line along
    an edge, which can run past the paper's sides). Whatever sticks out past this box is cropped
    off, so nothing ends up closer to the canvas edge than the padding."""
    off = (np.abs(im.astype(np.int16) - a.margin_color).max(2) > 6).astype(np.uint8)
    k = max(5, round(min(im.shape[:2]) / 100))  # ~1 mm on a 600 dpi Found print
    off = cv2.morphologyEx(off, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(off, connectivity=8)
    x, y, w, h, _ = st[1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))]
    return slice(y, y + h), slice(x, x + w)

files = sorted(f for f in glob.glob(os.path.join(a.src, '*')) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
if not files: raise SystemExit(f'no images in {a.src}')
for f in files:
    im = cv2.imread(f, cv2.IMREAD_COLOR)
    if a.margin_color >= 0:
        im = im[print_box(im)]
    h, w = im.shape[:2]
    scale = min(boxW / w, boxH / h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))  # floor: never past the box
    photo = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LANCZOS4) if (nw, nh) != (w, h) else im
    canvas = np.full((H, W, 3), bg, np.uint8)
    x, y = (W - nw) // 2, (H - nh) // 2
    canvas[y:y + nh, x:x + nw] = photo
    name = os.path.splitext(os.path.basename(f))[0] + '.jpg'
    # 4:4:4: the default 4:2:0 chroma subsampling bleeds a colour print's colour ~8 px into the canvas
    cv2.imwrite(os.path.join(a.out, name), canvas, [cv2.IMWRITE_JPEG_QUALITY, a.quality,
                cv2.IMWRITE_JPEG_SAMPLING_FACTOR, cv2.IMWRITE_JPEG_SAMPLING_FACTOR_444])
    print(f'{name}: {w}x{h} -> {nw}x{nh} on {W}x{H}')
