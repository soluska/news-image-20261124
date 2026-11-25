#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: a newspaper front page for
Tuesday 24 November 2026. Pure PIL primitives, no AI image generation,
no network. Deterministic: same code + same fonts = same bytes.

Stories (all reported on 24 Nov 2026, cross-checked):
  LEAD  Hormuz   - Iran says a fourth oil tanker hit a naval mine and
                   caught fire east of the Strait of Hormuz; US Central
                   Command has not confirmed the claims. (Reuters, IRNA)
  1     Markets  - Trump may have gained up to $15m on paper from
                   Nvidia's rally after taking credit for Jensen Huang's
                   return as CEO. (Financial Times, via Guardian/Inc)
  2     Space    - BepiColombo's Mercury orbit-insertion burn was cut
                   short by a software glitch: 77% of the planned push,
                   a 75-hour orbit, craft safe. (The Register, 24 Nov)
  3     Ukraine  - Russian overnight strike on Zaporizhzhia kills 2,
                   wounds 40 including four children; hits a block of
                   flats. (Just Security Early Edition, 24 Nov)
  4     Gaza     - Israeli airstrikes kill Hamas internal security
                   director Naeem Abu Nahel and six others in Gaza.
                   (Just Security / medics and police, 24 Nov)
  5     Asia     - Russian aircraft enter South Korea's air defence
                   identification zone; Seoul sounds an air raid alert.
                   (Just Security / Joint Chiefs, 24 Nov)
  6     Defence  - NATO chief Mark Rutte: the alliance will defend
                   against threats in space after reports of a Russian
                   nuclear-armed satellite. (BBC, 24 Nov)
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (139, 26, 26)
NAVY = (31, 58, 110)
GREY = (90, 88, 82)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def draw_tanker_scene(d, x0, y0, x1, y1):
    """Strait of Hormuz at night: dark sea, tanker, mine, explosion."""
    d.rectangle([x0, y0, x1, y1], fill=(16, 35, 63))
    # sky glow / horizon
    d.rectangle([x0, y0, x1, y0 + 26], fill=(24, 48, 84))
    # stars
    for sx, sy in [(18, 14), (52, 30), (96, 10), (140, 26), (180, 12),
                   (226, 30), (262, 16), (296, 28), (40, 52), (150, 48)]:
        d.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                  fill=(220, 225, 235))
    # moon
    d.ellipse([x0 + 268, y0 + 42, x0 + 296, y0 + 70], fill=(235, 232, 210))
    # sea bands
    for i, yy in enumerate(range(y0 + 108, y1, 16)):
        d.line([x0, yy, x1, yy], fill=(32, 66, 110), width=2)
    # dashed unauthorised-route line
    ry = y0 + 96
    for dx in range(0, (x1 - x0) - 14, 24):
        d.line([x0 + 10 + dx, ry, x0 + 10 + dx + 13, ry],
               fill=(255, 120, 90), width=3)
    d.text((x0 + 10, y0 + 232), "ROUTE CLOSED", font=font(BOLD, 14),
           fill=(255, 150, 130))
    # tanker: hull + deck + funnel
    hx0, hy0 = x0 + 52, y0 + 158
    hx1, hy1 = x0 + 258, y0 + 196
    d.polygon([(hx0, hy0), (hx1, hy0), (hx1 - 18, hy1), (hx0 + 6, hy1)],
              fill=(12, 12, 14))
    d.rectangle([hx0 + 30, hy0 - 26, hx0 + 74, hy0], fill=(30, 30, 34))
    d.rectangle([hx0 + 170, hy0 - 18, hx0 + 196, hy0], fill=(139, 26, 26))
    d.rectangle([hx0 + 84, hy0 - 12, hx0 + 160, hy0], fill=(52, 52, 58))
    for wx in range(hx0 + 36, hx0 + 70, 12):
        d.rectangle([wx, hy0 - 20, wx + 6, hy0 - 12], fill=(255, 210, 120))
    # wake
    d.line([hx0 - 26, hy1 + 8, hx0 + 8, hy1 + 8], fill=(120, 160, 210),
           width=3)
    d.line([hx1 - 6, hy1 + 14, hx1 + 30, hy1 + 14], fill=(120, 160, 210),
           width=3)
    # explosion burst above the tanker
    cx, cy = x0 + 150, y0 + 108
    for r, col in [(46, (255, 120, 30)), (34, (255, 170, 40)),
                   (22, (255, 220, 110))]:
        pts = []
        for i in range(16):
            ang = math.pi * i / 8
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    # naval mine, lower right
    mx, my = x0 + 268, y0 + 216
    for i in range(8):
        ang = math.pi * i / 4
        d.line([mx + 10 * math.cos(ang), my + 10 * math.sin(ang),
                mx + 20 * math.cos(ang), my + 20 * math.sin(ang)],
               fill=(8, 8, 10), width=4)
    d.ellipse([mx - 13, my - 13, mx + 13, my + 13], fill=(10, 10, 12))
    d.ellipse([mx - 5, my - 5, mx + 1, my + 1], fill=(70, 70, 78))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------
    d.text((W // 2, 26), "THE WORLD IN ONE DAY", font=font(BOLD, 56),
           fill=INK, anchor="ma")
    d.line([24, 96, W - 24, 96], fill=INK, width=3)
    d.line([24, 102, W - 24, 102], fill=INK, width=1)

    # ---- date band ------------------------------------------------
    d.rectangle([24, 112, W - 24, 148], fill=RED)
    d.text((W // 2, 117), "TUESDAY  \u00b7  24 NOVEMBER 2026",
           font=font(BOLD, 28), fill=(255, 255, 255), anchor="ma")

    # ---- lead panel ----------------------------------------------
    lx0, ly0, lx1, ly1 = 24, 160, W - 24, 452
    d.rectangle([lx0, ly0, lx1, ly1], fill=(255, 255, 255),
                outline=INK, width=2)
    tx = lx0 + 20
    d.text((tx, ly0 + 14), "STRAIT OF HORMUZ", font=font(BOLD, 24),
           fill=RED)
    head = font(BOLD, 42)
    lines = wrap(d, "Iran says fourth tanker hits mine in Hormuz", head, 596)
    y = text_block(d, tx, ly0 + 48, lines, head, INK, 50)
    sub = font(REG, 21)
    sublines = wrap(
        d,
        "The IRGC Navy says the tanker exploded and caught fire east of "
        "the strait; two more turned back. US Central Command has not "
        "confirmed the claims.",
        sub, 596)
    text_block(d, tx, y + 8, sublines, sub, (40, 40, 40), 27)
    # "4th tanker" tag
    d.rectangle([tx, ly1 - 44, tx + 270, ly1 - 12], fill=RED)
    d.text((tx + 12, ly1 - 40), "4TH TANKER THIS WEEK", font=font(BOLD, 18),
           fill=(255, 255, 255))
    # illustration, right side of the lead panel
    draw_tanker_scene(d, 668, ly0 + 14, lx1 - 14, ly1 - 14)

    # ---- six story panels, 2 x 3 ---------------------------------
    stories = [
        ("MARKETS", (26, 107, 60), "Trump may have gained up to $15m on Nvidia",
         "He took credit for Huang's return as CEO; the FT puts his "
         "paper gain at $1.3m\u2013$15m."),
        ("SPACE", NAVY, "BepiColombo limps into Mercury orbit",
         "A glitch cut the insertion burn short: 77% of the push, a "
         "75-hour orbit. The craft is safe."),
        ("UKRAINE", RED, "Two killed, 40 hurt in Zaporizhzhia strike",
         "An overnight Russian attack hits a block of flats; four "
         "children are among the wounded."),
        ("GAZA", (110, 74, 31), "Israel kills Hamas security chief in Gaza",
         "Airstrikes kill security chief Naeem Abu Nahel and six others, "
         "two of them police officers."),
        ("ASIA", (15, 107, 107), "Russian jets trigger Seoul air alert",
         "Russian aircraft enter South Korea's air defence zone; Seoul "
         "sounds its first air raid alert."),
        ("DEFENCE", (58, 58, 74), "NATO vows to defend space",
         "Chief Mark Rutte warns the alliance will meet threats in orbit "
         "after reports of a Russian nuclear satellite."),
    ]
    pw, ph, gap = 476, 164, 12
    for i, (kick, col, headline, subline) in enumerate(stories):
        x0 = 24 + (i % 2) * (pw + gap)
        y0 = 464 + (i // 2) * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255),
                    outline=INK, width=2)
        d.rectangle([x0, y0, x1, y0 + 32], fill=col)
        d.text((x0 + 12, y0 + 5), kick, font=font(BOLD, 19),
               fill=(255, 255, 255))
        hf = font(BOLD, 25)
        hl = wrap(d, headline, hf, pw - 24)
        y = text_block(d, x0 + 12, y0 + 42, hl, hf, INK, 30)
        sf = font(REG, 18)
        sl = wrap(d, subline, sf, pw - 24)
        text_block(d, x0 + 12, y + 4, sl, sf, (52, 52, 52), 22)

    # ---- footer ---------------------------------------------------
    d.text((W // 2, 990),
           "Sources: Reuters \u00b7 IRNA \u00b7 Financial Times \u00b7 The Register "
           "\u00b7 BBC \u00b7 Just Security",
           font=font(REG, 15), fill=GREY, anchor="ma")

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
