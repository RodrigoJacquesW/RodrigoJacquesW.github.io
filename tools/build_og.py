"""Social preview image (LinkedIn/WhatsApp link card): assets/img/og.png, 1200x630.

    python3 tools/build_og.py      # needs playwright + chromium (dev only)
"""

import base64
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_stack import ICON  # noqa: E402

photo = base64.b64encode((ROOT / "assets" / "img" / "rodrigo.jpg").read_bytes()).decode()

# circuit traces, same idea as the site background
random.seed(4)
lines = []
for _ in range(70):
    x, y = random.randrange(0, 1200, 24), random.randrange(0, 630, 24)
    pts = [(x, y)]
    for _ in range(random.randint(2, 4)):
        if random.random() < 0.5:
            x += random.choice([-1, 1]) * 24 * random.randint(2, 6)
        else:
            y += random.choice([-1, 1]) * 24 * random.randint(2, 5)
        pts.append((x, y))
    d = "M" + " L".join(f"{a},{b}" for a, b in pts)
    lines.append(f'<path d="{d}"/><circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="3.5"/>')

chips = "".join(f'<span class="chip">{ICON[k]}{k}</span>' for k in
                ["SQL", "Python", "BigQuery", "dbt", "Dataform", "Airflow", "Power BI", "Git"])

html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
<style>
  html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
  body {{ background: radial-gradient(900px 500px at 78% 40%, #17304f 0%, #0f1520 60%); color: #eef0f3;
          font-family: Inter, sans-serif; position: relative; }}
  svg.bg {{ position: absolute; inset: 0; }}
  svg.bg path {{ fill: none; stroke: rgba(90,156,240,.16); stroke-width: 2; }}
  svg.bg circle {{ fill: none; stroke: rgba(90,156,240,.3); stroke-width: 2; }}
  .wrap {{ position: absolute; inset: 0; padding: 70px 72px; display: grid; grid-template-columns: 1fr 300px; gap: 40px; align-items: center; }}
  .eyebrow {{ font-size: 22px; color: #8fb8f2; font-weight: 600; letter-spacing: .02em; }}
  h1 {{ font-family: "Space Grotesk", sans-serif; font-size: 76px; line-height: 1.02; margin: 14px 0 16px; letter-spacing: -.02em; }}
  .role {{ font-family: "Space Grotesk", sans-serif; font-size: 34px; color: #5a9cf0; font-weight: 600; margin-bottom: 34px; }}
  .role span {{ color: #6b7380; font-weight: 400; margin: 0 6px; }}
  .chips {{ display: flex; flex-wrap: wrap; gap: 12px; }}
  .chip {{ display: inline-flex; align-items: center; gap: 10px; padding: 10px 16px 10px 12px; border-radius: 12px;
           background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.12); font-size: 22px; font-weight: 600; color: #eef0f3; }}
  .chip svg {{ width: 28px; height: 28px; color: #eef0f3; }}
  .photo {{ width: 300px; height: 300px; border-radius: 50%; object-fit: cover; border: 6px solid #1f6fd1;
            box-shadow: 0 0 0 10px rgba(31,111,209,.18), 0 20px 60px rgba(0,0,0,.45); }}
  .url {{ position: absolute; right: 72px; bottom: 40px; font-size: 22px; color: #8d939d; }}
</style></head><body>
<svg class="bg" viewBox="0 0 1200 630">{''.join(lines)}</svg>
<div class="wrap">
  <div>
    <div class="eyebrow">Portfólio de dados · Florianópolis</div>
    <h1>Rodrigo Jacques Wolff</h1>
    <div class="role">Analytics Engineer <span>·</span> Engenharia de Dados</div>
    <div class="chips">{chips}</div>
  </div>
  <img class="photo" src="data:image/jpeg;base64,{photo}">
</div>
<div class="url">rodrigojacquesw.github.io</div>
</body></html>"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.set_content(html, wait_until="networkidle")
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(ROOT / "assets" / "img" / "og.png"))
        b.close()
    print("assets/img/og.png")
