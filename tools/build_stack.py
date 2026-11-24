"""Build the "Stack" section of index.html (PT) and en/index.html (EN) from the list below.

    python3 tools/build_stack.py

Logos: Simple Icons (CC0) drawn in the brand color, Devicon for Salesforce, and simple badges in the
brand color for tools without an open logo (dbt, Dataform, Power BI, Excel, Oracle, Sienge).
The section is written between the markers <!-- stack:start --> and <!-- stack:end -->.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "tools" / "icons"
COLORS = json.loads((ICONS / "brand_colors.json").read_text())

# Brands whose color has no contrast on the page: drawn in the text color instead.
INK = {"github", "pandas"}
# Yellow on light background: glyph on a tile of the brand color.
TILE = {"duckdb": ("#FFF000", "#000000")}


def simple_icon(slug: str) -> str:
    path = re.search(r'<path d="([^"]+)"', (ICONS / f"{slug}.svg").read_text()).group(1)
    if slug in TILE:
        bg, fg = TILE[slug]
        return (f'<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="5" fill="{bg}"/>'
                f'<path transform="translate(4 4) scale(.6667)" fill="{fg}" d="{path}"/></svg>')
    color = "currentColor" if slug in INK else f"#{COLORS[slug]}"
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="{color}" d="{path}"/></svg>'


def file_icon(name: str) -> str:
    svg = (ICONS / f"{name}.svg").read_text().strip()
    return svg.replace("<svg ", '<svg aria-hidden="true" ', 1)


def badge(text: str, bg: str, fg: str = "#ffffff", size: int = 9) -> str:
    return (f'<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="5" fill="{bg}"/>'
            f'<text x="12" y="15.6" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="700" '
            f'font-size="{size}" fill="{fg}">{text}</text></svg>')


GENERIC = {
    "sql": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#336791" stroke-width="1.8"><ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/><path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/></svg>',
    "api": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#0e9f6e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 4c-2 0-3 1-3 3v2c0 1.5-1 3-2.5 3C4 12 5 13.5 5 15v2c0 2 1 3 3 3M16 4c2 0 3 1 3 3v2c0 1.5 1 3 2.5 3-1.5 0-2.5 1.5-2.5 3v2c0 2-1 3-3 3"/></svg>',
    "etl": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#7c5cd6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h13M12 3l4 4-4 4M21 17H8M12 13l-4 4 4 4"/></svg>',
    "star": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#d97706" stroke-width="1.8" stroke-linejoin="round"><circle cx="12" cy="12" r="3.2" fill="#d97706" stroke="none"/><path d="M12 8.8V3M12 15.2V21M8.8 12H3M15.2 12H21"/><circle cx="12" cy="3" r="1.6"/><circle cx="12" cy="21" r="1.6"/><circle cx="3" cy="12" r="1.6"/><circle cx="21" cy="12" r="1.6"/></svg>',
    "test": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#16865b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.4-7.5 9.5-4.3-1.1-7.5-4.9-7.5-9.5V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>',
}

ICON = {
    "SQL": GENERIC["sql"],
    "Python": simple_icon("python"),
    "pandas": simple_icon("pandas"),
    "BigQuery": simple_icon("googlebigquery"),
    "Google Cloud": simple_icon("googlecloud"),
    "DuckDB": simple_icon("duckdb"),
    "dbt": badge("dbt", "#FF694B", size=10.5),
    "Dataform": badge("Df", "#4285F4", size=12),
    "Airflow": simple_icon("apacheairflow"),
    "ETL / ELT": GENERIC["etl"],
    "Star Schema": GENERIC["star"],
    "Power BI": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="11" width="4.5" height="10" rx="1.2" fill="#F2C811"/><rect x="9.75" y="7" width="4.5" height="14" rx="1.2" fill="#E8B100"/><rect x="16.5" y="3" width="4.5" height="18" rx="1.2" fill="#C99A00"/></svg>',
    "DAX": badge("fx", "#F2C811", "#1a1a1a", 13),
    "Power Query": badge("M", "#F2C811", "#1a1a1a", 13),
    "Excel": badge("X", "#217346", size=13),
    "Git": simple_icon("git"),
    "GitHub": simple_icon("github"),
    "Bitbucket": simple_icon("bitbucket"),
    "GitHub Actions": simple_icon("githubactions"),
    "Data tests": GENERIC["test"],
    "Oracle": badge("O", "#C74634", size=13),
    "APIs REST": GENERIC["api"],
    "SAP": simple_icon("sap"),
    "Salesforce": file_icon("salesforce"),
    "HubSpot": simple_icon("hubspot"),
    "Sienge": badge("S", "#0B3B66", size=13),
}

GROUPS = [
    # (PT title, EN title, items: (label, EN label or None))
    ("Linguagens", "Languages", [("SQL", None), ("Python", None), ("pandas", None)]),
    ("Cloud & Data Warehouse", "Cloud & Data Warehouse", [("BigQuery", None), ("Google Cloud", None), ("DuckDB", None)]),
    ("Engenharia de Dados", "Data Engineering", [("dbt", None), ("Dataform", None), ("Airflow", None), ("ETL / ELT", None), ("Star Schema", None)]),
    ("Business Intelligence", "Business Intelligence", [("Power BI", None), ("DAX", None), ("Power Query", None), ("Excel", None)]),
    ("Versionamento & Qualidade", "Version control & Quality", [("Git", None), ("GitHub", None), ("Bitbucket", None), ("GitHub Actions", "GitHub Actions"), ("Data tests", "Data tests")]),
    ("Integrações & Fontes", "Integrations & Sources", [("Oracle", None), ("APIs REST", "REST APIs"), ("SAP", None), ("Salesforce", None), ("HubSpot", None), ("Sienge", None)]),
]
PT_LABELS = {"Data tests": "Testes de dados", "GitHub Actions": "GitHub Actions (CI)"}
EN_LABELS = {"GitHub Actions": "GitHub Actions (CI)"}

HEAD = {
    "pt": ("Stack", "As ferramentas que uso no dia a dia, do dado bruto ao dashboard."),
    "en": ("Stack", "The tools I use day to day, from raw data to dashboard."),
}


def section(lang: str) -> str:
    title, sub = HEAD[lang]
    cards = []
    for pt_title, en_title, items in GROUPS:
        chips = []
        for label, en_label in items:
            shown = (PT_LABELS.get(label, label) if lang == "pt" else EN_LABELS.get(label, en_label or label))
            chips.append(f'<li class="skill">{ICON[label]}<span>{shown}</span></li>')
        cards.append(f'      <div class="skill-group"><h3>{pt_title if lang == "pt" else en_title}</h3>'
                     f'<ul>{"".join(chips)}</ul></div>')
    return ("<!-- stack:start -->\n"
            f'<section id="stack">\n  <div class="wrap">\n    <div class="section-head">\n'
            f"      <h2>{title}</h2>\n      <p>{sub}</p>\n    </div>\n"
            f'    <div class="skills">\n' + "\n".join(cards) + "\n    </div>\n  </div>\n</section>\n"
            "<!-- stack:end -->")


def inject(page: Path, lang: str) -> None:
    html = page.read_text(encoding="utf-8")
    block = section(lang)
    if "<!-- stack:start -->" in html:
        html = re.sub(r"<!-- stack:start -->.*?<!-- stack:end -->", lambda _: block, html, flags=re.S)
    else:  # first run: right after the hero
        html = html.replace("</header>\n", "</header>\n\n" + block + "\n", 1)
    page.write_text(html, encoding="utf-8")
    print(f"  {page.relative_to(ROOT)}: {sum(len(g[2]) for g in GROUPS)} skills")


if __name__ == "__main__":
    inject(ROOT / "index.html", "pt")
    inject(ROOT / "en" / "index.html", "en")
