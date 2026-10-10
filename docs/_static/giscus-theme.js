// Created by JXP and Claude.
// Keep the giscus comment box in step with the site's light/dark switch. The
// theme sets `data-theme` on <html>; giscus listens for a postMessage.
(function () {
  function giscusTheme() {
    var t = document.documentElement.getAttribute("data-theme");
    return t === "dark" ? "dark" : "light";
  }
  function push() {
    var frame = document.querySelector("iframe.giscus-frame");
    if (!frame) return;
    frame.contentWindow.postMessage(
      { giscus: { setConfig: { theme: giscusTheme() } } },
      "https://giscus.app"
    );
  }
  new MutationObserver(push).observe(document.documentElement, {
    attributes: true, attributeFilter: ["data-theme"],
  });
  window.addEventListener("message", function (ev) {
    if (ev.origin === "https://giscus.app") push();  // first load: sync once ready
  });
})();
