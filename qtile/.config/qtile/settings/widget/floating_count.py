from libqtile import hook, qtile
from libqtile.widget import base


class FloatCount(base._TextBox):
    defaults = [
        ("format", " {count}", "Display format for the number of floating windows."),
    ]

    def __init__(self, **config):
        base._TextBox.__init__(self, text="0", **config)
        self.add_defaults(FloatCount.defaults)

    def _configure(self, qtile, bar):
        super()._configure(qtile, bar)
        hook.subscribe.client_managed(self.update_count)
        hook.subscribe.float_change(self.update_count)
        hook.subscribe.setgroup(self.update_count)
        hook.subscribe.client_killed(self._on_client_killed)
        self.update_count()

    def _on_client_killed(self, *args, **kwargs):
        if self.qtile:
            self.qtile.call_soon(self.update_count)

    def update_count(self, *args, **kwargs):
        if not qtile or not qtile.current_group:
            count = 0

        else:
            count = sum(1 for w in qtile.current_group.windows if w.floating)

        new_text = self.format.format(count=count)

        if self.text != new_text:
            self.text = new_text
            self.bar.draw()

    def finalize(self):
        hook.unsubscribe.client_managed(self.update_count)
        hook.unsubscribe.float_change(self.update_count)
        hook.unsubscribe.setgroup(self.update_count)
        hook.unsubscribe.client_killed(self._on_client_killed)
        super().finalize()
