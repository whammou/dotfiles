// ==UserScript==
// @name        conditional-div-bg
// @description Paint divs with --od-bg0 only when the site gave them a
//              solid background; keep transparent, translucent, and
//              gradient-only divs see-through so they never cover content.
//              Reacts to stylesheet toggles: `xc` (config-cycle
//              content.user_stylesheets) and `toggle-tab-css` (Ctrl-r) both
//              rewrite qutebrowser's injected <style> in place via set_css(),
//              so painted divs are unpainted when the stylesheet is stripped
//              and repainted when it comes back.
// @run-at      document-start
// ==/UserScript==

(function () {
    'use strict';

    const ALPHA_THRESHOLD = 0.5;
    const SHADE_VARS = ['--od-bg0', '--od-bg1', '--od-bg2', '--od-bg3', '--od-bg_d'];

    // Theme availability: 'unknown' (stylesheet not injected yet), 'on'
    // (--od-bg0 resolvable), 'off' (stylesheet stripped or never present).
    let themeState = 'unknown';
    let bg0 = '';
    let shades = [];
    // Elements already evaluated: re-inserted subtrees are skipped wholesale.
    // An element's own background-color doesn't change when it moves, so
    // re-running getComputedStyle on it is pure waste. Reset on re-enable so
    // the whole document is re-evaluated under the restored theme.
    let visited = new WeakSet();
    // Divs this script painted; unpainted wholesale when the stylesheet goes
    // away, rebuilt from scratch when it returns.
    let paintedEls = new Set();
    // Divs seen before the theme became resolvable, flushed once it lands.
    const pending = new Set();
    // Added nodes are queued and processed once per animation frame, so
    // getComputedStyle work is coalesced instead of running per-mutation.
    const queue = [];
    let rafId = 0;
    // Set once a qutebrowser-style <style> element is seen, so an unresolvable
    // variable can be told apart from "stylesheet hasn't landed yet".
    let seenCandidateStyle = false;
    let recheckRaf = 0;
    // Diagnostics: read via `:jseval JSON.stringify(window.__cdb)`.
    const stats = { theme: 'unknown', bg0: '', painted: 0, seeThrough: 0, themed: 0, pending: 0 };
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

    // qutebrowser's stylesheet.js appends its <style> as a child of <html>
    // (watch_root) or of the document itself before <html> exists. Site
    // styles live in <head>, so a style whose parent is <html>/document is
    // ours — this is what set_css() rewrites in place on xc / Ctrl-r.
    function isCandidateStyle(node) {
        return node.nodeName === 'STYLE' &&
            (node.parentNode === document.documentElement ||
             node.parentNode === document);
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

    // Resolves --od-bg0 (and the shade family) exactly once per state change;
    // afterwards returns the cached value. Returns '' when the theme is not
    // resolvable, so callers know not to paint.
    function resolveTheme() {
        if (themeState === 'on' && bg0) {
            return bg0;
        }
        if (themeState === 'off') {
            return '';
        }
        // 'unknown': the stylesheet may not have been injected yet.
        if (!document.documentElement) {
            return '';
        }
        const cs = getComputedStyle(document.documentElement);
        const v = cs.getPropertyValue('--od-bg0').trim();
        if (!v) {
            return '';
        }
        bg0 = v;
        shades = SHADE_VARS.map(s => cssColorToRgb(cs.getPropertyValue(s)))
            .filter(Boolean);
        stats.bg0 = bg0;
        themeState = 'on';
        stats.theme = themeState;
        return bg0;
    }

    function setThemeOff() {
        if (themeState === 'off') {
            return;
        }
        themeState = 'off';
        stats.theme = themeState;
        for (const el of paintedEls) {
            el.style.removeProperty('background-color');
        }
        paintedEls.clear();
        pending.clear();
        stats.painted = 0;
        stats.pending = 0;
    }

    // Re-reads the theme after any stylesheet mutation. With the stylesheet
    // stripped, all script-painted divs are reverted to the site's own colors.
    // When it returns, the whole document is re-evaluated from scratch.
    function recheckTheme() {
        if (!document.documentElement) {
            return;
        }
        const cs = getComputedStyle(document.documentElement);
        const v = cs.getPropertyValue('--od-bg0').trim();
        if (v) {
            const prevBg0 = bg0;
            bg0 = v;
            shades = SHADE_VARS.map(s => cssColorToRgb(cs.getPropertyValue(s)))
                .filter(Boolean);
            stats.bg0 = bg0;
            if (themeState === 'on') {
                if (bg0 !== prevBg0) {  // config re-source changed the palette
                    for (const el of paintedEls) {
                        el.style.setProperty('background-color', bg0, 'important');
                    }
                }
                flushPending();
                return;
            }
            // off/unknown -> on: repaint everything under the restored theme.
            themeState = 'on';
            stats.theme = themeState;
            visited = new WeakSet();
            paintedEls = new Set();
            if (document.body) {
                paintTree(document.body);
            }
            flushPending();
            return;
        }
        // Vars unresolvable: if the theme <style> exists, it was emptied by
        // xc / Ctrl-r — go quiet. Otherwise the stylesheet simply hasn't
        // landed yet; stay 'unknown' (the 3s timer pins 'off' as a fallback).
        if (seenCandidateStyle) {
            setThemeOff();
        }
    }

    function scheduleRecheck() {
        if (recheckRaf) {
            return;
        }
        recheckRaf = requestAnimationFrame(() => {
            recheckRaf = 0;
            recheckTheme();
        });
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
        if (themeState === 'off') {
            return;  // stylesheet stripped: leave the site's own colors alone
        }
        if (visited.has(el)) {
            return;
        }
        if (!resolveTheme()) {
            // Stylesheet not injected yet: queue and paint once the theme
            // variables become resolvable. Bounded fail-safe.
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
        paintedEls.add(el);
        stats.painted = paintedEls.size;
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
        const batch = queue.splice(0, queue.length);
        for (const node of batch) {
            if (node.nodeType !== Node.ELEMENT_NODE) {
                continue;
            }
            if (node.nodeName === 'STYLE') {
                // A <style> child of <html> is qutebrowser's stylesheet;
                // set_css() rewrites its textContent in place, so rechecking
                // here (debounced) catches xc / Ctrl-r toggles.
                if (isCandidateStyle(node)) {
                    seenCandidateStyle = true;
                }
                scheduleRecheck();
                continue;
            }
            if (themeState !== 'off') {
                paintTree(node);
            }
        }
        // Late-arriving stylesheet: drain whatever got queued before it.
        if (pending.size) {
            scheduleRecheck();
        }
    }

    function schedule() {
        if (rafId) {
            return;
        }
        rafId = requestAnimationFrame(processBatch);
    }

    // Initial scan: stylesheet.js is registered before greasemonkey scripts,
    // so its <style> usually already exists when this script runs.
    if (document.documentElement) {
        for (const s of document.documentElement.querySelectorAll('style')) {
            if (isCandidateStyle(s)) {
                seenCandidateStyle = true;
                break;
            }
        }
    }
    scheduleRecheck();

    if (document.body) {
        paintTree(document.body);
    }
    flushPending();

    // If the stylesheet never shows up (e.g. stylesheets disabled globally),
    // pin 'off' so paint() stops probing getComputedStyle per element. Any
    // later stylesheet mutation flips the state back on.
    setTimeout(() => {
        if (themeState === 'unknown') {
            setThemeOff();
        }
    }, 3000);

    new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            // childList mutation whose target is a <style> child of <html>:
            // set_css() replaced its text node -> theme toggled.
            if (mutation.target.nodeName === 'STYLE' &&
                    isCandidateStyle(mutation.target)) {
                seenCandidateStyle = true;
                scheduleRecheck();
            }
            for (const node of mutation.addedNodes) {
                if (node.nodeType !== Node.ELEMENT_NODE) {
                    continue;
                }
                if (node.nodeName === 'STYLE') {
                    if (isCandidateStyle(node)) {
                        seenCandidateStyle = true;
                    }
                    queue.push(node);
                    continue;
                }
                queue.push(node);
            }
            for (const node of mutation.removedNodes) {
                if (node.nodeType === Node.ELEMENT_NODE &&
                        node.nodeName === 'STYLE' && isCandidateStyle(node)) {
                    scheduleRecheck();  // theme <style> torn down
                }
            }
        }
        if (queue.length) {
            schedule();
        }
    }).observe(document, {childList: true, subtree: true});
})();
