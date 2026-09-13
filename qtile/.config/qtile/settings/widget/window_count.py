from libqtile import bar, hook
from libqtile.widget import base


class WindowCount(base._TextBox):
    defaults = [
        ("text_format", " 󰾆 {num} ", "Format for window count"),
        ("show_zero", True, "Show window count when no windows"),
    ]

    def __init__(self, **config):
        base._TextBox.__init__(self, **config)
        self.add_defaults(WindowCount.defaults)
        self._count = 0

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        self._setup_hooks()
        self._wincount()

    def _setup_hooks(self):
        hook.subscribe.client_killed(self._win_killed)
        hook.subscribe.client_managed(self._wincount)
        hook.subscribe.current_screen_change(self._wincount)
        hook.subscribe.group_window_add(self._wincount)
        hook.subscribe.group_window_remove(self._wincount)
        hook.subscribe.setgroup(self._wincount)

    def _wincount(self, *args):
        try:
            self._count = len(self.bar.screen.group.windows)
        except AttributeError:
            self._count = 0
        self.update(self.text_format.format(num=self._count))

    def _win_killed(self, window):
        if self.qtile:
            self.qtile.call_soon(self._wincount)

    def calculate_length(self):
        if self._count or self.show_zero:
            return base._TextBox.calculate_length(self)
        return 0

    def finalize(self):
        hook.unsubscribe.client_killed(self._win_killed)
        hook.unsubscribe.client_managed(self._wincount)
        hook.unsubscribe.current_screen_change(self._wincount)
        hook.unsubscribe.group_window_add(self._wincount)
        hook.unsubscribe.group_window_remove(self._wincount)
        hook.unsubscribe.setgroup(self._wincount)
        super().finalize()
