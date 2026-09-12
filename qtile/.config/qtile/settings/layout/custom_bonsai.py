from typing import cast

from libqtile.command.base import expose_command

from qtile_bonsai import Bonsai
from qtile_bonsai.tree import BonsaiPane

from ..group.scratchpads import scratchpad_layout


class MyCustomBonsai(Bonsai):
    name = "CustomBonsai"

    def __init__(self, *args, **kwargs):
        self.excluded_wm_classes = kwargs.pop("excluded_wm_classes", [])
        self.float_sizes = kwargs.pop("float_sizes", {})
        super().__init__(*args, **kwargs)
        self._pending_float = False

    def _spawn_program(self, program: str):
        """
        Override: clear any stale ``_pending_float`` before spawning.

        ``_spawn_program`` is the single gateway for all layout-initiated
        spawns (``spawn_split``, ``spawn_tab``, ``spawn``).  By clearing
        the flag here we cover every non-float spawn path automatically,
        including any future methods the parent class might add.
        """
        self._pending_float = False
        super()._spawn_program(program)

    @expose_command
    def spawn_float(self, program: str):
        """
        Launch the provided program and ensure the resulting window is floating.

        Like ``spawn_split`` / ``spawn_tab``, but the spawned window is placed
        on the floating layer instead of being added to the Bonsai tree.
        """
        self._pending_float = True
        # Bypass _spawn_program (which would clear _pending_float) by calling
        # the parent implementation directly.
        Bonsai._spawn_program(self, program)

    @expose_command
    def spawn(self, program: str):
        """
        Plain spawn — clears ``_pending_float``, then delegates.

        Replacement for ``lazy.spawn()`` in keybindings that need the flag
        cleared (e.g. ``mod+s`` which otherwise leaves a stale float flag
        after a cancelled ``spawn_float``).
        """
        self._spawn_program(program)

    def add_client(self, window):
        if self._pending_float:
            self._pending_float = False
            self._reset_next_window_handler()
            prev = self.group.current_window if self.group else None
            window.enable_floating()
            if window.group:
                window.group.mark_floating(window, True)
                self._apply_float_size(window)
                # Hide immediately before window is drawn — prevents flash
                # (deferred hide via hook would show then hide).
                try:
                    from settings.layouts import hide_floating_win

                    hide_floating_win(window)
                except Exception:
                    pass
            if prev and prev.group is self.group:
                qtile_inst = getattr(self.group, "qtile", None)
                if qtile_inst:
                    qtile_inst.call_soon(
                        lambda: self.group.focus(prev, warp=False)
                        if prev.group is self.group
                        else None
                    )
                self.group.focus(prev, warp=False)
            return
        should_keep_tree = (
            not window.can_steal_focus
            and not self._tree.is_empty
            and self.group
            and self.group.current_window is not None
        )
        if should_keep_tree:
            from qtile_bonsai.core.nodes import TabContainer

            prev_window = self.group.current_window
            prev_actives = {
                id(tc): tc.active_child
                for tc in self._tree.iter_walk()
                if isinstance(tc, TabContainer)
            }
            super().add_client(window)
            for tc in self._tree.iter_walk():
                if isinstance(tc, TabContainer) and id(tc) in prev_actives:
                    if tc.active_child is not prev_actives[id(tc)]:
                        tc.active_child = prev_actives[id(tc)]
            self._request_relayout()
            if prev_window and prev_window.group is self.group:
                qtile_inst = getattr(self.group, "qtile", None)
                if qtile_inst:
                    qtile_inst.call_soon(
                        lambda: self.group.focus(prev_window, warp=False)
                        if prev_window.group is self.group
                        else None
                    )
                self.group.focus(prev_window, warp=False)
            return
        super().add_client(window)

    def _apply_float_size(self, window):
        """Apply configured size preset to a floating window."""
        wm_class = window.get_wm_class()
        if not wm_class:
            return
        klass = wm_class[0].lower()
        spec = self.float_sizes.get(klass)
        if not spec:
            return
        screen = window.group.screen
        if not screen:
            return

        if isinstance(spec, str):
            geom = scratchpad_layout(preset=spec)
            if geom is None:
                return
            sw, sh = screen.width, screen.height
            w = int(sw * geom["width"])
            h = int(sh * geom["height"])
        else:
            w, h = int(spec[0]), int(spec[1])

        window.set_size_floating(w, h)
        window.center()

    def _handle_add_client__normal(self, window) -> BonsaiPane:
        wm_class = window.get_wm_class()
        if wm_class and self._is_excluded(wm_class):
            pane = cast(BonsaiPane, self._tree.tab())
            self._reset_next_window_handler()
            return pane
        return super()._handle_add_client__normal(window)

    def _is_excluded(self, wm_class):
        """Check if a window's WM_CLASS matches any excluded class (case-insensitive)."""
        if not self.excluded_wm_classes:
            return False
        wm_lower = [c.lower() for c in wm_class]
        return any(exc.lower() in wm_lower for exc in self.excluded_wm_classes)

    def _should_keep_focus(self) -> bool:
        cur = self.group.current_window if hasattr(self, "group") and self.group else None
        return bool(cur and cur.floating)

    @expose_command
    def focus_nth_tab(self, n: int, *, level: int = -1, keep_focus: bool | None = None):
        """Switch tab, optionally keeping focus on floating window (native no_focus_steal).

        When keep_focus is True or when current window is floating and keep_focus is None,
        only the Bonsai tree's active tab is switched (TabContainer.active_child) and
        layout is relaid, without calling group.focus. This replaces the
        _suppress_floating_hide+call_soon hacks.
        """
        if self._tree.is_empty:
            return
        if self._cancel_if_unsupported_container_select_mode_op():
            return
        if keep_focus is None:
            keep_focus = self._should_keep_focus()
        if keep_focus:
            base = self.focused_pane
            if base is None:
                try:
                    base = next(self._tree.iter_panes())
                except StopIteration:
                    return
            try:
                from qtile_bonsai.core.nodes import TabContainer

                ancestor_tcs = list(reversed(base.get_ancestors(TabContainer)))
                if not (level == -1 or 0 < level <= len(ancestor_tcs)):
                    return
                if level == -1:
                    level = len(ancestor_tcs)
                tc = ancestor_tcs[level - 1]
                if not (0 < n <= len(tc.children)):
                    return
                target_tab = tc.children[n - 1]
                try:
                    gpane = self._tree.find_mru_pane(start_node=target_tab)
                    gwin = getattr(gpane, "window", None) if gpane else None
                    if gpane is None or gwin is None or gwin not in self.group.windows:
                        try:
                            if gpane and gpane in set(self._tree.iter_panes()):
                                self._tree.remove(gpane, normalize=True)
                            else:
                                self._tree.remove(target_tab, normalize=True)
                        except Exception:
                            pass
                        self._request_relayout()
                        return
                except Exception:
                    pass
                tc.active_child = target_tab
                self._request_relayout()
                return
            except Exception:
                return
        # ghost check for non-keep path before super which would crash on window None
        try:
            base = self.focused_pane
            if base is not None:
                from qtile_bonsai.core.nodes import TabContainer as _TC2

                tcs = list(reversed(base.get_ancestors(_TC2)))
                if 0 < level <= len(tcs) or level == -1:
                    lvl = len(tcs) if level == -1 else level
                    tc2 = tcs[lvl - 1]
                    if 0 < n <= len(tc2.children):
                        tt = tc2.children[n - 1]
                        gp = self._tree.find_mru_pane(start_node=tt)
                        gw = getattr(gp, "window", None) if gp else None
                        if gp is None or gw is None or gw not in self.group.windows:
                            try:
                                if gp and gp in set(self._tree.iter_panes()):
                                    self._tree.remove(gp, normalize=True)
                                else:
                                    self._tree.remove(tt, normalize=True)
                            except Exception:
                                pass
                            self._request_relayout()
                            return
        except Exception:
            pass
        super().focus_nth_tab(n, level=level)

    @expose_command
    def next_tab(self, *, level: int = -1, wrap: bool = True, keep_focus: bool | None = None):
        if self._tree.is_empty:
            return
        if self._cancel_if_unsupported_container_select_mode_op():
            return
        if keep_focus is None:
            keep_focus = self._should_keep_focus()
        if keep_focus:
            base = self.focused_pane or next(self._tree.iter_panes(), None)
            if base is None:
                return
            pane = self._tree.next_tab(base, level=level, wrap=wrap)
            if pane is None:
                return
            gw = getattr(pane, "window", None)
            if gw is None or gw not in self.group.windows:
                try:
                    if pane in set(self._tree.iter_panes()):
                        self._tree.remove(pane, normalize=True)
                    self._request_relayout()
                except Exception:
                    pass
                return
            try:
                from qtile_bonsai.core.nodes import Tab, TabContainer

                tabs = list(reversed(pane.get_ancestors(Tab)))
                if not (level == -1 or 0 < level <= len(tabs)):
                    return
                lvl = len(tabs) if level == -1 else level
                tab = tabs[lvl - 1]
                tab.parent.active_child = tab
                self._request_relayout()
            except Exception:
                return
            return
        # ghost check before super which would crash on dead window
        try:
            base2 = self.focused_pane or next(self._tree.iter_panes(), None)
            if base2 is not None:
                gp = self._tree.next_tab(base2, level=level, wrap=wrap)
                gw2 = getattr(gp, "window", None) if gp else None
                if gp is None or gw2 is None or gw2 not in self.group.windows:
                    if gp and gp in set(self._tree.iter_panes()):
                        try:
                            self._tree.remove(gp, normalize=True)
                        except Exception:
                            pass
                    self._request_relayout()
                    return
        except Exception:
            pass
        super().next_tab(level=level, wrap=wrap)

    @expose_command
    def prev_tab(self, *, level: int = -1, wrap: bool = True, keep_focus: bool | None = None):
        if self._tree.is_empty:
            return
        if self._cancel_if_unsupported_container_select_mode_op():
            return
        if keep_focus is None:
            keep_focus = self._should_keep_focus()
        if keep_focus:
            base = self.focused_pane or next(self._tree.iter_panes(), None)
            if base is None:
                return
            pane = self._tree.prev_tab(base, level=level, wrap=wrap)
            if pane is None:
                return
            gw = getattr(pane, "window", None)
            if gw is None or gw not in self.group.windows:
                try:
                    if pane in set(self._tree.iter_panes()):
                        self._tree.remove(pane, normalize=True)
                    self._request_relayout()
                except Exception:
                    pass
                return
            try:
                from qtile_bonsai.core.nodes import Tab, TabContainer

                tabs = list(reversed(pane.get_ancestors(Tab)))
                if not (level == -1 or 0 < level <= len(tabs)):
                    return
                lvl = len(tabs) if level == -1 else level
                tab = tabs[lvl - 1]
                tab.parent.active_child = tab
                self._request_relayout()
            except Exception:
                return
            return
        try:
            base2 = self.focused_pane or next(self._tree.iter_panes(), None)
            if base2 is not None:
                gp = self._tree.prev_tab(base2, level=level, wrap=wrap)
                gw2 = getattr(gp, "window", None) if gp else None
                if gp is None or gw2 is None or gw2 not in self.group.windows:
                    if gp and gp in set(self._tree.iter_panes()):
                        try:
                            self._tree.remove(gp, normalize=True)
                        except Exception:
                            pass
                    self._request_relayout()
                    return
        except Exception:
            pass
        super().prev_tab(level=level, wrap=wrap)

    @expose_command
    def pull_floating_to_tab(self, *, normalize: bool = True):
        """Pull the currently focused floating window into a new tab.

        If the focused window is floating, it is first tiled via
        ``disable_floating()`` (which triggers ``Group.mark_floating`` ->
        ``Layout.add_client``), focused, then pulled out to a new tab at
        the nearest ``TabContainer`` via Bonsai's ``pull_out_to_tab``.
        If the window is already tiled, it is simply pulled out to a tab.
        """
        win = self.group.current_window
        if win is None:
            return
        if win.floating:
            try:
                win.disable_fullscreen()
            except Exception:
                pass
            win.disable_floating()
            self.group.focus(win)
        if self._tree.is_empty:
            return
        pane = self.focused_pane
        if pane is None:
            return
        if self._cancel_if_unsupported_container_select_mode_op():
            return
        try:
            self._tree.pull_out_to_tab(pane, normalize=normalize)
        except ValueError:
            return
        self._request_relayout()

    @expose_command
    def pull_out_to_tab(self, *, normalize: bool = True):
        """Extract the currently focused window into a new tab.

        Handles floating windows for backward compat by delegating to
        ``pull_floating_to_tab`` when the focused window is floating.
        Otherwise behaves like the parent ``Bonsai.pull_out_to_tab``.
        """
        win = self.group.current_window
        if win is not None and win.floating:
            self.pull_floating_to_tab(normalize=normalize)
            return
        if self._tree.is_empty:
            return
        pane = self.focused_pane
        if pane is None:
            return
        if self._cancel_if_unsupported_container_select_mode_op():
            return
        try:
            self._tree.pull_out_to_tab(pane, normalize=normalize)
        except ValueError:
            return
        self._request_relayout()
