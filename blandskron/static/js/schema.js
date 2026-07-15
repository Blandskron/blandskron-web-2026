(function () {
  "use strict";
  var graph = [
    {"@type": "Organization", "name": "Blandskron SpA", "url": "https://www.blandskron.com/", "areaServed": ["CL", "LATAM"]},
    {"@type": "ProfessionalService", "name": "Blandskron", "url": "https://www.blandskron.com/", "serviceType": ["Desarrollo de software", "Inteligencia artificial", "Automatización", "Ciberseguridad"]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "¿Qué hace Blandskron?", "acceptedAnswer": {"@type": "Answer", "text": "Blandskron diseña, integra y protege software, automatización e inteligencia artificial."}}, {"@type": "Question", "name": "¿Dónde opera Blandskron?", "acceptedAnswer": {"@type": "Answer", "text": "Blandskron opera en Chile y Latinoamérica."}}]}
  ];
  var element = document.createElement("script");
  element.type = "application/ld+json";
  element.textContent = JSON.stringify({"@context": "https://schema.org", "@graph": graph});
  document.head.appendChild(element);
}());
