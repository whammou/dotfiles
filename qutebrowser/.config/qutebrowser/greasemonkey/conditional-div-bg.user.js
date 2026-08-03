// ==UserScript==
// @name        conditional-div-bg
// @description Paint divs with --od-bg0 only when the site gave them a
//              solid background; keep transparent, translucent, and
//              gradient-only divs see-through so they never cover content.
// @run-at      document-start
// ==/UserScript==

(function () {
    'use strict';

    const ALPHA_THRESHOLD = 0.5;
    const SHADE_VARS = ['--od-bg0', '--od-bg1', '--od-bg2', '--od-bg3', '--od-bg_d'];

    let bg0 = '';
    let shades = [];
    const pending = new Set();
    // Elements already evaluated: re-inserted subtrees are skipped wholesale.
    // An element's own background-color doesn't change when it moves, so
    // re-running getComputedStyle on it is pure waste.
    const visited = new WeakSet();
    // Added nodes are queued and processed once per animation frame, so
    // getComputedStyle work is coalesced instead of running per-mutation.
    const queue = [];
    let rafId = 0;
    let styleSeen = false;
    // Diagnostics: read via `:jseval JSON.stringify(window.__cdb)`.
    const stats = { bg0: '', painted: 0, seeThrough: 0, themed: 0, pending: 0 };
    window.__cdb = stats;

    // Diagnostic mode: appending `#cdb` to a URL shows live stats in the tab
    // title, bypassing :jseval (statusbar hidden, jseval runs in another
    // world). The interval fights pages that overwrite the title.
    if (location.hash === '#cdb') {
        const showStats = () => {
            document.title = 'CDB ' + JSON.stringify(stats);
        };
        showStats();
        setInterval(showStats, 1000);
    }

    function cssColorToRgb(value) {
        const v = value.trim();
        if (!v.startsWith('#')) {
            return v;
        }
        const hex = v.length === 4
            ? v.slice(1).split('').map(c => c + c).join('')
            : v.slice(1);
        const n = parseInt(hex, 16);
        return Number.isNaN(n) ? v
            : `rgb(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255})`;
    }

    function resolveTheme() {
        if (bg0 || !document.documentElement) {
            return bg0;
        }
        const cs = getComputedStyle(document.documentElement);
        bg0 = cs.getPropertyValue('--od-bg0').trim();
        shades = SHADE_VARS.map(v => cssColorToRgb(cs.getPropertyValue(v)))
            .filter(Boolean);
        stats.bg0 = bg0;
        return bg0;
    }

    function alphaOf(bg) {
        if (bg === 'transparent' || bg === 'rgba(0, 0, 0, 0)') {
            return 0;
        }
        const m = bg.match(/rgba?\(([^)]+)\)/);
        if (!m) {
            return 1;
        }
        const parts = m[1].split(',').map(s => parseFloat(s.trim()));
        return parts.length === 4 ? parts[3] : 1;
    }

    function isGradient(image) {
        return image !== 'none' && !image.startsWith('url(');
    }

    function paint(el) {
        if (visited.has(el)) {
            return;
        }
        if (!resolveTheme()) {
            // Stylesheet not injected yet (or toggled off): queue and paint
            // once the theme variables become resolvable. Bounded fail-safe.
            if (pending.size < 2000) {
                pending.add(el);
                stats.pending = pending.size;
            }
            return;
        }
        const cs = getComputedStyle(el);
        const bg = cs.backgroundColor;
        visited.add(el);
        if (shades.includes(bg)) {
            stats.themed++;  // already painted by the theme stylesheet
            return;
        }
        if (alphaOf(bg) < ALPHA_THRESHOLD &&
                (cs.backgroundImage === 'none' || isGradient(cs.backgroundImage))) {
            stats.seeThrough++;  // transparent/translucent or decorative
            return;
        }
        el.style.setProperty('background-color', bg0, 'important');
        stats.painted++;
    }

    function paintTree(node) {
        if (node.nodeType !== Node.ELEMENT_NODE) {
            return;
        }
        if (visited.has(node)) {
            return;  // whole subtree already decided
        }
        if (node.matches('div')) {
            paint(node);
        }
        node.querySelectorAll('div').forEach(paint);
    }

    function flushPending() {
        // Iterate only when the vars are resolvable: walking a full pending
        // set with unresolved vars is pure getComputedStyle waste.
        if (!resolveTheme() || pending.size === 0) {
            return;
        }
        for (const el of pending) {
            paint(el);
        }
        pending.clear();
        stats.pending = 0;
    }

    function processBatch() {
        rafId = 0;
        if (pending.size && styleSeen) {
            flushPending();  // qutebrowser's <style> landed -> vars resolvable
            styleSeen = false;
        }
        const batch = queue.splice(0, queue.length);
        for (const node of batch) {
            if (node.nodeType !== Node.ELEMENT_NODE) {
                continue;
            }
            if (node.nodeName === 'STYLE') {
                styleSeen = true;
                continue;
            }
            paintTree(node);
        }
        // Late-arriving stylesheet: drain whatever got queued before it.
        if (pending.size && styleSeen) {
            flushPending();
            styleSeen = false;
        }
    }

    function schedule() {
        if (rafId) {
            return;
        }
        rafId = requestAnimationFrame(processBatch);
    }

    if (document.body) {
        paintTree(document.body);
    }
    flushPending();

    new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            for (const node of mutation.addedNodes) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    queue.push(node);
                }
            }
        }
        if (queue.length) {
            schedule();
        }
    }).observe(document, {childList: true, subtree: true});
})();
