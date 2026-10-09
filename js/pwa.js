(function () {
  if (window.__kfPwa) return;
  window.__kfPwa = true;

  const path = location.pathname.replace(/\\/g, "/");
  const htmlIdx = path.indexOf("/html/");
  const root =
    (window.KF && KF.root) ||
    (htmlIdx >= 0 ? path.slice(0, htmlIdx + 6) : "/");

  const standalone = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone;
  const ios = /iphone|ipad|ipod/i.test(navigator.userAgent);

  function ensureHead() {
    if (!document.querySelector('link[rel="manifest"]')) {
      const link = document.createElement("link");
      link.rel = "manifest";
      link.href = root + "manifest.webmanifest";
      document.head.appendChild(link);
    }
    if (!document.querySelector('meta[name="theme-color"]')) {
      const meta = document.createElement("meta");
      meta.name = "theme-color";
      meta.content = "#16324f";
      document.head.appendChild(meta);
    }
    if (!document.querySelector('link[rel="apple-touch-icon"]')) {
      const icon = document.createElement("link");
      icon.rel = "apple-touch-icon";
      icon.href = root + "img/apple-touch-icon.png";
      document.head.appendChild(icon);
    }
    document.documentElement.setAttribute("data-kf-pwa", "1");
  }

  const btnSvg =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M11 3h2v10.17l3.59-3.58L18 11l-6 6-6-6 1.41-1.41L11 13.17V3zm-7 16h16v2H4z"/></svg>';

  function mountButton() {
    if (standalone) return;
    let btn = document.querySelector(".pwa-install");
    if (!btn) {
      btn = document.createElement("button");
      btn.type = "button";
      btn.className = "pwa-install";
      btn.setAttribute("aria-label", "Add to desktop");
      btn.innerHTML = btnSvg + "<span>Add to desktop</span>";
      const nav = document.querySelector(".topbar-row .nav") || document.querySelector(".nav");
      const row = document.querySelector(".topbar-row");
      if (nav && nav.parentNode) nav.insertAdjacentElement("afterend", btn);
      else if (row) row.appendChild(btn);
      else document.body.appendChild(btn);
    }
    return btn;
  }

  let deferred = null;

  function showTip(html) {
    let tip = document.querySelector(".pwa-tip");
    if (!tip) {
      tip = document.createElement("div");
      tip.className = "pwa-tip";
      tip.innerHTML =
        '<div class="pwa-tip-card"><button class="pwa-tip-close" type="button" aria-label="Close">×</button><div class="pwa-tip-body"></div></div>';
      document.body.appendChild(tip);
      tip.addEventListener("click", (e) => {
        if (e.target === tip || e.target.closest(".pwa-tip-close")) tip.hidden = true;
      });
    }
    tip.querySelector(".pwa-tip-body").innerHTML = html;
    tip.hidden = false;
  }

  function onInstallClick() {
    if (deferred) {
      const ev = deferred;
      deferred = null;
      ev.prompt();
      return;
    }
    if (ios) {
      showTip(
        "<h3>Add to Home Screen</h3><p>Tap the Share button in Safari, then choose <b>Add to Home Screen</b>.</p>"
      );
      return;
    }
    showTip(
      "<h3>Add to desktop</h3><p>Open the browser menu and choose <b>Install app</b> or <b>Add to desktop</b>. Chrome also shows an install icon in the address bar.</p>"
    );
  }

  function boot() {
    ensureHead();
    const btn = mountButton();
    if (btn) btn.addEventListener("click", onInstallClick);

    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register(root + "sw.js").catch(() => {});
    }

    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      deferred = e;
    });

    window.addEventListener("appinstalled", () => {
      deferred = null;
      const b = document.querySelector(".pwa-install");
      if (b) b.hidden = true;
    });

    if (!document.querySelector('script[data-kf-firebase]')) {
      const fs = document.createElement("script");
      fs.type = "module";
      fs.dataset.kfFirebase = "1";
      fs.src = root + "js/firebase-analytics.js";
      document.head.appendChild(fs);
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
