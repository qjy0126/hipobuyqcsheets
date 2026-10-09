#!/usr/bin/env python3
"""Generate crawlable product detail HTML with unique titles for SEO."""
from __future__ import annotations

import json
import re
import shutil
from collections import defaultdict
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGIN = "https://hipobuyqcsheets.com"
INVITE = "R71GHKM1I"
TODAY = "2026-09-29"

CAT_LABELS = {
    "shoes": "Shoes",
    "t-shirts": "T-Shirts",
    "hoodies": "Hoodies",
    "jackets": "Jackets",
    "pants": "Pants / Shorts",
    "sets": "Sets",
    "jersey": "Jerseys",
    "underwear": "Underwear",
    "headwear": "Headwear",
    "watches": "Watches",
    "accessories": "Accessories",
    "other": "Other",
    "glasses": "Glasses",
    "perfume": "Perfume",
    "bricks": "Building Blocks",
}


def load_products() -> list[dict]:
    raw = (ROOT / "js" / "catalog.js").read_text(encoding="utf-8")
    start = raw.index("KF.products = ") + len("KF.products = ")
    products, _ = json.JSONDecoder().raw_decode(raw[start:])
    return products


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower())
    s = re.sub(r"^-+|-+$", "", s)
    s = re.sub(r"-+", "-", s)
    return s[:60]


def item_id(p: dict) -> str:
    return re.sub(r"^p-", "", str(p.get("id") or ""), count=1)


def item_slug(p: dict) -> str:
    base = slugify(str(p.get("title") or ""))
    num = item_id(p)
    return f"{base}-{num}" if base else num


def listing(source_url: str) -> tuple[str, str]:
    url = source_url or ""
    weidian = re.search(r"itemID=(\d+)", url, re.I)
    if weidian or "weidian.com" in url.lower():
        pid = weidian.group(1) if weidian else ""
        return pid, "weidian"
    tb = re.search(r"[?&]id=(\d+)", url, re.I)
    if "taobao.com" in url.lower() or "tmall.com" in url.lower():
        return (tb.group(1) if tb else ""), "taobao"
    ali = re.search(r"offer/(\d+)", url, re.I)
    if "1688.com" in url.lower():
        return (ali.group(1) if ali else ""), "1688"
    return "", "weidian"


def hipobuy_url(source_url: str) -> str:
    pid, path = listing(source_url)
    raw = source_url or ""
    weidian = re.search(r"itemID=(\d+)", raw, re.I)
    if weidian:
        raw = f"https://weidian.com/item.html?itemID={weidian.group(1)}"
    from urllib.parse import quote
    enc = quote(raw, safe="")
    if pid:
        return (
            f"https://hipobuy.com/product/{path}/{pid}"
            f"?source=SEARCH_LIST&keyword={enc}&inviteCode={INVITE}"
        )
    return raw or "https://hipobuy.com/"


def product_card(p: dict) -> str:
    slug = item_slug(p)
    img = "/" + str(p.get("image") or "").lstrip("./")
    title = escape(str(p.get("title") or ""))
    price = float(p.get("price") or 0)
    return (
        f'<a class="product-card" href="/item/{escape(slug)}/">'
        f'<div class="thumb"><img src="{escape(img)}" alt="{title}" loading="lazy" decoding="async" /></div>'
        f"<h3>{title}</h3><b>${price:.2f}</b></a>"
    )


def item_page(p: dict, related: list[dict]) -> str:
    slug = item_slug(p)
    path = f"/item/{slug}/"
    canonical = ORIGIN + path
    name = str(p.get("title") or "Find")
    page_title = f"{name} — HipoBuySpreadsheet"
    price = float(p.get("price") or 0)
    cat = str(p.get("category") or "")
    label = CAT_LABELS.get(cat, cat.replace("-", " ").title() or "Find")
    source = str(p.get("source") or "Weidian")
    img_rel = "/" + str(p.get("image") or "").lstrip("./")
    img_abs = ORIGIN + img_rel
    desc = (
        f"{name} on the HipoBuySpreadsheet. {label} find from {source}, "
        f"listed at ${price:.2f}. Preview QC photos here, then open Hipobuy to order."
    )
    buy = hipobuy_url(str(p.get("sourceUrl") or ""))
    qc = "QC photos on this find" if p.get("qc") else "No QC flag yet"
    brand = str(p.get("collection") or "HipoBuySpreadsheet")
    ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "image": img_abs,
        "description": desc,
        "brand": {"@type": "Brand", "name": brand},
        "offers": {
            "@type": "Offer",
            "price": f"{price:.2f}",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": canonical,
        },
    }
    rel = "\n        ".join(product_card(r) for r in related[:8]) or "<p>More finds in the spreadsheet.</p>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(page_title)}</title>
  <meta name="description" content="{escape(desc)}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <link rel="canonical" href="{escape(canonical)}" />
  <meta property="og:type" content="product" />
  <meta property="og:site_name" content="hipobuyqcsheets" />
  <meta property="og:title" content="{escape(page_title)}" />
  <meta property="og:description" content="{escape(desc)}" />
  <meta property="og:url" content="{escape(canonical)}" />
  <meta property="og:image" content="{escape(img_abs)}" />
  <meta property="product:price:amount" content="{price:.2f}" />
  <meta property="product:price:currency" content="USD" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <link rel="icon" href="/img/logo.svg" type="image/svg+xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/styles.css" />
</head>
<body data-page="item" data-item-id="{escape(str(p.get('id') or ''))}">
  <header class="topbar">
    <div class="wrap topbar-row">
      <a class="brand" href="/index.html">
        <img src="/img/logo.svg" alt="" />
        <span class="brand-name">HipoBuy<b>Spreadsheet</b></span>
      </a>
      <nav class="nav">
        <a href="/index.html">Home</a>
        <a href="/guides/index.html">Guide</a>
        <a href="/how-to-buy.html">Help Center</a>
        <a class="pill" href="/browse.html">Spreadsheet ↗</a>
      </nav>
    </div>
  </header>
  <main class="wrap item-page">
    <nav class="crumbs">
      <a href="/index.html">Home</a><span>/</span>
      <a href="/browse.html">Shop</a><span>/</span>
      <a href="/browse.html?cat={escape(cat)}">{escape(label)}</a><span>/</span>
      <span>{escape(name)}</span>
    </nav>
    <div class="item-layout">
      <div class="gallery">
        <div class="main">
          <img src="{escape(img_rel)}" alt="{escape(name)}" />
        </div>
      </div>
      <div class="item-info">
        <h1>{escape(name)}</h1>
        <div class="price">${price:.2f}</div>
        <p class="item-rating">{escape(qc)} · {escape(source)}</p>
        <a class="btn btn-gold btn-buy" href="{escape(buy)}" target="_blank" rel="noopener">Buy on Hipobuy</a>
        <p class="item-note">{escape(desc)}</p>
      </div>
    </div>
    <section class="related">
      <h2>More {escape(label)} finds</h2>
      <div class="product-grid">{rel}</div>
    </section>
  </main>
  <footer class="site-footer">
    <div class="wrap foot-note">© 2026 hipobuyqcsheets — independent directory. Checkout stays on Hipobuy.</div>
  </footer>
</body>
</html>
"""


def main() -> None:
    products = load_products()
    by_cat: dict[str, list] = defaultdict(list)
    for p in products:
        by_cat[str(p.get("category") or "other")].append(p)

    item_root = ROOT / "item"
    if item_root.exists():
        shutil.rmtree(item_root)
    item_root.mkdir()

    slugs = []
    for p in products:
        slug = item_slug(p)
        cat = str(p.get("category") or "other")
        related = [x for x in by_cat[cat] if x.get("id") != p.get("id")][:8]
        folder = item_root / slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(item_page(p, related), encoding="utf-8")
        slugs.append(slug)

    static = [
        "/",
        "/browse.html",
        "/how-to-buy.html",
        "/about.html",
        "/privacy.html",
        "/disclaimer.html",
        "/guides/index.html",
        "/agents/index.html",
    ]
    for folder, prefix in (("guides", "/guides/"), ("agents", "/agents/"), ("c", "/c/")):
        d = ROOT / folder
        if d.exists():
            for f in sorted(d.glob("*.html")):
                if f.name == "index.html" and folder != "c":
                    continue
                path = f"{prefix}{f.name}"
                if path not in static:
                    static.append(path)
    urls = list(static) + [f"/item/{s}/" for s in slugs]
    body = "\n".join(
        f"  <url><loc>{ORIGIN}{u}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>{'daily' if u in ('/', '/browse.html') else 'weekly'}</changefreq>"
        f"<priority>{'1.0' if u == '/' else '0.9' if u == '/browse.html' else '0.6'}</priority></url>"
        for u in urls
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + body
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    robots = ROOT / "robots.txt"
    robots.write_text(
        f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n",
        encoding="utf-8",
    )
    print(f"wrote {len(slugs)} item pages + sitemap")


if __name__ == "__main__":
    main()
