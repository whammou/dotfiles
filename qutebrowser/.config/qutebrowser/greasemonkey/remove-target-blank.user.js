// ==UserScript==
// @name         Remove target="_blank"
// @namespace    http://tampermonkey.net/
// @version      1.3
// @description  Remove target="_blank" from links to prevent opening in new tabs
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Only added subtrees are scanned, not the whole document: scanning
    // document.querySelectorAll('a[target="_blank"]') once per animation
    // frame is O(entire DOM) and stalls Meet-class pages that churn
    // constantly. Work is also capped per frame like conditional-div-bg.
    const MAX_NODES_PER_FRAME = 128;
    // FIFO queue with a head index: the array is compacted once per frame,
    // so enqueue and dequeue are both amortized O(1) and the oldest nodes
    // are never starved by a continuous stream of new ones.
    const pending = [];
    let head = 0;
    // Nodes whose subtree scan is still queued: a node is skipped when any
    // ancestor is already queued, because that ancestor's scan will cover it
    // (an SPA burst adds a container and its children as separate records).
    const queued = new Set();
    let rafId = 0;

    function removeTargetBlankFrom(node) {
        var links = node.querySelectorAll('a[target="_blank"]');
        for (var i = 0; i < links.length; i++) {
            links[i].removeAttribute('target');
        }
    }

    function queueNode(node) {
        if (node.nodeType !== Node.ELEMENT_NODE ||
                node.nodeName === 'SCRIPT' || node.nodeName === 'STYLE') {
            return;
        }
        // Skip subtrees already covered by a queued ancestor scan.
        for (let p = node.parentNode; p; p = p.parentNode) {
            if (queued.has(p)) {
                return;
            }
        }
        if (!queued.has(node)) {
            queued.add(node);
            pending.push(node);
        }
    }

    function process() {
        rafId = 0;
        var processed = 0;
        while (head < pending.length && processed < MAX_NODES_PER_FRAME) {
            const node = pending[head++];
            queued.delete(node);
            if (node.nodeType !== Node.ELEMENT_NODE) {
                processed++;
                continue;
            }
            // Dropped when a queued ancestor will scan this subtree anyway
            // (the ancestor was queued after this node in the same burst).
            let covered = false;
            for (let p = node.parentNode; p; p = p.parentNode) {
                if (queued.has(p)) {
                    covered = true;
                    break;
                }
            }
            if (!covered) {
                if (node.matches('a[target="_blank"]')) {
                    node.removeAttribute('target');
                }
                removeTargetBlankFrom(node);
            }
            processed++;
        }
        if (head > 0) {
            pending.splice(0, head);
            head = 0;
        }
        if (pending.length) {
            schedule();
        }
    }

    // Debounce: coalesce bursts of DOM mutations into at most one scan per
    // animation frame instead of one scan per mutation.
    function schedule() {
        if (rafId) {
            return;
        }
        rafId = requestAnimationFrame(process);
    }

    // Run immediately: scan the initial document.
    removeTargetBlankFrom(document);

    // Run on DOM mutations (for dynamically loaded content)
    var observer = new MutationObserver(function (mutations) {
        for (var i = 0; i < mutations.length; i++) {
            var mutation = mutations[i];
            if (mutation.type === 'attributes') {
                // Sites set link.target dynamically; the attribute observer
                // fires only for 'target' changes, so this is near-free.
                queueNode(mutation.target);
                continue;
            }
            var added = mutation.addedNodes;
            for (var j = 0; j < added.length; j++) {
                queueNode(added[j]);
            }
        }
        if (pending.length) {
            schedule();
        }
    });
    if (document.body) {
        observer.observe(document.body, {childList: true, subtree: true, attributes: true, attributeFilter: ['target']});
    } else {
        document.addEventListener('DOMContentLoaded', function () {
            observer.observe(document.body, {childList: true, subtree: true, attributes: true, attributeFilter: ['target']});
            removeTargetBlankFrom(document);
        });
    }
})();
