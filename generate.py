#!/usr/bin/env python3
"""Generate Findsheet static HTML site."""
from pathlib import Path
import json
import html as H

ROOT = Path(__file__).resolve().parent

SITE = {
    "name": "Findsheet",
    "tagline": "HipoBuySpreadsheet",
    "url": "https://findsheet.com",
    "description": "Findsheet is an independent HipoBuySpreadsheet directory — browse finds by category, compare prices, open Weidian / Taobao / 1688 links, then paste into Hipobuy.",
}

CATEGORIES = [
    ("shoes", "Shoes", "Shoes", "Sneakers and footwear finds from Weidian, Taobao and 1688."),
    ("t-shirts", "T-Shirts", "Tees", "Graphic tees and logo shirts for agent shopping."),
    ("hoodies", "Hoodies", "Hoodies", "Hoodies and sweaters for haul planning."),
    ("jackets", "Jackets", "Jackets", "Outerwear finds — plan shipping weight early."),
    ("pants-shorts", "Pants & Shorts", "Bottoms", "Jeans, cargos and shorts with size-chart checks."),
    ("bags", "Bags", "Bags", "Crossbody, tote and backpack finds."),
    ("accessories", "Accessories", "Accessories", "Belts, wallets, jewelry and small goods."),
    ("watches", "Watches", "Watches", "Watch finds — verify seller details before paying."),
    ("jerseys", "Jerseys", "Jerseys", "Football and sports jersey finds."),
    ("electronics", "Electronics", "Electronics", "Headphones and gadgets — check battery shipping rules."),
    ("headwear", "Headwear", "Hats", "Caps and beanies that pack light."),
    ("women", "Women", "Women", "Women's streetwear and wardrobe finds."),
]

PRODUCTS = [
    {"slug":"comme-des-garcons-play-grey-tee","title":"Comme des Garçons Play Grey T-Shirt","brand":"Comme des Garçons","category":"t-shirts","price":117,"source":"Weidian","summary":"Grey heart logo tee find — confirm print and size chart on the live listing before Hipobuy."},
    {"slug":"nocta-black-short-sleeve-tee","title":"Nocta Black Short Sleeve T-Shirt","brand":"Nocta","category":"t-shirts","price":147,"source":"Weidian","summary":"Black short-sleeve tee — check fabric weight and variants before ordering."},
    {"slug":"stussy-black-dice-graphic-tee","title":"Stussy Black Dice Graphic T-Shirt","brand":"Stussy","category":"t-shirts","price":114,"source":"Taobao","summary":"Dice graphic tee — compare print sharpness across seller photos."},
    {"slug":"supreme-white-logo-tee","title":"Supreme White Logo T-Shirt","brand":"Supreme","category":"t-shirts","price":111,"source":"Weidian","summary":"White logo tee — treat as a discovery lead; verify batch on source page."},
    {"slug":"bape-white-short-sleeve-tee","title":"A Bathing Ape White Short Sleeve T-Shirt","brand":"A Bathing Ape","category":"t-shirts","price":116,"source":"1688","summary":"White Bape-style tee — inspect print edges in warehouse QC."},
    {"slug":"amiri-black-white-tee","title":"Amiri Black and White Short Sleeve T-Shirt","brand":"Amiri","category":"t-shirts","price":109.82,"source":"Weidian","summary":"Contrast tee — print and collar shape are worth a QC pause."},
    {"slug":"travis-fragment-low-sneakers","title":"Travis Fragment Low Sneakers","brand":"Nike","category":"shoes","price":420,"source":"Weidian","summary":"Fragment low find — confirm size and sole batch photos on the seller page."},
    {"slug":"dunk-panda-low-sneakers","title":"Panda Dunk Low Sneakers","brand":"Nike","category":"shoes","price":289,"source":"Weidian","summary":"Black/white Dunk low — check toebox shape and leather in QC."},
    {"slug":"new-balance-550-white-grey","title":"New Balance 550 White Grey","brand":"New Balance","category":"shoes","price":310,"source":"Taobao","summary":"550 white/grey — sneakers add parcel mass; plan shipping early."},
    {"slug":"salomon-xt6-black-sneakers","title":"Salomon XT-6 Black Trail Sneakers","brand":"Salomon","category":"shoes","price":398,"source":"Weidian","summary":"XT-6 trail silhouette — confirm sole and mesh against references."},
    {"slug":"jordan-4-military-black","title":"Jordan 4 Military Black","brand":"Jordan","category":"shoes","price":455,"source":"Weidian","summary":"Military Black AJ4 — cage shape and heel tab are common QC focus."},
    {"slug":"balenciaga-triple-s-white","title":"Balenciaga Triple S White Sneakers","brand":"Balenciaga","category":"shoes","price":480,"source":"Weidian","summary":"Triple S find — sole stack and mudguard paint need close QC."},
    {"slug":"essentials-fear-of-god-hoodie-black","title":"Essentials Fear of God Black Hoodie","brand":"Essentials","category":"hoodies","price":198,"source":"Weidian","summary":"Black hoodie — check print and oversized fit notes on the listing."},
    {"slug":"stussy-basic-logo-hoodie-ash","title":"Stussy Basic Logo Hoodie Ash","brand":"Stussy","category":"hoodies","price":176,"source":"Taobao","summary":"Ash logo hoodie — confirm sleeve length in size chart."},
    {"slug":"nike-tech-fleece-hoodie-grey","title":"Nike Tech Fleece Hoodie Grey","brand":"Nike","category":"hoodies","price":245,"source":"Weidian","summary":"Tech fleece style — zipper and cuff finish deserve a QC pass."},
    {"slug":"canada-goose-expedition-parka-navy","title":"Canada Goose Expedition Parka Navy","brand":"Canada Goose","category":"jackets","price":680,"source":"Weidian","summary":"Heavy parka — high shipping weight; compare badges carefully."},
    {"slug":"the-north-face-nuptse-black","title":"The North Face Nuptse Black Puffer","brand":"The North Face","category":"jackets","price":320,"source":"Taobao","summary":"Nuptse-style puffer — loft and stitching in multi-angle QC."},
    {"slug":"carhartt-detroit-jacket-brown","title":"Carhartt Detroit Jacket Brown","brand":"Carhartt","category":"jackets","price":268,"source":"1688","summary":"Work jacket — lining and pocket stitching are common checkpoints."},
    {"slug":"cargo-pants-black-wide","title":"Black Wide Cargo Pants","brand":"Unbranded","category":"pants-shorts","price":129,"source":"Weidian","summary":"Wide cargos — measure inseam and thigh; fits vary by batch."},
    {"slug":"denim-tears-jeans-indigo","title":"Denim Tears Indigo Jeans","brand":"Denim Tears","category":"pants-shorts","price":210,"source":"Weidian","summary":"Indigo denim — wash and embroidery need careful QC."},
    {"slug":"nike-sportswear-shorts-black","title":"Nike Sportswear Shorts Black","brand":"Nike","category":"pants-shorts","price":89,"source":"Taobao","summary":"Black shorts — light haul filler; still confirm logo embroidery."},
    {"slug":"lv-keepall-bandouliere-bag","title":"Louis Vuitton Keepall Bandouliere Bag","brand":"Louis Vuitton","category":"bags","price":520,"source":"Weidian","summary":"Keepall-style bag — canvas texture and hardware are priority QC."},
    {"slug":"chrome-hearts-cross-body-bag","title":"Chrome Hearts Cross Body Bag","brand":"Chrome Hearts","category":"bags","price":340,"source":"Weidian","summary":"Cross-body bag — zipper pull and leather edges in QC photos."},
    {"slug":"hermes-belt-black-gold","title":"Hermès Black Gold Buckle Belt","brand":"Hermès","category":"accessories","price":188,"source":"Taobao","summary":"Belt find — buckle finish and leather stamp clarity."},
    {"slug":"chrome-hearts-cross-pendant","title":"Chrome Hearts Cross Pendant","brand":"Chrome Hearts","category":"accessories","price":95,"source":"Weidian","summary":"Cross pendant — casting sharpness and clasp in close-ups."},
    {"slug":"rolex-submariner-homage","title":"Submariner Style Dive Watch","brand":"Homage","category":"watches","price":450,"source":"1688","summary":"Dive watch homage — confirm movement type with seller before paying."},
    {"slug":"casio-gshock-black","title":"G-Shock Style Black Digital Watch","brand":"Casio","category":"watches","price":120,"source":"Taobao","summary":"Digital watch find — lighter shipping; verify module functions."},
    {"slug":"brazil-home-jersey-2024","title":"Brazil Home Football Jersey","brand":"Nike","category":"jerseys","price":99,"source":"Weidian","summary":"Brazil home kit style — print heat and collar stitching in QC."},
    {"slug":"argentina-away-jersey-messi","title":"Argentina Away Jersey Messi Print","brand":"Adidas","category":"jerseys","price":105,"source":"Weidian","summary":"Argentina away jersey — name/number alignment in QC."},
    {"slug":"airpods-max-silver-homage","title":"AirPods Max Style Over-Ear Headphones","brand":"Homage","category":"electronics","price":280,"source":"1688","summary":"Over-ear headphones — confirm battery shipping rules for your country."},
    {"slug":"sony-wh1000xm-style-headphones","title":"WH-1000XM Style Noise Cancelling Headphones","brand":"Homage","category":"electronics","price":260,"source":"Taobao","summary":"ANC headphones — electronics can face stricter customs."},
    {"slug":"new-era-yankees-fitted-cap","title":"New Era Yankees Fitted Cap","brand":"New Era","category":"headwear","price":78,"source":"Weidian","summary":"Yankees fitted cap — brim curve and embroidery density."},
    {"slug":"stussy-stock-beanie-black","title":"Stussy Stock Logo Beanie Black","brand":"Stussy","category":"headwear","price":65,"source":"Taobao","summary":"Black beanie — light filler; still QC knit quality."},
    {"slug":"acne-studios-scarf-women","title":"Acne Studios Style Wool Scarf","brand":"Acne Studios","category":"women","price":145,"source":"Weidian","summary":"Wool scarf — fringe finish and logo tag in QC."},
    {"slug":"skims-style-bodysuit-black","title":"Skims Style Black Bodysuit","brand":"Skims","category":"women","price":98,"source":"Taobao","summary":"Bodysuit — stretch fabric and seams vary; use size chart + QC."},
    {"slug":"ugg-style-platform-boot-women","title":"UGG Style Platform Boot","brand":"UGG","category":"women","price":230,"source":"Weidian","summary":"Platform boot — sole height adds weight; plan shipping early."},
]

AGENTS = [
    ("hipobuy", "Hipobuy", "Paste Weidian / Taobao / 1688 links, review warehouse QC, then ship internationally."),
    ("cnfans", "CNFans", "Compatible agent for the same marketplace links — useful for a second quote."),
    ("kakobuy", "Kakobuy", "Another agent option for Findsheet directory links."),
    ("mulebuy", "Mulebuy", "Beginner-friendly agent path for the same spreadsheet finds."),
    ("sugargoo", "Sugargoo", "Use Findsheet for discovery, Sugargoo for purchasing and freight."),
    ("allchinabuy", "AllChinaBuy", "Backup agent quote for weight-sensitive parcels."),
]

GUIDES = [
    ("what-is-a-hipobuy-spreadsheet", "What is a HipoBuySpreadsheet?", "A curated directory of Weidian, Taobao and 1688 links you paste into a shopping agent."),
    ("how-to-buy-from-hipobuy", "How to buy from Hipobuy", "Find a listing, paste into Hipobuy, review QC, choose a shipping line."),
    ("hipobuy-qc-photos-checklist", "Hipobuy QC photos checklist", "What to inspect before approving international shipping."),
    ("best-hipobuy-spreadsheet-approach-2026", "Best HipoBuySpreadsheet approach 2026", "Product pages + category hubs beat guide-only sites for long-term SEO."),
]

CAT_MAP = {c[0]: c for c in CATEGORIES}


def esc(s):
    return H.escape(str(s))


def price(p):
    return f"¥{p:g}" if isinstance(p, float) and p % 1 else f"¥{int(p) if float(p)==int(p) else p}"


def tone(slug):
    return f"tone-{(sum(map(ord, slug)) % 5) + 1}"


def cat_name(slug):
    return CAT_MAP.get(slug, (slug, slug, slug, ""))[1]


def cat_short(slug):
    return CAT_MAP.get(slug, (slug, slug, slug, ""))[2]


def depth_prefix(depth):
    return "../" * depth if depth else ""


def head(title, description, path, depth=0, extra=""):
    base = depth_prefix(depth)
    canon = f"{SITE['url']}{path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <link rel="canonical" href="{esc(canon)}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:url" content="{esc(canon)}" />
  <meta property="og:type" content="website" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Syne:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{base}css/styles.css" />
  {extra}
</head>
<body>
"""


def header(depth=0):
    b = depth_prefix(depth)
    cats = "".join(
        f'<a href="{b}c/{slug}.html">{esc(short)}</a>' for slug, _, short, _ in CATEGORIES
    )
    return f"""  <header class="site-header">
    <div class="wrap header-top">
      <a class="brand" href="{b}index.html">
        <strong>{esc(SITE['name'])}</strong>
        <span>{esc(SITE['tagline'])}</span>
      </a>
      <nav class="nav" aria-label="Primary">
        <a href="{b}browse.html">Browse</a>
        <a href="{b}guides/index.html">Guides</a>
        <a href="{b}agents/index.html">Agents</a>
        <a href="{b}how-to-buy.html">How to buy</a>
      </nav>
      <a class="btn btn-accent btn-sm" href="{b}browse.html">Open sheet</a>
    </div>
    <div class="wrap cat-bar">{cats}</div>
  </header>
  <main>
"""


def footer(depth=0):
    b = depth_prefix(depth)
    return f"""  </main>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <p class="display" style="font-size:1.8rem;margin:0">{esc(SITE['name'])}</p>
        <p class="prose" style="margin-top:0.75rem">Independent HipoBuySpreadsheet directory. Not affiliated with Hipobuy. Always confirm stock, price and warehouse QC before shipping.</p>
      </div>
      <div>
        <h3>Browse</h3>
        <ul>
          <li><a href="{b}browse.html">All finds</a></li>
          <li><a href="{b}c/shoes.html">Shoes</a></li>
          <li><a href="{b}c/t-shirts.html">T-Shirts</a></li>
          <li><a href="{b}c/hoodies.html">Hoodies</a></li>
        </ul>
      </div>
      <div>
        <h3>Learn</h3>
        <ul>
          <li><a href="{b}guides/what-is-a-hipobuy-spreadsheet.html">What is a HipoBuySpreadsheet?</a></li>
          <li><a href="{b}how-to-buy.html">How to buy</a></li>
          <li><a href="{b}agents/hipobuy.html">Hipobuy agent</a></li>
          <li><a href="{b}about.html">About</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap footer-note">© 2026 {esc(SITE['name'])}. Edit files in the <code>html/</code> folder.</div>
  </footer>
</body>
</html>
"""


def product_card(p, depth=0):
    b = depth_prefix(depth)
    return f"""      <article class="product-card">
        <a href="{b}p/{esc(p['slug'])}.html">
          <div class="thumb {tone(p['slug'])}">
            <div class="thumb-meta"><b>{esc(p['brand'][:1])}</b><span>{esc(p['source'])}</span></div>
          </div>
          <div class="meta">
            <div class="row">
              <h3>{esc(p['title'])}</h3>
              <span class="price">{price(p['price'])}</span>
            </div>
            <p class="cat">{esc(cat_short(p['category']))}</p>
          </div>
        </a>
      </article>
"""


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def page_index():
    cards = "".join(product_card(p) for p in PRODUCTS[:12])
    cats = "".join(
        f'<a class="cat-card" href="c/{slug}.html">{esc(short)}</a>'
        for slug, _, short, _ in CATEGORIES
    )
    guides = "".join(
        f'<a href="guides/{slug}.html" style="display:block;border-bottom:1px solid var(--line);padding:1rem 0"><p style="margin:0;font-size:0.7rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--muted)">Guide</p><p style="margin:0.35rem 0 0;font-size:1.1rem">{esc(title)}</p><p style="margin:0.35rem 0 0;color:var(--muted);font-size:0.9rem">{esc(excerpt)}</p></a>'
        for slug, title, excerpt in GUIDES
    )
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "name": SITE["name"],
                "url": SITE["url"],
                "description": SITE["description"],
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": f"{SITE['url']}/browse.html?q={{search_term_string}}",
                    "query-input": "required name=search_term_string",
                },
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "What is the best HipoBuySpreadsheet to use?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Use a directory with unique product pages, category hubs, and QC guidance. Findsheet is built as an independent HipoBuySpreadsheet focused on browse speed and SEO.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "Is Findsheet affiliated with Hipobuy?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "No. Findsheet is independent and does not sell products or process orders.",
                        },
                    },
                ],
            },
        ],
    }
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    body = f"""{head(f"{SITE['tagline']}: Browse Finds, Prices & QC | {SITE['name']}", SITE['description'], '/', 0, extra)}
{header(0)}
    <section class="hero">
      <div class="hero-grid" aria-hidden="true"></div>
      <div class="wrap hero-inner">
        <div>
          <h1>{esc(SITE['name'])}</h1>
          <p class="lead">HipoBuySpreadsheet built for search — product pages, category hubs, and QC-first shopping guidance.</p>
          <p class="sub">Browse finds, open Weidian / Taobao / 1688 listings, paste into Hipobuy. Independent directory — not operated by Hipobuy.</p>
          <div class="cta-row">
            <a class="btn" href="browse.html">Browse spreadsheet</a>
            <a class="btn btn-ghost" href="how-to-buy.html">How to buy</a>
          </div>
        </div>
        <div>
          <form class="search-box" action="browse.html" method="get" role="search">
            <label class="sr-only" for="q" style="position:absolute;left:-9999px">Search</label>
            <input id="q" name="q" placeholder="Search brand, item, category…" />
            <button type="submit">Search</button>
          </form>
          <div class="stats">
            <div><strong>8,600+</strong><span>Target listings</span></div>
            <div><strong>12</strong><span>Categories</span></div>
            <div><strong>SEO</strong><span>Product URLs</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div>
            <h2>Browse by category</h2>
            <p class="muted">Each hub is a unique HTML page for long-term SEO.</p>
          </div>
          <a href="browse.html">View all</a>
        </div>
        <div class="cat-grid">{cats}</div>
      </div>
    </section>

    <section class="section band">
      <div class="wrap">
        <div class="section-head">
          <div>
            <h2>Latest spreadsheet finds</h2>
            <p class="muted">Seed catalog — replace titles and links with your real finds later.</p>
          </div>
        </div>
        <div class="product-grid">{cards}</div>
        <p style="margin-top:2rem"><a class="btn btn-accent" href="browse.html">Browse all finds</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap" style="display:grid;gap:2.5rem">
        <div>
          <h2 class="display" style="font-size:1.9rem;margin:0">Why Findsheet ranks better over time</h2>
          <ul class="prose">
            <li><strong style="color:var(--ink)">Unique product HTML pages</strong> — long-tail brand/item queries.</li>
            <li><strong style="color:var(--ink)">Category hubs</strong> — one clear page per shopping intent.</li>
            <li><strong style="color:var(--ink)">Guides + agents</strong> — informational keywords without burying the catalog.</li>
          </ul>
        </div>
        <div>
          <h2 class="display" style="font-size:1.9rem;margin:0">Guides</h2>
          {guides}
        </div>
      </div>
    </section>

    <section class="section band-soft">
      <div class="wrap faq">
        <h2 class="display" style="font-size:1.9rem;margin:0 0 1rem">FAQ</h2>
        <details open>
          <summary>What is the best HipoBuySpreadsheet to use?</summary>
          <p>Use a directory with unique product pages, fresh category hubs, and clear QC guidance. Findsheet is built for that.</p>
        </details>
        <details>
          <summary>Is Findsheet affiliated with Hipobuy?</summary>
          <p>No. Findsheet is independent and does not sell products or process orders. Paste source links into Hipobuy or another agent.</p>
        </details>
        <details>
          <summary>How do I check Hipobuy QC photos?</summary>
          <p>After the item reaches the warehouse, open QC photos in your agent account before approving international shipping.</p>
        </details>
      </div>
    </section>
{footer(0)}"""
    write(ROOT / "index.html", body)


def page_browse():
    cards = "".join(product_card(p) for p in PRODUCTS)
    body = f"""{head('Browse HipoBuySpreadsheet Finds | Findsheet', 'Browse the Findsheet HipoBuySpreadsheet directory — search brands and categories.', '/browse.html')}
{header(0)}
    <div class="wrap page-hero">
      <h1>Browse spreadsheet</h1>
      <p class="prose">All seed finds on one page. Open any product HTML file to edit title, price and source link.</p>
      <form class="search-box" style="max-width:28rem;margin-top:1.5rem" action="browse.html" method="get">
        <input id="filter" name="q" placeholder="Filter on this page…" />
        <button type="submit">Filter</button>
      </form>
    </div>
    <div class="wrap section" style="padding-top:1rem">
      <div class="product-grid" id="grid">{cards}</div>
    </div>
    <script src="js/filter.js"></script>
{footer(0)}"""
    write(ROOT / "browse.html", body)


def page_categories():
    for slug, name, short, desc in CATEGORIES:
        items = [p for p in PRODUCTS if p["category"] == slug]
        cards = "".join(product_card(p, 1) for p in items) or '<p class="prose">No seed items in this category yet.</p>'
        body = f"""{head(f'HipoBuySpreadsheet {name} — Finds & Links | Findsheet', f'Browse {name.lower()} finds from the Findsheet HipoBuySpreadsheet. {desc}', f'/c/{slug}.html', 1)}
{header(1)}
    <div class="wrap page-hero">
      <nav class="crumbs"><a href="../index.html">Home</a> / <a href="../browse.html">Browse</a> / {esc(name)}</nav>
      <h1>{esc(name)}</h1>
      <p class="prose">{esc(desc)} Open a product page, confirm the live listing, paste into Hipobuy.</p>
      <p style="font-size:0.72rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--muted)">{len(items)} finds</p>
    </div>
    <div class="wrap section" style="padding-top:1rem">
      <div class="product-grid">{cards}</div>
    </div>
{footer(1)}"""
        write(ROOT / "c" / f"{slug}.html", body)


def page_products():
    for p in PRODUCTS:
        related = [x for x in PRODUCTS if x["category"] == p["category"] and x["slug"] != p["slug"]][:4]
        rel = "".join(product_card(x, 1) for x in related)
        cname = cat_name(p["category"])
        ld = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": p["title"],
            "description": p["summary"],
            "brand": {"@type": "Brand", "name": p["brand"]},
            "offers": {
                "@type": "Offer",
                "priceCurrency": "CNY",
                "price": p["price"],
                "availability": "https://schema.org/InStock",
                "url": f"{SITE['url']}/p/{p['slug']}.html",
            },
        }
        extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
        body = f"""{head(f"{p['title']} — HipoBuySpreadsheet Find | Findsheet", f"{p['title']} · est. {price(p['price'])} · {p['source']}. Confirm live listing, then paste into Hipobuy.", f"/p/{p['slug']}.html", 1, extra)}
{header(1)}
    <div class="wrap page-hero">
      <nav class="crumbs"><a href="../index.html">Home</a> / <a href="../c/{esc(p['category'])}.html">{esc(cname)}</a> / Find</nav>
    </div>
    <div class="wrap product-layout">
      <div class="product-visual {tone(p['slug'])}">
        <p style="margin:0;font-size:0.72rem;letter-spacing:0.18em;text-transform:uppercase;opacity:0.7">{esc(p['source'])}</p>
        <p class="big">{esc(p['brand'][:2])}</p>
        <p style="margin-top:3rem;opacity:0.7;font-size:0.9rem">Replace with product image later.</p>
      </div>
      <div>
        <p style="margin:0;font-size:0.72rem;letter-spacing:0.16em;text-transform:uppercase;color:var(--muted)">{esc(p['brand'])}</p>
        <h1 style="margin:0.4rem 0 0;font-family:Syne,sans-serif;font-size:clamp(1.8rem,4vw,2.8rem)">{esc(p['title'])}</h1>
        <p class="price-lg">{price(p['price'])}</p>
        <p style="margin:0;font-size:0.72rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--muted)">Estimate · confirm on source listing</p>
        <p class="prose" style="margin-top:1.25rem">{esc(p['summary'])}</p>
        <div class="cta-row">
          <a class="btn" href="https://example.com/listing/{esc(p['slug'])}" rel="nofollow noopener" target="_blank">Open source listing</a>
          <a class="btn btn-ghost" href="../how-to-buy.html">Paste into Hipobuy</a>
        </div>
        <div class="checklist">
          <strong>Buyer checklist</strong>
          <ol>
            <li>Confirm stock, size and photos on the live marketplace page.</li>
            <li>Paste the URL into Hipobuy (or CNFans / Kakobuy / Mulebuy).</li>
            <li>Review warehouse QC photos before approving shipping.</li>
          </ol>
        </div>
      </div>
    </div>
    {"<div class='wrap section'><h2 class='display' style='font-size:1.8rem;margin:0 0 1.5rem'>Related " + esc(cname) + "</h2><div class='product-grid'>" + rel + "</div></div>" if related else ""}
{footer(1)}"""
        write(ROOT / "p" / f"{p['slug']}.html", body)


def page_guides():
    links = "".join(
        f'<a href="{slug}.html" style="display:block;border:1px solid var(--line);background:var(--paper);padding:1.25rem;margin-bottom:0.75rem"><h2 style="margin:0;font-family:Syne,sans-serif;font-size:1.35rem">{esc(title)}</h2><p style="margin:0.5rem 0 0;color:var(--muted);font-size:0.9rem">{esc(excerpt)}</p></a>'
        for slug, title, excerpt in GUIDES
    )
    write(
        ROOT / "guides" / "index.html",
        f"""{head('HipoBuySpreadsheet Guides | Findsheet', 'Guides for HipoBuySpreadsheet shopping, QC and SEO.', '/guides/index.html', 1)}
{header(1)}
    <div class="wrap page-hero"><h1>Guides</h1><p class="prose">Informational pages that support catalog SEO.</p></div>
    <div class="wrap section" style="padding-top:0.5rem">{links}</div>
{footer(1)}""",
    )

    bodies = {
        "what-is-a-hipobuy-spreadsheet": [
            ("Short definition", "A HipoBuySpreadsheet is community shorthand for a browsable collection of Chinese marketplace product links. You discover an item, open the live seller page, then paste that URL into Hipobuy."),
            ("What Findsheet adds", "Findsheet turns the old slow-sheet habit into category hubs and product HTML pages that search engines can index."),
            ("What it is not", "It is not Hipobuy itself, not a payment processor, and not a guarantee of stock. Always re-check the live page and warehouse QC."),
        ],
        "how-to-buy-from-hipobuy": [
            ("1. Find and verify", "Browse Findsheet by category. Open the source listing and confirm photos, variants, price and availability."),
            ("2. Paste into Hipobuy", "Copy the product URL into Hipobuy or another agent. Choose size/color, then pay item cost."),
            ("3. Warehouse QC", "Review QC photos from multiple angles. GL only when you are comfortable."),
            ("4. Ship and track", "Consolidate, compare shipping lines, pay freight, then track to your door."),
        ],
        "hipobuy-qc-photos-checklist": [
            ("Universal checks", "Ask for extra angles if logos, seams, stains or shape look off."),
            ("Category focus", "Shoes: toebox and sole. Tees: print edges. Bags: hardware. Electronics: battery rules."),
            ("Mindset", "QC photos reduce risk; they do not eliminate it. The GL/RL decision stays with you."),
        ],
        "best-hipobuy-spreadsheet-approach-2026": [
            ("Match search intent", "People searching “hipobuy spreadsheet” want finds, not a sales pitch."),
            ("Give every find a URL", "Unique product HTML pages create long-tail rankings. Category hubs capture head terms."),
            ("Stay independent", "Disclose affiliates, remind buyers to verify listings, refresh the catalog."),
        ],
    }
    for slug, title, excerpt in GUIDES:
        sections = "".join(
            f"<h2>{esc(h)}</h2><p>{esc(b)}</p>" for h, b in bodies[slug]
        )
        write(
            ROOT / "guides" / f"{slug}.html",
            f"""{head(f'{title} | Findsheet', excerpt, f'/guides/{slug}.html', 1)}
{header(1)}
    <article class="wrap page-hero" style="max-width:46rem;margin-inline:auto">
      <a class="crumbs" href="index.html">All guides</a>
      <h1>{esc(title)}</h1>
      <p class="prose">{esc(excerpt)}</p>
      <div class="prose">{sections}</div>
      <p style="margin-top:2rem"><a class="btn btn-accent" href="../browse.html">Browse spreadsheet finds</a></p>
    </article>
{footer(1)}""",
        )


def page_agents():
    links = "".join(
        f'<a href="{slug}.html" style="display:block;border:1px solid var(--line);padding:1.25rem;background:var(--paper)"><h2 style="margin:0;font-family:Syne,sans-serif">{esc(name)}</h2><p style="margin:0.6rem 0 0;color:var(--muted);font-size:0.9rem">{esc(summary)}</p></a>'
        for slug, name, summary in AGENTS
    )
    write(
        ROOT / "agents" / "index.html",
        f"""{head('Shopping Agents | Findsheet', 'HipoBuySpreadsheet links work with major China shopping agents.', '/agents/index.html', 1)}
{header(1)}
    <div class="wrap page-hero"><h1>Compatible agents</h1><p class="prose">Same marketplace links, different checkout paths.</p></div>
    <div class="wrap section" style="padding-top:0.5rem;display:grid;gap:0.75rem;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">{links}</div>
{footer(1)}""",
    )
    for slug, name, summary in AGENTS:
        write(
            ROOT / "agents" / f"{slug}.html",
            f"""{head(f'{name} + HipoBuySpreadsheet Links | Findsheet', summary, f'/agents/{slug}.html', 1)}
{header(1)}
    <div class="wrap page-hero" style="max-width:46rem;margin-inline:auto">
      <a class="crumbs" href="index.html">All agents</a>
      <h1>{esc(name)}</h1>
      <p class="prose">{esc(summary)}</p>
      <p class="prose">Findsheet product links are marketplace URLs. Paste them into {esc(name)} after you verify the live listing. We are not affiliated with {esc(name)}.</p>
      <p style="margin-top:1.5rem"><a class="btn" href="../browse.html">Browse finds to paste</a></p>
    </div>
{footer(1)}""",
        )


def page_simple():
    write(
        ROOT / "how-to-buy.html",
        f"""{head('How to Buy from Hipobuy | Findsheet', 'Step-by-step: find a spreadsheet listing, paste into Hipobuy, review QC, ship.', '/how-to-buy.html')}
{header(0)}
    <div class="wrap page-hero" style="max-width:46rem;margin-inline:auto">
      <h1>How to buy</h1>
      <div class="prose">
        <h2>1. Find the item</h2>
        <p>Browse Findsheet categories or search. Verify the live Weidian / Taobao / 1688 listing.</p>
        <h2>2. Paste into your agent</h2>
        <p>Copy the source URL into Hipobuy (or CNFans, Kakobuy, Mulebuy, Sugargoo). Pay item cost.</p>
        <h2>3. Review warehouse QC</h2>
        <p>Inspect logos, shape, stitching and defects before you GL.</p>
        <h2>4. Ship internationally</h2>
        <p>Compare lines by weight and destination, pay freight, then track.</p>
      </div>
      <p style="margin-top:1.5rem"><a class="btn btn-accent" href="browse.html">Start browsing finds</a></p>
    </div>
{footer(0)}""",
    )
    write(
        ROOT / "about.html",
        f"""{head('About Findsheet', SITE['description'], '/about.html')}
{header(0)}
    <div class="wrap page-hero" style="max-width:46rem;margin-inline:auto">
      <h1>About</h1>
      <p class="prose">{esc(SITE['description'])}</p>
      <p class="prose">This site is plain HTML in the <code>html/</code> folder — edit any page directly. Built for long-term SEO with unique product and category pages.</p>
    </div>
{footer(0)}""",
    )


def page_robots_sitemap():
    write(
        ROOT / "robots.txt",
        f"""User-agent: *
Allow: /
Disallow: /js/

Sitemap: {SITE['url']}/sitemap.xml
""",
    )
    urls = ["/", "/browse.html", "/how-to-buy.html", "/about.html", "/guides/index.html", "/agents/index.html"]
    urls += [f"/c/{s}.html" for s, *_ in CATEGORIES]
    urls += [f"/p/{p['slug']}.html" for p in PRODUCTS]
    urls += [f"/guides/{s}.html" for s, *_ in GUIDES]
    urls += [f"/agents/{s}.html" for s, *_ in AGENTS]
    items = "\n".join(
        f"  <url><loc>{SITE['url']}{u if u != '/' else '/'}</loc><changefreq>weekly</changefreq></url>"
        if u != "/"
        else f"  <url><loc>{SITE['url']}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>"
        for u in urls
    )
    # fix homepage
    items = "\n".join(
        f"  <url><loc>{SITE['url']}{'' if u == '/' else u}</loc></url>" for u in urls
    )
    write(
        ROOT / "sitemap.xml",
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
""",
    )


def page_js():
    write(
        ROOT / "js" / "filter.js",
        """(function () {
  var params = new URLSearchParams(location.search);
  var q = (params.get("q") || "").trim().toLowerCase();
  var input = document.getElementById("filter");
  if (input && q) input.value = q;
  if (!q) return;
  document.querySelectorAll("#grid .product-card").forEach(function (card) {
    var text = card.textContent.toLowerCase();
    card.style.display = text.indexOf(q) >= 0 ? "" : "none";
  });
})();
""",
    )


def main():
    page_js()
    page_index()
    page_browse()
    page_categories()
    page_products()
    page_guides()
    page_agents()
    page_simple()
    page_robots_sitemap()
    print("done")


if __name__ == "__main__":
    main()
