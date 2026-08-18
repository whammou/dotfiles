// ==UserScript==
// @name        visited-links-tmp
// @description TEMPORARY FIX (see qutebrowser/qutebrowser#8921): QtWebEngine
//              6.11 (qutebrowser 3.7.x) no longer applies the `:visited`
//              state, so CSS cannot distinguish visited links at all. This
//              script recolors links the user actually clicked this session
//              (stored per-origin in sessionStorage), surfacing them in
//              --od-purple instead of --od-blue. Works with `xc` stylesheet
//              toggles (inline !important beats the injected author sheet).
//              Session-scoped only: history from before qutebrowser started,
//              and clicks made on other origins, are not recalled. REMOVE
//              when the engine regression (#8921) is fixed upstream.
//              Handles SERP redirect links (google.com/url?q=...) whose hrefs
//              are re-rendered with fresh tracking params, and middle-click
//              (auxclick) open-in-new-tab.
// @run-at      document-end
// ==/UserScript==

(function () {
    'use strict';

    // --od-purple from css/00-variables.css, hardcoded because qutebrowser's
    // injected stylesheet may be toggled off (`xc`) and GM scripts cannot
    // reliably read the variable through the GM wrapper.
    const VISITED_COLOR = '#456E92';
    const STORAGE_KEY = 'qb_visited_links_tmp';
    const VISITED_ATTR = 'data-qb-visited-tmp';
    const STYLE_RULE = 'a[' + VISITED_ATTR + '] { color: ' + VISITED_COLOR + ' !important; }';

    // sessionStorage is per-origin: only links clicked from this origin can
    // be restyled on a later visit to the same origin. Back-navigation and
    // tab restores within the session are covered; cross-origin history is
    // not (browser privacy prevents querying it from JS).
    let stored = [];
    try {
        stored = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '[]');
    } catch (e) {
        stored = [];
    }
    const visited = new Set(stored);

    // Diagnostics: read via `:jseval JSON.stringify(window.__vltmp)`.
    const stats = { clicks: 0, recolored: 0, stored: visited.size };
    window.__vltmp = stats;

    let styleEl = null;

    function ensureStyle() {
        if (styleEl && styleEl.isConnected) {
            return;
        }
        styleEl = document.createElement('style');
        styleEl.textContent = STYLE_RULE;
        document.documentElement.appendChild(styleEl);
    }

    // SERP redirect links are re-rendered with fresh tracking params on every
    // search (google.com/url?q=<target>&ved=...&usg=...), so raw href strings
    // never match across renders. The canonical form is the redirect target
    // itself (the q= param); for ordinary links it is the href minus any
    // #fragment.
    function canonicalHref(href) {
        let url;
        try {
            url = new URL(href);
        } catch (e) {
            return href;
        }
        if (url.pathname === '/url' && url.searchParams.has('q')) {
            const target = url.searchParams.get('q');
            try {
                return new URL(target, url.origin).href;
            } catch (e) {
                return target;
            }
        }
        url.hash = '';
        return url.href;
    }

    function markVisited(link) {
        const canonical = canonicalHref(link.href);
        if (!visited.has(canonical)) {
            visited.add(canonical);
            stats.stored = visited.size;
            try {
                sessionStorage.setItem(STORAGE_KEY, JSON.stringify([...visited]));
            } catch (e) {
                // Storage unavailable (private mode/quota): session-local only.
            }
        }
        link.setAttribute(VISITED_ATTR, '1');
        stats.clicks += 1;
    }

    function recolor(link) {
        if (visited.has(canonicalHref(link.href))) {
            link.setAttribute(VISITED_ATTR, '1');
            stats.recolored += 1;
        }
    }

    function sweep(root) {
        ensureStyle();
        if (visited.size === 0) {
            return;
        }
        for (const link of root.querySelectorAll('a[href]')) {
            recolor(link);
        }
    }

    // Capture phase: catches clicks on link children too, and fires before
    // navigation can unload the document. `auxclick` covers middle-click
    // (open-in-new-tab), which does not produce a `click` event; Enter on a
    // focused link dispatches a `click` in Chromium, so keyboard is covered.
    function onActivate(event) {
        if (event.type === 'auxclick' && event.button !== 1) {
            return;
        }
        const target = event.target;
        if (!(target instanceof Element)) {
            return;
        }
        const link = target.closest('a[href]');
        if (link) {
            markVisited(link);
        }
    }
    document.addEventListener('click', onActivate, true);
    document.addEventListener('auxclick', onActivate, true);

    // Initial pass plus incremental sweeps over added subtrees only, so SPA
    // navigation and infinite feeds do not force full-document rescans.
    sweep(document);
    const observer = new MutationObserver((records) => {
        for (const record of records) {
            for (const node of record.addedNodes) {
                if (node.nodeType !== Node.ELEMENT_NODE) {
                    continue;
                }
                if (node.matches('a[href]')) {
                    recolor(node);
                }
                sweep(node);
            }
        }
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
})();
