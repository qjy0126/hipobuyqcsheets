(function () {
  const params = new URLSearchParams(location.search);
  const $ = (sel) => document.querySelector(sel);
  const fill = (id, html) => {
    const el = document.getElementById(id);
    if (el) el.innerHTML = html;
  };

  function stars(rating) {
    const n = Math.max(0, Math.min(5, Number(rating) || 0));
    const full = Math.floor(n + 1e-9);
    return `<span class="stars">${"★".repeat(full)}${"☆".repeat(5 - full)}</span>`;
  }

  function productCard(p) {
    return `
      <a class="product-card" href="${KF.itemPath(p)}" data-id="${p.id}">
        <div class="thumb"><img src="${KF.asset(p.image)}" alt="${escapeHtml(p.title)}" loading="lazy" decoding="async" /></div>
        <h3>${escapeHtml(p.title)}</h3>
        ${stars(p.rating)}
        <b>${KF.money(p.price)}</b>
      </a>`;
  }
  KF.ui.productCard = productCard;
  KF.ui.stars = stars;

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (ch) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[ch]));
  }

  function catLabel(slug) {
    return (
      KF.categories.find((c) => c.slug === slug) ||
      KF.nav.apparel.find((c) => c.slug === slug) ||
      KF.nav.lifestyle.find((c) => c.slug === slug) ||
      { label: slug || "All finds" }
    ).label;
  }

  function pagerHtml(page, pages, extra) {
    if (pages <= 1) return "";
    function href(n) {
      const next = new URL(location.href);
      extra.forEach(([k, v]) => {
        if (v) next.searchParams.set(k, v);
        else next.searchParams.delete(k);
      });
      if (n > 1) next.searchParams.set("page", String(n));
      else next.searchParams.delete("page");
      return next.pathname.split("/").pop() + next.search;
    }
    const parts = [];
    const from = Math.max(1, page - 2);
    const to = Math.min(pages, page + 2);
    if (page > 1) parts.push(`<a href="${href(page - 1)}">Prev</a>`);
    for (let n = from; n <= to; n++) {
      parts.push(n === page ? `<span class="is-on">${n}</span>` : `<a href="${href(n)}">${n}</a>`);
    }
    if (page < pages) parts.push(`<a href="${href(page + 1)}">Next</a>`);
    return parts.join("");
  }

  function renderShop() {
    const cat = document.body.dataset.cat || params.get("cat") || "";
    const q = (params.get("q") || "").toLowerCase();
    const qcOnly = params.get("qc") === "1";
    const sort = params.get("sort") || "latest";
    const pageSize = 48;
    const page = Math.max(1, parseInt(params.get("page") || "1", 10) || 1);
    let list = KF.products.slice();
    if (cat) list = list.filter((p) => KF.inCategory(p, cat));
    if (q) {
      const digits = q.replace(/\D/g, "");
      list = list.filter((p) => {
        const id = String(p.id || "").replace(/^p-/, "");
        if (digits.length >= 4 && id.includes(digits)) return true;
        return `${p.title} ${p.collection} ${id} ${KF.productCats(p).join(" ")}`.toLowerCase().includes(q);
      });
    }
    if (qcOnly) list = list.filter((p) => p.qc);
    if (sort === "price-asc") list.sort((a, b) => a.price - b.price);
    if (sort === "price-desc") list.sort((a, b) => b.price - a.price);
    if (sort === "rating" || sort === "popular") list.sort((a, b) => b.rating - a.rating);

    const title = catLabel(cat) || (q ? `Search: ${params.get("q")}` : "All finds");
    const h1 = document.querySelector(".catalog-intro h1");
    if (h1) h1.textContent = q ? `Search “${params.get("q")}”` : (cat ? title : "All HipoBuySpreadsheet finds");
    document.title = `${title} — HipoBuySpreadsheet`;

    const total = list.length;
    const pages = Math.max(1, Math.ceil(total / pageSize));
    const safePage = Math.min(page, pages);
    const start = (safePage - 1) * pageSize;
    const slice = list.slice(start, start + pageSize);
    fill("shop-count", total ? `Showing ${start + 1}–${start + slice.length} of ${total} results` : "No products found");
    fill("product-grid", slice.map(productCard).join("") || "<p>No finds in this filter.</p>");
    fill("pager", pagerHtml(safePage, pages, [
      ["cat", cat],
      ["q", params.get("q")],
      ["sort", sort === "latest" ? "" : sort],
      ["qc", qcOnly ? "1" : ""],
    ]));

    const sortBox = $("#sort");
    if (sortBox) {
      sortBox.value = sort;
      sortBox.addEventListener("change", () => {
        const next = new URL(location.href);
        if (sortBox.value !== "latest") next.searchParams.set("sort", sortBox.value);
        else next.searchParams.delete("sort");
        next.searchParams.delete("page");
        location.href = next.pathname.split("/").pop() + next.search;
      });
    }

    const qInput = $("#shop-q");
    if (qInput && params.get("q")) qInput.value = params.get("q");
  }

  function renderItem() {
    const wanted = params.get("id");
    const item = KF.products.find((p) => p.id === wanted);
    if (!item) {
      location.replace(KF.findsPath());
      return;
    }
    document.title = `${item.title} — HipoBuySpreadsheet`;
    $("#item-title").textContent = item.title;
    $("#item-price").textContent = KF.money(item.price);
    $("#item-rating").innerHTML = `${stars(item.rating)} ${item.qc ? "QC photos on this find" : "No QC flag yet"} · ${item.source}`;
    $("#item-main").src = KF.asset(item.image);
    $("#item-main").alt = item.title;
    const buy = $("#buy-link");
    if (buy) {
      buy.href = KF.agentUrl(item.sourceUrl);
      buy.textContent = "Buy on Hipobuy";
    }
    const note = $("#item-note");
    if (note) {
      note.textContent = `${item.title} on the HipoBuySpreadsheet. ${catLabel(item.category)} find from ${item.source}, listed at ${KF.money(item.price)}. Preview here, then open Hipobuy to order.`;
    }
    fill("crumbs", `
      <a href="index.html">Home</a><span>/</span>
      <a href="browse.html">Shop</a><span>/</span>
      <a href="${KF.catPath(item.category)}">${escapeHtml(catLabel(item.category))}</a><span>/</span>
      <span>${escapeHtml(item.title)}</span>
    `);
    const related = KF.products.filter((p) => p.category === item.category && p.id !== item.id).slice(0, 12);
    fill("related-grid", related.map(productCard).join(""));
  }

  const page = document.body.dataset.page;
  if (page === "shop") renderShop();
  if (page === "item") renderItem();
})();
