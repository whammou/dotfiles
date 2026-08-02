// ==UserScript==
// @name         Remove target="_blank"
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Remove target="_blank" from links to prevent opening in new tabs
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function removeTargetBlank() {
        var links = document.querySelectorAll('a[target="_blank"]');
        for (var i = 0; i < links.length; i++) {
            links[i].removeAttribute('target');
        }
    }

    // Run immediately
    removeTargetBlank();

    // Run on DOM mutations (for dynamically loaded content)
    var observer = new MutationObserver(removeTargetBlank);
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
})();