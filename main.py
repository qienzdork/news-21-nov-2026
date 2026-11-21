#!/usr/bin/env python3
"""THE WORLD TODAY -- front page for Saturday 21 November 2026.

Draws a 1024x1024 newspaper front page with Pillow and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Every story on the page happened, or was first reported, on Saturday
21 November 2026. A DATE CHECK footer at the bottom names the big
stories from other days that were deliberately left out.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

PAPER = (247, 242, 233)
INK = (20, 20, 20)
GRAY = (110, 108, 100)
LIGHT = (232, 226, 214)
RED = (176, 30, 30)
NAVY = (15, 25, 48)
BLUE = (30, 80, 140)
GOLD = (198, 148, 40)
GREEN = (42, 118, 60)
SAND = (226, 200, 150)
SKY = (214, 230, 240)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"  # no italic face here
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, fill, max_w, leading):
    """Draw wrapped paragraph; return the y just below the last line."""
    for line in wrap(d, text, font, max_w):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(d, x0, y, x1, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def burst(d, cx, cy, r_out, r_in, fill, spikes=10):
    """Starburst polygon centred at (cx, cy)."""
    import math

    pts = []
    for i in range(spikes * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / spikes - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def thumb_sky(d, x, y, w, h):
    """Night sky over a Kyiv skyline, explosions, drone dots, Polish flag."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy in [(12, 10), (40, 26), (70, 8), (105, 20), (130, 12),
                   (22, 40), (88, 34), (118, 44), (55, 48)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 220, 220))
    base = y + h
    for bx, bw, bh in [(0, 26, 46), (28, 18, 62), (48, 22, 38),
                       (72, 16, 56), (90, 24, 44), (116, 18, 66), (136, 14, 40)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 12, 26))
        for wy in range(base - bh + 6, base - 4, 10):
            for wx in range(x + bx + 4, x + bx + bw - 3, 8):
                d.rectangle([wx, wy, wx + 2, wy + 3], fill=GOLD)
    burst(d, x + 52, y + 34, 20, 8, (255, 170, 40))
    burst(d, x + 52, y + 34, 10, 4, (255, 230, 120))
    burst(d, x + 118, y + 26, 13, 5, (255, 120, 40))
    burst(d, x + 118, y + 26, 6, 3, (255, 220, 140))
    for dx, dy in [(30, 18), (96, 12), (140, 22)]:
        d.ellipse([x + dx, y + dy, x + dx + 3, y + dy + 3], fill=(255, 255, 255))
    d.line([(x + 150, y + h - 58), (x + 150, y + h - 14)], fill=(240, 240, 240), width=2)
    d.rectangle([x + 150, y + h - 58, x + 168, y + h - 47], fill=(255, 255, 255))
    d.rectangle([x + 150, y + h - 47, x + 168, y + h - 36], fill=RED)


def thumb_chart(d, x, y, w, h):
    """Falling market chart."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=GRAY, width=1)
    for gy in range(y + 18, y + h - 8, 18):
        d.line([(x + 6, gy), (x + w - 6, gy)], fill=(235, 235, 235), width=1)
    pts = [(x + 8, y + 22), (x + 34, y + 34), (x + 58, y + 30),
           (x + 84, y + 52), (x + 108, y + 66), (x + 132, y + 88)]
    d.line(pts, fill=RED, width=4, joint="curve")
    d.polygon([(x + 132, y + 88), (x + 120, y + 84), (x + 128, y + 74)],
              fill=RED)
    d.text((x + 8, y + h - 22), "S&P -3.7%", font=F(SANS_B, 15), fill=RED)


def thumb_court(d, x, y, w, h):
    """Courthouse columns and a gavel."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    d.polygon([(x + 10, y + 34), (x + w // 2, y + 10), (x + w - 10, y + 34)],
              fill=(120, 100, 70))
    for cx in (x + 26, x + w // 2 - 6, x + w - 38):
        d.rectangle([cx, y + 38, cx + 12, y + h - 22], fill=(150, 132, 100))
    d.rectangle([x + 8, y + h - 22, x + w - 8, y + h - 14], fill=(120, 100, 70))
    d.text((x + 8, y + h - 44), "9-6", font=F(SANS_B, 16), fill=RED)


def thumb_pill(d, x, y, w, h):
    """A capsule pill and molecules."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 236, 244))
    d.rounded_rectangle([x + 22, y + 44, x + 128, y + 70], radius=13,
                        fill=(255, 255, 255), outline=RED, width=2)
    d.rounded_rectangle([x + 22, y + 44, x + 75, y + 70], radius=13, fill=RED)
    for mx, my, mr in [(30, 22, 5), (120, 18, 4), (138, 88, 5), (16, 90, 4)]:
        d.ellipse([x + mx - mr, y + my - mr, x + mx + mr, y + my + mr],
                  outline=BLUE, width=2)
    d.text((x + 10, y + h - 24), "1 in 12", font=F(SANS_B, 15), fill=BLUE)


def thumb_desert(d, x, y, w, h):
    """Desert sky, interceptor trails crossing, burst."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 214, 160))
    d.ellipse([x + w - 34, y + 8, x + w - 12, y + 30], fill=(255, 220, 120))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(210, 175, 120))
    d.polygon([(x + 20, y + h - 26), (x + 34, y + h - 58), (x + 48, y + h - 26)],
              fill=(160, 120, 70))
    for bx, bw, bh in [(96, 12, 34), (112, 10, 48), (126, 12, 28)]:
        d.rectangle([x + bx, y + h - 26 - bh, x + bx + bw, y + h - 26],
                    fill=(90, 80, 70))
    d.line([(x + 8, y + h - 20), (x + 70, y + 26)], fill=(255, 255, 255), width=3)
    d.line([(x + w - 8, y + h - 30), (x + 82, y + 30)], fill=(255, 255, 255), width=3)
    d.rectangle([x + 64, y + 22, x + 72, y + 28], fill=INK)
    d.rectangle([x + 78, y + 26, x + 86, y + 32], fill=INK)
    burst(d, x + 76, y + 28, 16, 7, (255, 160, 40))
    burst(d, x + 76, y + 28, 8, 3, (255, 230, 140))


def thumb_globe(d, x, y, w, h):
    """Blue globe with land, a red deadline flag."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 236, 244))
    cx, cy, r = x + w // 2 - 8, y + h // 2, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 130, 200))
    d.ellipse([cx - 26, cy - 18, cx - 2, cy + 2], fill=GREEN)
    d.ellipse([cx + 4, cy + 6, cx + 26, cy + 26], fill=GREEN)
    d.ellipse([cx - 8, cy - 30, cx + 10, cy - 14], fill=GREEN)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=2)
    d.line([(x + w - 26, y + 12), (x + w - 26, y + 44)], fill=INK, width=2)
    d.polygon([(x + w - 26, y + 12), (x + w - 10, y + 18), (x + w - 26, y + 24)],
              fill=RED)


def thumb_cricket(d, x, y, w, h):
    """Cricket pitch, stumps, bat and ball."""
    d.rectangle([x, y, x + w, y + h], fill=(90, 160, 80))
    d.rectangle([x + 18, y + 8, x + w - 18, y + h - 8], fill=(214, 186, 140))
    for sx in (x + 34, x + 40, x + 46):
        d.rectangle([sx, y + 16, sx + 3, y + 34], fill=(255, 220, 90))
    d.polygon([(x + 96, y + h - 30), (x + 108, y + h - 34), (x + 128, y + 26),
               (x + 116, y + 30)], fill=(150, 100, 50))
    d.ellipse([x + 122, y + 78, x + 134, y + 90], fill=RED)
    d.ellipse([x + 124, y + 80, x + 128, y + 84], fill=(255, 255, 255))


def story_cell(d, x, y, w, h, kicker, headline, body, thumb):
    """One grid story: thumbnail left, kicker + headline + body right."""
    tw, th = 150, 110
    thumb(d, x, y + 6, tw, th)
    tx = x + tw + 12
    tw_text = w - tw - 12
    d.text((tx, y + 2), kicker, font=F(SANS_B, 12), fill=RED)
    yy = para(d, tx, y + 22, headline, F(SERIF_B, 18), INK, tw_text, 20)
    para(d, tx, yy + 2, body, F(SANS, 12), (40, 40, 40), tw_text, 15)


def mini_story(d, x, y, w, kicker, headline, body):
    """Compact story with no thumbnail; returns bottom y."""
    d.text((x, y), kicker, font=F(SANS_B, 12), fill=RED)
    yy = para(d, x, y + 17, headline, F(SERIF_B, 17), INK, w, 20)
    return para(d, x, yy + 1, body, F(SANS, 12), (40, 40, 40), w, 15)


def compose():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)
    d.rectangle([20, 20, W - 20, H - 20], outline=INK, width=1)

    # ---- Masthead ----
    title = "THE WORLD TODAY"
    tf = F(SERIF_B, 64)
    d.text(((W - d.textlength(title, font=tf)) / 2, 26), title,
           font=tf, fill=INK)
    rule(d, 28, 102, 996, 3)
    rule(d, 28, 108, 996, 1)
    d.text((28, 116), "SATURDAY, 21 NOVEMBER 2026",
           font=F(SANS_B, 15), fill=INK)
    right = "WORLD TELEVISION DAY"
    d.text((996 - d.textlength(right, font=F(SANS, 13)), 118), right,
           font=F(SANS, 13), fill=GRAY)
    rule(d, 28, 140, 996, 1)

    # ---- Lead story ----
    d.text((28, 152), "WAR IN EUROPE  ·  KYIV — WARSAW",
           font=F(SANS_B, 15), fill=RED)
    para(d, 28, 174, "400 DRONES, 110 MISSILES RAIN ON UKRAINE; TWO LAND IN POLAND",
         F(SERIF_B, 38), INK, 940, 44)
    thumb_sky(d, 28, 268, 968, 120)
    d.text((28, 392), "Kyiv's skyline under attack overnight; a Russian Kh-101 cruise "
           "missile came down in south-east Poland. NATO jets scrambled.",
           font=F(SERIF_I, 12), fill=GRAY)
    para(d, 28, 410,
         "Russia hit Ukraine overnight with more than 400 drones and 110 missiles, "
         "killing at least eight in Kyiv. Poland said two Russian missiles and a "
         "suspected drone came down on its territory; PM Tusk called it a "
         "deliberate provocation.",
         F(SANS, 14), (40, 40, 40), 940, 19)

    # ---- Stat strip (auto-fit so it never bleeds off the page) ----
    d.rectangle([28, 458, 996, 494], fill=NAVY)
    stats = ("S&P 500 -3.70%  ·  NASDAQ -5.28%  ·  DOW -1.93%  ·  NVIDIA -13.8%  ·  "
             "400+ DRONES  ·  110 MISSILES  ·  8 DEAD IN KYIV  ·  ICJ 9-6")
    sf = F(SANS_B, 15)
    while d.textlength(stats, font=sf) > 940 and sf.size > 10:
        sf = F(SANS_B, sf.size - 1)
    d.text(((W - d.textlength(stats, font=sf)) / 2, 469), stats,
           font=sf, fill=(255, 255, 255))

    # ---- Story grid, 2 x 2 ----
    story_cell(d, 28, 510, 474, 130, "MARKETS  ·  NEW YORK",
               "AI sell-off drags Wall Street into correction",
               "US stocks fell sharply as an AI and chip sell-off pushed the S&P 500 "
               "and the Dow into correction. Nvidia fell 13.8% as the SEC examines "
               "accounting issues.",
               thumb_chart)
    story_cell(d, 522, 510, 474, 130, "JUSTICE  ·  THE HAGUE",
               "UN court: Myanmar guilty of Rohingya genocide",
               "The International Court of Justice ruled 9-6 that Myanmar committed "
               "genocide against the Rohingya - the first time it has held a state "
               "responsible.",
               thumb_court)
    story_cell(d, 28, 654, 474, 130, "HEALTH  ·  LONDON",
               "Cancer pill makes tumours vanish in 1 in 12",
               "A trial of the pill daraxonrasib made pancreatic cancer undetectable "
               "on scans in one in 12 patients, a major step against a hard-to-treat "
               "disease.",
               thumb_pill)
    story_cell(d, 522, 654, 474, 130, "MIDDLE EAST  ·  RIYADH",
               "Houthi missiles aimed at Riyadh shot down",
               "The Saudi-led coalition said it intercepted three Houthi ballistic "
               "missiles headed for Riyadh, the third night of alerts, as Iranian "
               "tankers mass at Kharg Island.",
               thumb_desert)
    rule(d, 28, 794, 996, 1)

    # ---- Bottom band: climate + sport (left), briefs (right) ----
    by = mini_story(d, 28, 804, 460, "CLIMATE  ·  ANTALYA",
                    "COP31 talks miss deadline in Antalya",
                    "Climate talks in Antalya ran past their deadline; the draft "
                    "drops any mention of fossil fuels.")
    mini_story(d, 28, by + 8, 460, "SPORT  ·  WELLINGTON",
               "Rahul completes the SENA set",
               "KL Rahul's century made him the first Indian opener with Test "
               "hundreds in all four SENA countries.")
    d.rectangle([512, 804, 996, 954], fill=LIGHT)
    d.text((526, 812), "ALSO ON 21 NOVEMBER", font=F(SANS_B, 13), fill=RED)
    briefs = [
        "Gen Z protests sweep 25 European countries over costs, war and climate.",
        "Denmark expels Russian diplomat over alleged plot to kill a Ukrainian rapper.",
        "French police convicted over 2020 beating of producer Michel Zecler.",
        "Russian military plane crash in Siberia kills all 19 aboard.",
        "US approved nearly 900,000 AI chips for China, a House panel discloses.",
    ]
    yy = 834
    for b in briefs:
        yy = para(d, 526, yy, "•  " + b, F(SANS, 11), (40, 40, 40), 456, 14)

    # ---- DATE CHECK footer ----
    d.rectangle([28, 962, 996, 1000], outline=RED, width=2)
    d.rectangle([28, 962, 34, 1000], fill=RED)
    para(d, 44, 967,
         "DATE CHECK — Every story above happened or was first reported on "
         "Saturday 21 November 2026. NOT 21 Nov, so not shown: Peru earthquake "
         "(20 Nov) · Cyclone Akvan landfall (20 Nov) · Rikers Island closure plan "
         "(20 Nov) · Trump on Iran (20 Nov).",
         F(SANS_B, 11), INK, 940, 14)
    return img


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    img = compose()
    img.save(os.path.join(OUT_DIR, "entry.png"), "PNG")


if __name__ == "__main__":
    main()
