from libqtile.widget.clock import Clock


class CenteredClock(Clock):
    def draw(self):
        if self.bar and self.width:
            self.offsetx = (self.bar.width - self.width) // 2
        super().draw()
        try:
            for w in self.bar.widgets:
                if getattr(w, "name", None) in ("windowname", "windowname_box"):
                    if getattr(w, "box_is_open", False) or w.name == "windowname":
                        w.draw()
        except Exception:
            pass
