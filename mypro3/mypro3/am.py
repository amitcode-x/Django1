# Retry with fix: use Image.eval to scale grain brightness instead of .point with float.
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont, ImageEnhance
import numpy as np
import random
import math
import os

# ---- Parameters (feel free to tweak) ----
WIDTH, HEIGHT = 1080, 1080
SEED = 42
BG_COLOR = (10, 12, 30)  # deep navy base
OUTPUT_PATH = "/mnt/data/aesthetic_snap.png"

random.seed(SEED)
np.random.seed(SEED)

# ---- Helpers ----
def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

def radial_gradient(size, inner_color, outer_color, center=None, radius=None):
    w, h = size
    cx, cy = center if center else (w/2, h/2)
    if radius is None:
        radius = math.hypot(max(cx, w-cx), max(cy, h-cy))
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xx - cx)**2 + (yy - cy)**2) / radius
    dist = np.clip(dist, 0, 1)
    for i in range(3):
        arr[..., i] = (inner_color[i] * (1-dist) + outer_color[i] * dist).astype(np.uint8)
    return Image.fromarray(arr, mode="RGB")

def linear_gradient(size, color1, color2, horizontal=False):
    w, h = size
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    if horizontal:
        t = np.linspace(0, 1, w)
        for i in range(3):
            arr[..., i] = np.tile((color1[i] * (1-t) + color2[i] * t).astype(np.uint8), (h,1))
    else:
        t = np.linspace(0, 1, h)
        for i in range(3):
            arr[..., i] = np.tile(((color1[i] * (1-t) + color2[i] * t)).astype(np.uint8).reshape(h,1), (1,w))
    return Image.fromarray(arr, mode="RGB")

def add_noise(img, intensity=0.08):
    # intensity: 0..1 of noise amplitude
    arr = np.array(img).astype(np.float32) / 255.0
    noise = np.random.normal(0, intensity, arr.shape).astype(np.float32)
    arr = np.clip(arr + noise, 0, 1)
    return Image.fromarray((arr * 255).astype(np.uint8))

def soft_blob(size, color, center, radius, feather=1.0):
    w, h = size
    cx, cy = center
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xx - cx)**2 + (yy - cy)**2)
    mask = np.clip(1 - (dist - radius) / (radius*feather), 0, 1)
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    for i in range(3):
        arr[..., i] = int(color[i])
    arr[..., 3] = (mask * 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")

def color_shift(img, shift=(10, -5, 20)):
    arr = np.array(img).astype(int)
    for i in range(3):
        arr[..., i] = np.clip(arr[..., i] + shift[i], 0, 255)
    return Image.fromarray(arr.astype(np.uint8))

# ---- Build base ----
base = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)

# subtle angled linear gradient overlay
g1 = linear_gradient((WIDTH, HEIGHT), (18, 12, 45), (35, 12, 80), horizontal=False)
g1 = g1.rotate(15, expand=False).filter(ImageFilter.GaussianBlur(radius=30))
base = ImageChops.screen(base, g1)

# central radial glow
rad = radial_gradient((WIDTH, HEIGHT), (255, 120, 170), (10, 12, 30), center=(WIDTH*0.45, HEIGHT*0.4), radius=WIDTH*0.9)
rad = rad.filter(ImageFilter.GaussianBlur(radius=120))
base = ImageChops.add(base, rad, scale=1.2, offset=0)

# Add soft colored blobs (layers)
layers = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))

blob_colors = [
    (255, 155, 190),
    (120, 80, 255),
    (120, 240, 200),
    (255, 200, 140)
]

centers = [
    (WIDTH*0.65, HEIGHT*0.35),
    (WIDTH*0.2, HEIGHT*0.6),
    (WIDTH*0.8, HEIGHT*0.75),
    (WIDTH*0.45, HEIGHT*0.85)
]

radii = [260, 220, 200, 300]
feathers = [1.6, 1.3, 1.2, 2.0]

for i, col in enumerate(blob_colors):
    blob = soft_blob((WIDTH, HEIGHT), col, centers[i], radii[i], feather=feathers[i])
    blob = blob.filter(ImageFilter.GaussianBlur(radius=40 + i*8))
    layers = Image.alpha_composite(layers, blob)

# Slight color shift on layers
layers_rgb = color_shift(layers.convert("RGB"), shift=(6, -8, 10)).convert("RGBA")
layers = Image.blend(layers, layers_rgb, alpha=0.6)

# Overlay blobs onto base with soft light effect
base = Image.composite(layers.convert("RGB"), base, layers.split()[-1])

# Add noise for film grain
grain = add_noise(Image.new("RGB", (WIDTH, HEIGHT), (128,128,128)), intensity=0.12)
grain = grain.filter(ImageFilter.GaussianBlur(radius=0.6))
# scale brightness using Image.eval (per-pixel)
grain = Image.eval(grain, lambda p: int(p * 0.6))
base = ImageChops.overlay(base, grain)

# ---- Decorative shapes: arcs, rings, and lines ----
draw = ImageDraw.Draw(base)

# Draw faint concentric rings
ring_center = (int(WIDTH*0.48), int(HEIGHT*0.4))
for k in range(1, 6):
    bbox = [
        ring_center[0] - k*140,
        ring_center[1] - k*140,
        ring_center[0] + k*140,
        ring_center[1] + k*140,
    ]
    alpha = int(40 / k)
    ring_img = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
    rd = ImageDraw.Draw(ring_img)
    rd.ellipse(bbox, outline=(255,255,255,alpha), width=max(1, 12//k))
    ring_img = ring_img.filter(ImageFilter.GaussianBlur(radius=6))
    base = Image.alpha_composite(base.convert("RGBA"), ring_img).convert("RGB")

# Decorative slanted rectangles
for i in range(6):
    rect = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
    rd = ImageDraw.Draw(rect)
    xi = int(WIDTH * (i/6.0))
    width_rect = int(WIDTH * 0.18)
    rd.rectangle([xi - width_rect//2, -200, xi + width_rect//2, HEIGHT+200], fill=(255,255,255,10))
    rect = rect.rotate(18 + i*6, resample=Image.BICUBIC, expand=False).filter(ImageFilter.GaussianBlur(radius=20))
    base = Image.alpha_composite(base.convert("RGBA"), rect).convert("RGB")

# ---- Light flare and stars ----
flare = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
fd = ImageDraw.Draw(flare)
# central flare
for i in range(6):
    r = 300 - i*40
    alpha = max(0, 120 - i*18)
    fd.ellipse([ring_center[0]-r, ring_center[1]-r, ring_center[0]+r, ring_center[1]+r], fill=(255,220,200,alpha))
flare = flare.filter(ImageFilter.GaussianBlur(radius=60))
base = Image.alpha_composite(base.convert("RGBA"), flare).convert("RGB")

# tiny star speckles
stars = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
sd = ImageDraw.Draw(stars)
for _ in range(600):
    x = random.randint(0, WIDTH-1)
    y = random.randint(0, HEIGHT-1)
    size = random.random()**3 * 3.5
    brightness = int(180 + random.random()*75)
    sd.ellipse([x-size, y-size, x+size, y+size], fill=(brightness, brightness, 255, int(120*random.random())))
stars = stars.filter(ImageFilter.GaussianBlur(radius=0.9))
base = Image.alpha_composite(base.convert("RGBA"), stars).convert("RGB")

# ---- Subtle geometric grid (soft) ----
grid = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
gd = ImageDraw.Draw(grid)
gap = 120
for x in range(-gap, WIDTH+gap, gap):
    gd.line([(x, -100), (x, HEIGHT+100)], fill=(255,255,255,8), width=1)
for y in range(-gap, HEIGHT+gap, gap):
    gd.line([(-100, y), (WIDTH+100, y)], fill=(255,255,255,6), width=1)
grid = grid.filter(ImageFilter.GaussianBlur(radius=12))
base = Image.alpha_composite(base.convert("RGBA"), grid).convert("RGB")

# ---- Foreground texture: wavy scanlines ----
scan = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
sd = ImageDraw.Draw(scan)
for i in range(0, HEIGHT, 6):
    offset = int(8 * math.sin(i / 35.0 + SEED))
    sd.line([(-50, i), (WIDTH+50, i)], fill=(10,10,20,12), width=2)
scan = scan.filter(ImageFilter.GaussianBlur(radius=1.2))
base = Image.alpha_composite(base.convert("RGBA"), scan).convert("RGB")

# ---- Add a centered poster card with glassmorphism ----
card_w, card_h = int(WIDTH*0.62), int(HEIGHT*0.52)
card = Image.new("RGBA", (card_w, card_h), (255,255,255,24))
card_mask = Image.new("L", (card_w, card_h), 0)
md = ImageDraw.Draw(card_mask)
md.rounded_rectangle([0,0,card_w,card_h], radius=32, fill=220)
card = card.filter(ImageFilter.GaussianBlur(radius=8))

# Place card
card_x = WIDTH//2 - card_w//2
card_y = int(HEIGHT*0.22)
base = Image.alpha_composite(base.convert("RGBA"), Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))).convert("RGB")
tmp = base.copy().convert("RGBA")
tmp.paste(card, (card_x, card_y), card_mask)
base = tmp.convert("RGB")

# subtle inner highlight on card
highlight = Image.new("RGBA", (card_w, card_h), (255,255,255,0))
hd = ImageDraw.Draw(highlight)
hd.ellipse([-card_w*0.4, -card_h*0.6, card_w*0.9, card_h*0.9], fill=(255,255,255,30))
highlight = highlight.filter(ImageFilter.GaussianBlur(radius=40))
tmp = base.convert("RGBA")
tmp.paste(highlight, (card_x, card_y), highlight)
base = tmp.convert("RGB")

# ---- Title text with elegant font fallback ----
draw = ImageDraw.Draw(base)
title = "a e s t h e t i c"
subtitle = "midnight bloom"

# Try to load a common system font, fallback to default
def load_font(size, bold=False):
    possible = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
    ]
    for p in possible:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size=size)
            except:
                continue
    return ImageFont.load_default()

title_font = load_font(64)
sub_font = load_font(28)

# title positioning
tw, th = draw.textsize(title, font=title_font)
tx = WIDTH//2 - tw//2
ty = card_y + 40
# shadow
draw.text((tx+2, ty+2), title, font=title_font, fill=(0,0,0,90))
draw.text((tx, ty), title, font=title_font, fill=(255,255,255,220))

# subtitle
stw, sth = draw.textsize(subtitle, font=sub_font)
sx = WIDTH//2 - stw//2
sy = ty + th + 12
draw.text((sx, sy), subtitle, font=sub_font, fill=(230,230,250,200))

# ---- Small details: rounded "sticker" with emoji ----
st_w, st_h = 220, 64
st = Image.new("RGBA", (st_w, st_h), (255,255,255,200))
sd = ImageDraw.Draw(st)
sd.rounded_rectangle([0,0,st_w,st_h], radius=32, fill=(255,255,255,220))
emoji = "✨"
try:
    font_emoji = load_font(32)
    sd.text((18, 12), emoji, font=font_emoji, fill=(30,20,60))
except:
    sd.text((18, 12), "*", fill=(30,20,60))
sd.text((64, 14), "midnight • 10:10 PM", font=sub_font, fill=(30,30,40,220))
st = st.filter(ImageFilter.GaussianBlur(radius=0.6))
base.paste(st, (card_x + 30, card_y + card_h - 90), st)

# ---- Final color grade and vignette ----
def vignette(img, strength=0.6):
    w, h = img.size
    vig = Image.new("L", (w, h), 0)
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w/2, h/2
    dist = np.sqrt((xx - cx)**2 + (yy - cy)**2)
    maxd = np.sqrt(cx**2 + cy**2)
    mask = np.clip((dist / maxd), 0, 1)
    mask = (mask**2 * 255 * strength).astype(np.uint8)
    return ImageChops.multiply(img, Image.fromarray(np.dstack([255-mask]*3).astype(np.uint8)))

graded = base.copy()
# slight warmth
graded = color_shift(graded, shift=(8, 2, -6))
# vignette
graded = vignette(graded, strength=0.7)

# final subtle sharpen
final = graded.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=3))

# save and display
final.save(OUTPUT_PATH)
final

 