// ==UserScript==
// @name         Remove target="_blank"
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  Remove target="_blank" from links to prevent opening in new tabs
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    let rafId = 0;

    function removeTargetBlank() {
        var links = document.querySelectorAll('a[target="_blank"]');
        for (var i = 0; i < links.length; i++) {
            links[i].removeAttribute('target');
        }
    }

    // Debounce: coalesce bursts of DOM mutations into at most one document
    // scan per animation frame instead of one querySelectorAll per mutation.
    function schedule() {
        if (rafId) {
            return;
        }
        rafId = requestAnimationFrame(function () {
            rafId = 0;
            removeTargetBlank();
        });
    }

    // Run immediately
    removeTargetBlank();

    // Run on DOM mutations (for dynamically loaded content)
    var observer = new MutationObserver(schedule);
    if (document.body) {
        observer.observe(document.body, {childList: true, subtree: true});
    } else {
        document.addEventListener('DOMContentLoaded', function () {
            observer.observe(document.body, {childList: true, subtree: true});
        });
    }
})();
