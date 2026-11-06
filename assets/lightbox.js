// 画面写真(.shot img)をクリックすると、その場で大きく表示する簡易ライトボックス
document.addEventListener("click", function (e) {
  var img = e.target.closest(".shot img");
  if (!img) return;

  var overlay = document.createElement("div");
  overlay.className = "lightbox-overlay";

  var big = document.createElement("img");
  big.src = img.currentSrc || img.src;
  big.alt = img.alt;

  var closeBtn = document.createElement("button");
  closeBtn.type = "button";
  closeBtn.className = "lightbox-close";
  closeBtn.setAttribute("aria-label", "閉じる");
  closeBtn.textContent = "×";

  overlay.appendChild(big);
  overlay.appendChild(closeBtn);
  document.body.appendChild(overlay);
  document.body.style.overflow = "hidden";

  function close() {
    overlay.remove();
    document.body.style.overflow = "";
    document.removeEventListener("keydown", onKey);
  }
  function onKey(ev) {
    if (ev.key === "Escape") close();
  }

  overlay.addEventListener("click", function (ev) {
    if (ev.target === overlay) close();
  });
  closeBtn.addEventListener("click", close);
  document.addEventListener("keydown", onKey);
});
