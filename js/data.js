window.KF = window.KF || {};

KF.site = {
  name: "HipoBuySpreadsheet",
  domain: "hipobuyqcsheets.com",
  origin: "",
  updated: "Sep 2026",
  discord: "https://discord.gg/7DRMaMAADv",
};

// Live Server may host this folder at /html/ or at /. Prefer the page URL.
KF.root = (function () {
  const p = location.pathname.replace(/\\/g, "/");
  const htmlIdx = p.indexOf("/html/");
  if (htmlIdx >= 0) return p.slice(0, htmlIdx + 6);
  try {
    const scripts = document.getElementsByTagName("script");
    for (let i = 0; i < scripts.length; i++) {
      const raw = scripts[i].getAttribute("src") || "";
      if (!raw || !/js\/(?:data|catalog|shop|filter)\.js(?:\?|$)/.test(raw)) continue;
      return new URL(raw, location.href).pathname.replace(/\/js\/[^/]+$/, "/");
    }
  } catch (e) {}
  return "/";
})();

// Product photos still hosted on the original image library CDN.
KF.cdn = "https://cdn.jsdelivr.net/gh/qjy0126/hipobuyspreadsheet@main/html/";

KF.asset = (path) => {
  const s = String(path || "");
  if (!s) return s;
  if (/^https?:\/\//i.test(s)) return s;
  const rel = s.replace(/^\.\//, "").replace(/^\//, "");
  // Product photos stay on GitHub CDN (too large for Cloudflare Workers assets).
  if (/^img\/products\//i.test(rel) && !/^(localhost|127\.0\.0\.1)$/i.test(location.hostname)) {
    return KF.cdn + rel;
  }
  return KF.root + rel;
};

KF.rewriteProductImages = function () {
  if (/^(localhost|127\.0\.0\.1)$/i.test(location.hostname)) return;
  const base = KF.cdn + "img/products/";
  document.querySelectorAll("img[src*='products/']").forEach((img) => {
    const src = img.getAttribute("src") || "";
    const m = src.match(/(\d+)\.webp/i);
    if (m) img.src = base + m[1] + ".webp";
  });
};

KF.slugify = (text) => String(text || "")
  .toLowerCase()
  .replace(/[^a-z0-9]+/g, "-")
  .replace(/^-+|-+$/g, "")
  .replace(/-+/g, "-")
  .slice(0, 60);

KF.itemSlug = (p) => {
  const id = String((p && p.id) || "").replace(/^p-/, "");
  const base = KF.slugify(p && p.title);
  return (base ? base + "-" : "") + id;
};
KF.itemPath = (p) => {
  const file = "item/" + KF.itemSlug(p) + "/index.html";
  const path = location.pathname.replace(/\\/g, "/");
  if (/\/(item|guides|agents|c)\//.test(path)) return KF.root + file;
  return file;
};
KF.catPath = (slug) => (slug ? "browse.html?cat=" + encodeURIComponent(slug) : "browse.html");
KF.findsPath = () => "browse.html";
KF.brandSlug = (name) => KF.slugify(name);

KF.nav = {
  apparel: [
    { slug: "shoes", label: "Shoes" },
    { slug: "t-shirts", label: "T-Shirts" },
    { slug: "hoodies", label: "Hoodies" },
    { slug: "jackets", label: "Jackets" },
    { slug: "pants", label: "Pants/Shorts" },
    { slug: "sets", label: "Sets" },
    { slug: "jersey", label: "Jersey" },
  ],
  lifestyle: [
    { slug: "headwear", label: "Headwear" },
    { slug: "watches", label: "Watches" },
    { slug: "accessories", label: "Accessories" },
    { slug: "other", label: "Other" },
  ],
};

KF.categories = [
  { slug: "shoes", label: "Shoes" },
  { slug: "t-shirts", label: "T-Shirts" },
  { slug: "hoodies", label: "Hoodies" },
  { slug: "jackets", label: "Jackets" },
  { slug: "pants", label: "Pants/Shorts" },
  { slug: "headwear", label: "Headwear" },
  { slug: "sets", label: "Sets" },
  { slug: "jersey", label: "Jersey" },
  { slug: "accessories", label: "Accessories" },
  { slug: "watches", label: "Watches" },
  { slug: "other", label: "Other" },
];

KF.products = KF.products || [];

KF.productCats = (p) => {
  const cats = [p.category].concat(p.categories || []).filter(Boolean);
  const seen = {};
  return cats.filter((c) => (seen[c] ? false : (seen[c] = true)));
};
KF.inCategory = (p, slug) => {
  if (!slug) return true;
  if (slug === "jeans" || slug === "shorts" || slug === "pants-shorts") {
    return KF.inCategory(p, "pants") || /jean|short/i.test(p.title || "");
  }
  if (slug === "jerseys") return KF.inCategory(p, "jersey");
  if (slug === "hats") return KF.inCategory(p, "headwear");
  if (slug === "belts" || slug === "jewelry" || slug === "bags") {
    return KF.inCategory(p, "accessories") || new RegExp(slug.replace(/s$/, ""), "i").test(p.title || "");
  }
  if (slug === "headphones" || slug === "electronics") {
    return /headphone|airpod|earbud|watch|tech/i.test(p.title || "") || p.category === "other";
  }
  return KF.productCats(p).includes(slug);
};

KF.money = (n) => `$${Number(n).toFixed(2)}`;
KF.invite = { hipobuy: "R71GHKM1I" };

KF.listing = (sourceUrl) => {
  const url = String(sourceUrl || "");
  const weidian = url.match(/itemID=(\d+)/i);
  if (weidian || /weidian\.com/i.test(url)) {
    const id = weidian ? weidian[1] : "";
    const raw = id ? `https://weidian.com/item.html?itemID=${id}` : url;
    return { id, channel: "weidian", platform: "WEIDIAN", source: "WD", path: "weidian", url: raw };
  }
  const tb = url.match(/[?&]id=(\d+)/i);
  if (/taobao\.com|tmall\.com/i.test(url)) {
    return { id: tb ? tb[1] : "", channel: "taobao", platform: "TAOBAO", source: "TB", path: "taobao", url };
  }
  const ali = url.match(/offer\/(\d+)/i);
  if (/1688\.com/i.test(url)) {
    return { id: ali ? ali[1] : "", channel: "1688", platform: "1688", source: "AL", path: "1688", url };
  }
  return { id: "", channel: "weidian", platform: "WEIDIAN", source: "WD", path: "weidian", url };
};

KF.agentUrl = (sourceUrl) => {
  const L = KF.listing(sourceUrl);
  const enc = encodeURIComponent(L.url);
  if (L.id) {
    return `https://hipobuy.com/product/${L.path}/${L.id}?source=SEARCH_LIST&keyword=${enc}&inviteCode=${KF.invite.hipobuy}`;
  }
  return L.url;
};
KF.kakobuyUrl = KF.agentUrl;

KF.itemName = (p) => String((p && p.title) || "").replace(/\s+/g, " ").trim().slice(0, 100);
KF.track = () => {};
KF.ui = KF.ui || {};

KF.mountDiscord = function () {
  // Disabled — floating Discord tab bloated without styles.css sizing.
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    KF.rewriteProductImages();
  });
} else {
  KF.rewriteProductImages();
}

(function loadPwa() {
  if (window.__kfPwa || document.querySelector('script[src*="js/pwa.js"]')) return;
  const s = document.createElement("script");
  s.src = KF.root + "js/pwa.js";
  document.head.appendChild(s);
})();
