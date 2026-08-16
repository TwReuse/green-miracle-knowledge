(function () {
  "use strict";

  var documents = [];
  var minSearchLength = 1;

  function joinUrl(base, path) {
    if (path.substring(0, 1) === "/") return path;
    if (base.substring(base.length - 1) === "/") return base + path;
    return base + "/" + path;
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function normalize(value) {
    return String(value || "").normalize("NFKC").toLocaleLowerCase("zh-TW");
  }

  function queryTerms(query) {
    return normalize(query).split(/\s+/).filter(Boolean);
  }

  function getSearchTermFromLocation() {
    return new URLSearchParams(window.location.search).get("q") || "";
  }

  function summarize(text, terms) {
    var source = String(text || "").replace(/\s+/g, " ").trim();
    var normalized = normalize(source);
    var firstMatch = terms.reduce(function (found, term) {
      var index = normalized.indexOf(term);
      return index >= 0 && (found < 0 || index < found) ? index : found;
    }, -1);
    var start = Math.max(0, firstMatch - 45);
    var summary = source.substring(start, start + 180);
    return (start > 0 ? "…" : "") + summary + (start + 180 < source.length ? "…" : "");
  }

  function search(query) {
    var terms = queryTerms(query);
    if (!terms.length) return [];

    return documents.map(function (document) {
      var title = normalize(document.title);
      var text = normalize(document.text);
      if (!terms.every(function (term) { return title.includes(term) || text.includes(term); })) return null;

      var score = terms.reduce(function (total, term) {
        return total + (title.includes(term) ? 4 : 0) + (text.includes(term) ? 1 : 0);
      }, 0);

      return {
        location: document.location,
        title: document.title,
        summary: summarize(document.text, terms),
        score: score
      };
    }).filter(Boolean).sort(function (left, right) {
      return right.score - left.score || left.title.localeCompare(right.title, "zh-TW");
    }).slice(0, 20);
  }

  function displayResults(results) {
    var container = document.getElementById("mkdocs-search-results");
    if (!container) return;
    container.replaceChildren();

    if (!results.length) {
      var empty = document.createElement("p");
      empty.textContent = container.getAttribute("data-no-results-text") || "找不到符合的內容";
      container.appendChild(empty);
      return;
    }

    results.forEach(function (result) {
      container.insertAdjacentHTML(
        "beforeend",
        '<article><h3><a href="' + escapeHtml(joinUrl(base_url, result.location)) + '">' +
        escapeHtml(result.title) + "</a></h3><p>" + escapeHtml(result.summary) + "</p></article>"
      );
    });
  }

  function runSearch() {
    var input = document.getElementById("mkdocs-search-query");
    if (!input) return;
    var query = input.value.trim();
    displayResults(query.length >= minSearchLength ? search(query) : []);
  }

  function initializeSearch(data) {
    documents = Array.isArray(data.docs) ? data.docs : [];
    minSearchLength = Math.max(1, Number(data.config && data.config.min_search_length) || 1);

    var input = document.getElementById("mkdocs-search-query");
    if (!input) return;
    input.addEventListener("input", runSearch);

    var initialQuery = getSearchTermFromLocation();
    if (initialQuery) {
      input.value = initialQuery;
      runSearch();
    }
  }

  fetch(joinUrl(base_url, "search/search_index.json"))
    .then(function (response) {
      if (!response.ok) throw new Error("搜尋索引載入失敗");
      return response.json();
    })
    .then(initializeSearch)
    .catch(function (error) {
      console.error(error);
      displayResults([]);
    });
}());
