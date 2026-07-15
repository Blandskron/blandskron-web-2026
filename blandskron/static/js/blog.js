(function () {
  "use strict";

  if (!document.querySelector(".blog-content")) return;

  var loadScript = function (source, onLoad) {
    var script = document.createElement("script");
    script.src = source;
    script.defer = true;
    script.onload = onLoad;
    document.body.appendChild(script);
  };

  loadScript("https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js", function () {
    loadScript("https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js", function () {
      if (typeof window.renderMathInElement === "function") {
        window.renderMathInElement(document.body, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false }
          ]
        });
      }
    });
  });
}());
