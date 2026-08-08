// Per-site proxy rules for qutebrowser.
//
// qutebrowser's content.proxy cannot be set per-domain via config.set patterns
// (QtWebEngine limitation), so per-site routing is done here. This PAC file is
// evaluated by Chromium per-request with URL + hostname available.
//
// Rule: the dev server at 192.168.0.104:5173 is reachable only through the
// SOCKS5 tunnel (ssh -D 1080); everything else goes DIRECT.
//
// Note: PAC replaces the system proxy lookup entirely — if a system proxy is
// needed for other traffic, add explicit rules below before the DIRECT return.

function FindProxyForURL(url, host) {
    if (shExpMatch(url, "http://192.168.0.104:5173*")) {
        return "SOCKS5 127.0.0.1:1080";
    }
    return "DIRECT";
}
