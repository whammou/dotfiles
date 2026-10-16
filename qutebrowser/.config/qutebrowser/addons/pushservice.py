# pushservice.py - enable QtWebEngine Web Push (PushManager/Service Workers).
# QtWebEngine >= 6.5 exposes QWebEngineProfile.setPushServiceEnabled(), but it
# defaults to disabled and qutebrowser 3.7.0 never enables it, so
# PushManager.subscribe() fails and background push never arrives. Like
# pinnedtitle.py, this module waits for the app and hooks instances via objreg
# and module state instead of patching at config-source time: qutebrowser
# purges sys.modules entries added while sourcing a config file
# (configfiles.saved_sys_properties), so imports done here must happen at arm()
# time, when the event loop is running and webenginesettings is the real
# module. Push requires a persistent (non-off-the-record) profile, a secure
# context, granted notification permission and server-side VAPID keys; Qt uses
# Firebase Cloud Messaging under the hood, so pushes transit Google servers.
import threading
import time
from typing import Any

from qutebrowser.misc import objects
from qutebrowser.qt.core import QMetaObject, QObject, Qt, pyqtSlot
from qutebrowser.utils import log


def _enable(profile: Any) -> None:
    # Off-the-record profiles cannot do push (Chromium has no push service
    # for them); enabling there is a no-op at best, so skip explicitly.
    try:
        if profile is None:
            return
        try:
            from qutebrowser.qt import sip

            if sip.isdeleted(profile):
                return
        except Exception:
            pass
        if profile.isOffTheRecord():
            log.misc.debug("pushservice: skip off-the-record profile")
            return
        setter = getattr(profile, "setPushServiceEnabled", None)
        if setter is None:
            # Qt < 6.5: no push service API at all.
            log.misc.debug("pushservice: setPushServiceEnabled unavailable (Qt < 6.5?)")
            return
        setter(True)
        log.misc.info("pushservice: push service enabled")
    except Exception:
        log.misc.exception("pushservice: enabling push failed")


def _arm() -> None:
    try:
        from qutebrowser.browser.webengine import webenginesettings

        if getattr(webenginesettings, "_pushservice_installed", False):
            # :config-source re-exec: the wrapper from the previous
            # generation is still installed on this (persistent) module, so
            # only re-apply to live profiles instead of double-wrapping.
            _enable(getattr(webenginesettings, "default_profile", None))
            return

        orig_init = webenginesettings._init_profile

        def _init_profile_with_push(profile: Any) -> None:
            orig_init(profile)
            _enable(profile)

        webenginesettings._init_profile = _init_profile_with_push
        setattr(webenginesettings, "_pushservice_installed", True)

        # Profiles already created during startup (arm runs when the event
        # loop starts, after websettings.init): enable before any page can
        # call PushManager.subscribe(). The push service itself starts
        # lazily on first subscription, so this is still early enough.
        _enable(getattr(webenginesettings, "default_profile", None))
        _enable(getattr(webenginesettings, "private_profile", None))
    except Exception:
        log.misc.exception("pushservice: arm failed")


class _Scheduler(QObject):

    @pyqtSlot()
    def arm(self) -> None:
        _arm()


def _wait_for_app() -> None:
    # Daemon thread: at interpreter shutdown the objects module is torn down
    # while this thread may still be polling; any error then is irrelevant
    # (the process is exiting), just stop quietly.
    try:
        while objects.qapp is None:
            time.sleep(0.02)
        QMetaObject.invokeMethod(
            _scheduler, "arm", Qt.ConnectionType.QueuedConnection
        )
    except Exception:
        return


_scheduler = _Scheduler()
threading.Thread(target=_wait_for_app, daemon=True).start()
