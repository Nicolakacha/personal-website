"""Run from the repo root: python3 scripts/process-found-scans.py  (needs opencv-python, numpy)

Split each A4 scan into individual photos: deskew, mask the print (keeping its own
worn corners/edges), set it on a flat margin of identical width, remove dust, save at 600 dpi.
Also writes each print's alpha mask to _originals_backup/founds_masks/."""
import cv2, numpy as np, glob, os, json, sys
SRC = '_originals_backup/founds'
OUT = 'src/assets/found'
# Before/after crops of every dust candidate, for checking by eye (outside git).
S = '_originals_backup/founds_review'
# Print outlines (alpha masks), same size as the outputs.
MASKS = '_originals_backup/founds_masks'
DPI = 1200; OUT_DPI = 600
MARGIN_MM = 4.0
MARGIN_COLOR = 238
F = 8
os.makedirs(OUT, exist_ok=True); os.makedirs(f'{S}/review', exist_ok=True); os.makedirs(MASKS, exist_ok=True)

def detect(im):
    sm = cv2.resize(im, None, fx=1/F, fy=1/F, interpolation=cv2.INTER_AREA).astype(np.float32)
    bg = np.median(sm[5:40, :].reshape(-1, 3), 0)
    diff = np.abs(sm - bg).max(2)
    g = cv2.cvtColor(sm.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    mag = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
    mask = (((diff > 12) | (mag > 40)) * 255).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(mask); cv2.drawContours(filled, cnts, -1, 255, -1)
    filled = cv2.morphologyEx(filled, cv2.MORPH_OPEN, np.ones((15, 15), np.uint8))
    cnts, _ = cv2.findContours(filled, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for c in cnts:
        if cv2.contourArea(c) < 2000: continue
        (cx, cy), (w, h), a = cv2.minAreaRect(c)
        if a > 45: a -= 90; w, h = h, w
        if a < -45: a += 90; w, h = h, w
        rects.append(((cx * F, cy * F), (w * F, h * F), a))
    return rects, bg

def reading_order(rects):
    rects = sorted(rects, key=lambda r: r[0][1])
    rows = []
    for r in rects:
        if rows and abs(r[0][1] - rows[-1][-1][0][1]) < min(r[1][1], rows[-1][-1][1][1]) / 2:
            rows[-1].append(r)
        else:
            rows.append([r])
    return [r for row in rows for r in sorted(row, key=lambda r: r[0][0])]

def cut(im, rect):
    (cx, cy), (w, h), a = rect
    pad = int(MARGIN_MM / 25.4 * DPI) + 120
    half = int(np.hypot(w, h) / 2) + pad
    x0, y0 = int(cx) - half, int(cy) - half
    H, W = im.shape[:2]
    region = cv2.copyMakeBorder(im[max(y0,0):min(y0+2*half,H), max(x0,0):min(x0+2*half,W)],
        max(0,-y0), max(0,y0+2*half-H), max(0,-x0), max(0,x0+2*half-W), cv2.BORDER_REPLICATE)
    if abs(a) > 0.05:
        M = cv2.getRotationMatrix2D((half, half), a, 1.0)
        region = cv2.warpAffine(region, M, (2*half, 2*half), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    hw, hh = int(w/2) + pad, int(h/2) + pad
    return region[half-hh:half+hh, half-hw:half+hw]

def fit_quad(crop, pad):
    """Fit each side of the print as its own straight line (prints are not perfect rectangles,
    and the deskew is never exact). Along each side, every few px, walk an averaged profile
    from the scanner background inwards and take the end of the first strong step — the paper
    edge, including its own shadow/highlight line — then fit a robust line through those points.
    Returns the 4 corners (tl, tr, br, bl) in crop coordinates."""
    g = cv2.GaussianBlur(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 1.5)
    H, W = g.shape
    x0, x1, y0, y1 = pad, W - pad, pad, H - pad
    R, A = 90, 4  # search half-width across the edge, half-width of the averaging strip
    def edge_in(profile):  # profile runs outside -> inside; returns offset of the paper edge
        grad = np.abs(profile[3:] - profile[:-3])  # over 3 px: some paper edges are soft
        m = grad.max()
        if m < 6: return None
        strong = grad > 0.35 * m
        i = int(np.argmax(strong))
        while i + 1 < len(strong) and strong[i + 1]: i += 1
        return i + 3
    lines, strength = {}, {}
    for side in 'LRTB':
        pts, ms = [], []
        lo, hi = (y0, y1) if side in 'LR' else (x0, x1)
        for t in range(int(lo + 0.1*(hi-lo)), int(hi - 0.1*(hi-lo)), 8):
            if side == 'L': prof = g[t-A:t+A+1, x0-R:x0+R].mean(0)
            if side == 'R': prof = g[t-A:t+A+1, x1-R:x1+R].mean(0)[::-1]
            if side == 'T': prof = g[y0-R:y0+R, t-A:t+A+1].mean(1)
            if side == 'B': prof = g[y1-R:y1+R, t-A:t+A+1].mean(1)[::-1]
            e = edge_in(prof)
            if e is None: continue
            ms.append(np.abs(prof[3:] - prof[:-3]).max())
            pos = {'L': x0-R+e, 'R': x1+R-e, 'T': y0-R+e, 'B': y1+R-e}[side]
            pts.append((pos, t) if side in 'LR' else (t, pos))
        if len(pts) < 10:  # no usable edge on this side: keep the detected rectangle's side
            print(f'  fit_quad: side {side} fell back to the detected rectangle', flush=True)
            pts = [({'L': x0, 'R': x1}[side], lo), ({'L': x0, 'R': x1}[side], hi)] if side in 'LR' else [(lo, {'T': y0, 'B': y1}[side]), (hi, {'T': y0, 'B': y1}[side])]
        vx, vy, px, py = cv2.fitLine(np.float32(pts), cv2.DIST_HUBER, 0, 0.01, 0.01).ravel()
        lines[side] = (np.array([px, py]), np.array([vx, vy]))
        strength[side] = float(np.median(ms)) if ms else 20.0
    def meet(a, b):
        (p1, d1), (p2, d2) = lines[a], lines[b]
        t = np.linalg.solve(np.array([d1, -d2]).T, p2 - p1)
        return p1 + t[0] * d1
    return np.float32([meet('T', 'L'), meet('T', 'R'), meet('B', 'R'), meet('B', 'L')]), strength

def print_mask(crop, quad, strength):
    """The fitted quadrilateral, trimmed at the corners to the print's real (worn/rounded) outline.
    Purely geometric — no colour matching, so a pale paper border is never mistaken for the
    scanner background: within 3 mm of each corner, every row (for the left/right sides) and every
    column (for the top/bottom sides) is walked from outside the edge line inwards to the first
    paper-edge step. Where the paper is cut back (rounded corner) that step lies inside the line
    and the gap is removed; where no clear step is found the straight line is kept."""
    H, W = crop.shape[:2]
    S8 = 8  # sub-pixel polygon fill
    mask = np.zeros((H, W), np.uint8)
    cv2.fillPoly(mask, [np.round(quad * (1 << S8)).astype(np.int32)], 255, cv2.LINE_AA, S8)
    g = cv2.GaussianBlur(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 1.5)
    Z, O = int(3.0 / 25.4 * DPI), 30  # corner reach; how far outside the line a walk starts
    tl, tr, br, bl = quad
    def x_on(p, q, y): return p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1])
    def y_on(p, q, x): return p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0])
    def walk(profile, thr):  # outside -> inside; offset of the end of the first strong step
        grad = np.abs(profile[3:] - profile[:-3])
        strong = grad > thr
        if not strong.any(): return None
        i = int(np.argmax(strong))
        while i + 1 < len(strong) and strong[i + 1]: i += 1
        return i + 3
    def trim(cut):  # cut: per-row/col depth inside the line; noise off, and a corner only grows towards the vertex
        cut = cv2.medianBlur(np.uint8(np.clip(cut, 0, 255))[:, None], 9)[:, 0].astype(int) if len(cut) >= 9 else cut
        return np.minimum.accumulate(cut[::-1])[::-1]  # index 0 = at the vertex
    for side, (p, q) in {'L': (tl, bl), 'R': (tr, br), 'T': (tl, tr), 'B': (bl, br)}.items():
        thr = max(6.0, 0.35 * strength[side])
        for end, far in ((p, q), (q, p)):  # both corners on this side
            sgn = 1 if far[1 if side in 'LR' else 0] > end[1 if side in 'LR' else 0] else -1
            ts = [int(round(end[1 if side in 'LR' else 0])) + sgn * k for k in range(Z)]
            cuts = []
            for t in ts:
                if side in 'LR':
                    x = x_on(p, q, t); d = 1 if side == 'L' else -1
                    xs = np.round(x - d * O + d * np.arange(O + Z)).astype(int)
                    if t - 1 < 0 or t + 2 > H or xs.min() < 0 or xs.max() >= W: cuts.append(0); continue
                    prof = g[t-1:t+2, xs].mean(0)
                else:
                    y = y_on(p, q, t); d = 1 if side == 'T' else -1
                    ys = np.round(y - d * O + d * np.arange(O + Z)).astype(int)
                    if t - 1 < 0 or t + 2 > W or ys.min() < 0 or ys.max() >= H: cuts.append(0); continue
                    prof = g[ys, t-1:t+2].mean(1)
                e = walk(prof, thr)
                cuts.append(0 if e is None else max(0, e - O))
            cuts = trim(np.array(cuts))
            for t, c in zip(ts, cuts):
                if c <= 0: continue
                if side in 'LR':
                    x = x_on(p, q, t)
                    if side == 'L': mask[t, :int(np.ceil(x + c))] = 0
                    else: mask[t, int(np.floor(x - c)) + 1:] = 0
                else:
                    y = y_on(p, q, t)
                    if side == 'T': mask[:int(np.ceil(y + c)), t] = 0
                    else: mask[int(np.floor(y - c)) + 1:, t] = 0
    return cv2.GaussianBlur(mask, (3, 3), 0).astype(np.float32) / 255

def local_std(img, k):
    m = cv2.blur(img, (k, k)); return np.sqrt(np.maximum(cv2.blur(img*img, (k, k)) - m*m, 0))

def dust_mask(photo, inside):
    """Deliberately conservative: only specks big enough to survive downscaling (>= ~0.1 mm),
    strongly contrasting, neutral in colour, sitting alone in a smooth area. Anything in texture,
    any cluster (abrasion, emulsion damage), any line (scratch, crack), any large or coloured mark
    (foxing, stains) belongs to the print and is left untouched."""
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    g = gray.astype(np.float32)
    med = cv2.medianBlur(gray, 31).astype(np.float32)
    r = g - med
    sigma = cv2.GaussianBlur(np.abs(r), (0, 0), 20) * 1.25
    flat = local_std(cv2.medianBlur(gray, 51).astype(np.float32), 61)
    loose = (np.abs(r) > np.maximum(20, 4 * sigma)) & inside
    strict = (np.abs(r) > np.maximum(45, 8 * sigma)) & inside
    n, lab, st, cen = cv2.connectedComponentsWithStats(strict.astype(np.uint8), 8)
    _, llab, lst, _ = cv2.connectedComponentsWithStats(loose.astype(np.uint8), 8)
    medc = cv2.medianBlur(photo, 31).astype(np.float32)
    out = np.zeros(gray.shape, np.uint8)
    R = 60
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if not (16 <= area <= 500 and max(w, h) <= 35 and area / (w*h) >= 0.35 and max(w, h) <= 2.5 * min(w, h)): continue
        cx, cy = int(cen[i][0]), int(cen[i][1])
        if flat[cy, cx] > 4: continue
        # isolation: no other noticeable deviation within R px
        ys, ye, xs, xe = max(cy-R, 0), cy+R, max(cx-R, 0), cx+R
        others = set(np.unique(llab[ys:ye, xs:xe])) - {0, llab[cy, cx]}
        others = [o for o in others if lst[o][4] >= 6]
        if others: continue
        sl = (slice(y, y+h), slice(x, x+w)); sel = lab[sl] == i
        d = (photo[sl][sel].astype(np.float32) - medc[sl][sel]).mean(0)
        if np.ptp(d) > 0.25 * np.abs(d).max() + 5: continue
        # sharpness: scan dust lies on the glass, in focus; soft blobs were printed into the photo
        ring = cv2.dilate(sel.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
        y2, x2 = max(y-3, 0), max(x-3, 0)
        gpatch = g[y2:y+h+3, x2:x+w+3]
        gy_, gx_ = np.gradient(gpatch)
        rmask = np.zeros(gpatch.shape, bool); rs = ring[:gpatch.shape[0]-(y-y2), :gpatch.shape[1]-(x-x2)]
        rmask[(y-y2):(y-y2)+rs.shape[0], (x-x2):(x-x2)+rs.shape[1]] = rs
        sharp = np.percentile(np.hypot(gx_, gy_)[rmask], 90) / (abs(r[cy, cx]) + 1e-3)
        lab_ = cv2.cvtColor(np.uint8([[photo[sl][sel].mean(0)]]), cv2.COLOR_BGR2LAB)[0, 0].astype(float)
        chroma = float(np.hypot(lab_[1]-128, lab_[2]-128))
        METRICS.append((CUR[0], cx, cy, round(float(sharp), 3), round(chroma, 1), int(r[cy, cx])))
        if sharp < 0.28 or chroma >= 10: continue
        near = lambda lst: any(n == CUR[0] and abs(cy - ky) < 15 for n, ky in lst)
        if (CUR[0] in KEEP_ALL or near(MANUAL_KEEP)) and not near(MANUAL_REMOVE): continue
        # grow to the loose footprint so the whole speck (incl. its soft rim) is replaced
        out[llab == llab[cy, cx]] = 255 if llab[cy, cx] else 0
        out[sl][sel] = 255
    return cv2.dilate(out, np.ones((7, 7), np.uint8))

METRICS = []; CUR = ['']
# Reviewed by eye at 100%. found_01: the round paper-white dots are uniform in shape and tone — printed
# from dust on the negative, i.e. part of the print — so keep them all except the two fibres.
# found_04/05: sharp black dots on white sky — origin uncertain, keep.
KEEP_ALL = {'found_01'}
# (x from the right edge, y) boxes in the 1200 dpi crop holding a hair that crosses the print
HAIRS = {'found_01': [(-470, 350, -160, 560)]}
MANUAL_KEEP = [('found_04', 1252), ('found_05', 3533)]
MANUAL_REMOVE = [('found_01', 2407), ('found_01', 2798)]
manifest = []
idx = 0
for path in sorted(glob.glob(f'{SRC}/*.jpeg')):
    im = cv2.imread(path)
    rects, bg = detect(im)
    for rect in reading_order(rects):
        idx += 1
        name = f'found_{idx:02d}'
        crop = cut(im, rect)
        CUR[0] = name
        pad = int(MARGIN_MM / 25.4 * DPI) + 120
        quad, strength = fit_quad(crop, pad)
        alpha = print_mask(crop, quad, strength)
        m = int(MARGIN_MM / 25.4 * DPI)
        ys, xs = np.where(alpha > 0.5)
        x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        crop, alpha = crop[y0-m:y1+m, x0-m:x1+m], alpha[y0-m:y1+m, x0-m:x1+m]
        inside = cv2.erode((alpha > 0.99).astype(np.uint8), np.ones((41, 41), np.uint8)) > 0
        dm = dust_mask(crop, inside)
        for hx0, hy0, hx1, hy1 in HAIRS.get(name, []):
            # a hair lying on the print (it continues off the print in the raw scan): thin dark line on light paper
            W_ = crop.shape[1]; hx0, hx1 = W_ + hx0, W_ + hx1
            gg = cv2.cvtColor(crop[hy0:hy1, hx0:hx1], cv2.COLOR_BGR2GRAY)
            line = (gg.astype(np.float32) - cv2.medianBlur(gg, 15).astype(np.float32)) < -10
            n_, lab_, st_, _ = cv2.connectedComponentsWithStats(line.astype(np.uint8), 8)
            for i_ in range(1, n_):
                if max(st_[i_][2], st_[i_][3]) >= 40:
                    dm[hy0:hy1, hx0:hx1][cv2.dilate((lab_ == i_).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = 255
        clean = cv2.inpaint(crop, dm, 4, cv2.INPAINT_TELEA) if dm.any() else crop
        a = alpha[..., None]
        out = (clean.astype(np.float32) * a + MARGIN_COLOR * (1 - a)).round().astype(np.uint8)
        small = cv2.resize(out, None, fx=OUT_DPI/DPI, fy=OUT_DPI/DPI, interpolation=cv2.INTER_AREA)
        cv2.imwrite(f'{OUT}/{name}.jpg', small, [cv2.IMWRITE_JPEG_QUALITY, 92])
        # The print's own outline at the output resolution, for re-matting it elsewhere (make-ig-posts.py).
        cv2.imwrite(f'{MASKS}/{name}.png', cv2.resize((alpha * 255).round().astype(np.uint8), small.shape[1::-1], interpolation=cv2.INTER_AREA))
        for (nm, qx, qy, sh, ch, rr) in [t for t in METRICS if t[0] == name]:
            a0, b0 = max(qy-60, 0), max(qx-60, 0)
            pa, pb = crop[a0:a0+120, b0:b0+120], clean[a0:a0+120, b0:b0+120]
            if pa.shape[:2] == (120, 120):
                cv2.imwrite(f'{S}/review/patch_{name}_{qy:05d}_s{sh:.2f}_c{ch:.0f}.png', cv2.resize(np.hstack([pa, np.full((120, 4, 3), 255, np.uint8), pb]), None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST))
        ov = crop.copy()
        for c in cv2.findContours(dm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
            (ccx, ccy), rr = cv2.minEnclosingCircle(c); cv2.circle(ov, (int(ccx), int(ccy)), int(rr) + 25, (0, 0, 255), 4)
        cv2.imwrite(f'{S}/review/{name}_dust.jpg', ov, [cv2.IMWRITE_JPEG_QUALITY, 85])
        xs = np.array([x0, x1 - 1]); ys = np.array([y0, y1 - 1])
        pw, ph = (xs.max()-xs.min()+1)/DPI*25.4, (ys.max()-ys.min()+1)/DPI*25.4
        manifest.append(dict(name=name, scan=os.path.basename(path), print_mm=[round(pw,1), round(ph,1)],
            angle=round(rect[2],2), dust_spots=int(cv2.connectedComponents(dm)[0]-1), px=list(small.shape[1::-1])))
        print(manifest[-1], flush=True)
json.dump(METRICS, open(f'{S}/metrics.json','w'))
json.dump(manifest, open(f'{S}/manifest.json', 'w'), indent=1)
