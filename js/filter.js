(function () {
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
