(function () {
  "use strict";

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag("js", new Date());
  window.gtag("config", "G-XS616SHMD7");
  window.gtag("config", "G-0HTRJHD9N0");

  var analyticsScript = document.createElement("script");
  analyticsScript.async = true;
  analyticsScript.src = "https://www.googletagmanager.com/gtag/js?id=G-XS616SHMD7";
  document.head.appendChild(analyticsScript);

  (function (windowObject, documentObject, methodName, elementName, id) {
    windowObject[methodName] = windowObject[methodName] || function () {
      (windowObject[methodName].q = windowObject[methodName].q || []).push(arguments);
    };
    var script = documentObject.createElement(elementName);
    script.async = true;
    script.src = "https://www.clarity.ms/tag/" + id;
    var firstScript = documentObject.getElementsByTagName(elementName)[0];
    firstScript.parentNode.insertBefore(script, firstScript);
  }(window, document, "clarity", "script", "u59txxo2oo"));
}());
