"""Generate a Mahler cameo favicon: cream profile silhouette on a dark sepia oval."""
from PIL import Image, ImageDraw, ImageFilter
import math, os

def draw_mahler(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size / 256  # scale factor

    def sc(coords):
        """Scale a list of (x,y) tuples."""
        return [(x * s, y * s) for x, y in coords]

    def se(x0, y0, x1, y1):
        """Scale an ellipse bounding box."""
        return [x0*s, y0*s, x1*s, y1*s]

    # --- background oval ---
    bg = (62, 34, 14, 255)          # dark espresso
    rim = (120, 75, 35, 255)        # bronze rim
    d.ellipse([0, 0, size-1, size-1], fill=bg, outline=rim, width=max(1, int(6*s)))

    # --- profile silhouette (facing right) ---
    cream = (240, 220, 185, 255)

    # Main head+neck+shoulder polygon (right-facing profile, roughly centred)
    profile = [
        # forehead top (slightly receding)
        (108, 38),
        # crown
        (135, 28),
        # back of skull
        (170, 55),
        (178, 90),
        (175, 128),
        # nape
        (168, 162),
        # back collar
        (175, 195),
        # right shoulder / chest base
        (210, 248),
        # front base (cut across bottom)
        (50,  248),
        # chin
        (66,  200),
        (72,  185),
        # lower lip indent
        (68,  172),
        # upper lip
        (74,  162),
        # philtrum / base of nose
        (72,  152),
        # nose tip (prominent)
        (52,  140),
        # nose bridge
        (75,  112),
        # brow
        (90,   90),
        # temple
        (100,  60),
    ]
    d.polygon(sc(profile), fill=cream)

    # --- pince-nez glasses ---
    glass_color = (80, 50, 20, 255)
    # left lens (closer to nose)
    d.ellipse(se(76, 108, 96, 124), outline=glass_color, width=max(1, int(3*s)))
    # right lens
    d.ellipse(se(96, 106, 116, 122), outline=glass_color, width=max(1, int(3*s)))
    # bridge between lenses
    d.line([(int(96*s), int(115*s)), (int(96*s), int(115*s))], fill=glass_color, width=max(1, int(2*s)))

    # subtle ear
    d.ellipse(se(152, 125, 166, 145), fill=cream, outline=cream)

    # --- thin shadow under chin for depth ---
    shadow = (180, 155, 120, 120)
    d.polygon(sc([
        (66, 200), (72, 185), (68, 172), (74, 162),
        (60, 162), (54, 175), (55, 195)
    ]), fill=shadow)

    return img


def main():
    out_dir = os.path.join("app", "static")
    os.makedirs(out_dir, exist_ok=True)

    sizes = [256, 64, 32, 16]
    frames = []
    for sz in sizes:
        img = draw_mahler(sz)
        # slight antialias by drawing at 2x then downscaling for small sizes
        if sz <= 32:
            big = draw_mahler(sz * 4)
            big = big.resize((sz, sz), Image.LANCZOS)
            frames.append(big)
        else:
            frames.append(img)

    ico_path = os.path.join(out_dir, "favicon.ico")
    frames[0].save(
        ico_path,
        format="ICO",
        sizes=[(sz, sz) for sz in sizes],
        append_images=frames[1:],
    )
    print(f"Saved {ico_path}  ({os.path.getsize(ico_path):,} bytes)")

    # Also save a PNG for inspection
    frames[0].save(os.path.join(out_dir, "favicon_preview.png"))
    print("Saved app/static/favicon_preview.png  (for inspection)")


if __name__ == "__main__":
    main()
