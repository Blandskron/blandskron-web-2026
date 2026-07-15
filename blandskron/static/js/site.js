// Shared site interactions. Kept outside templates so every page uses one source of truth.
(function () {
  "use strict";

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-scroll]");
    if (!button) return;

    var target = document.getElementById(button.getAttribute("data-scroll"));
    if (!target) return;

    var mobileMenu = document.getElementById("mobileMenu");
    var mobileButton = document.getElementById("mobileMenuBtn");
    if (mobileMenu && mobileButton && !mobileMenu.classList.contains("hidden")) {
      mobileMenu.classList.add("hidden");
      mobileButton.setAttribute("aria-expanded", "false");
    }

    target.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  var mobileButton = document.getElementById("mobileMenuBtn");
  var mobileMenu = document.getElementById("mobileMenu");
  if (mobileButton && mobileMenu) {
    mobileButton.addEventListener("click", function () {
      var isHidden = mobileMenu.classList.contains("hidden");
      mobileMenu.classList.toggle("hidden");
      mobileButton.setAttribute("aria-expanded", String(isHidden));
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth >= 768) {
        mobileMenu.classList.add("hidden");
        mobileButton.setAttribute("aria-expanded", "false");
      }
    });
  }

  var flashWrap = document.getElementById("flashWrap");
  if (flashWrap) {
    var flashItems = flashWrap.querySelectorAll(".flash-item");
    if (flashItems.length) {
      window.setTimeout(function () {
        flashItems.forEach(function (item) {
          item.style.opacity = "0";
          item.style.transform = "translateY(-6px)";
        });
        window.setTimeout(function () { flashWrap.remove(); }, 600);
      }, 5000);
    }
  }

  var revealElements = document.querySelectorAll(".fade-up");
  if (revealElements.length) {
    var reveal = function (element) { element.classList.add("is-visible"); };
    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (reducedMotion || !("IntersectionObserver" in window)) {
      revealElements.forEach(reveal);
    } else {
      var observer = new IntersectionObserver(function (entries, currentObserver) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          reveal(entry.target);
          currentObserver.unobserve(entry.target);
        });
      }, {
        // Tall articles can never reach a 12% intersection ratio. Any visible
        // portion is enough to activate the optional transform enhancement.
        threshold: 0,
        rootMargin: "0px 0px -36px 0px"
      });
      revealElements.forEach(function (element) { observer.observe(element); });

      // Keep the page usable if an observer callback is delayed by hydration,
      // syntax highlighting, math rendering, or a browser-specific issue.
      window.setTimeout(function () {
        revealElements.forEach(reveal);
      }, 1500);
    }
  }
}());
