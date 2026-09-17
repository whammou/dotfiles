from libqtile import bar
from libqtile.widget.clock import Clock


class CenteredClock(Clock):
    GAP = 0

    def draw(self):
        if self.bar and self.width:
            ideal = (self.bar.width - self.width) // 2
            try:
                idx = self.bar.widgets.index(self)
                left_fixed = sum(
                    w.length for w in self.bar.widgets[:idx] if w.length_type != bar.STRETCH
                )
                right_fixed = sum(
                    w.length for w in self.bar.widgets[idx + 1 :] if w.length_type != bar.STRETCH
                )
                left_limit = left_fixed + self.GAP
                right_limit = self.bar.width - right_fixed - self.width - self.GAP
                if right_limit < left_limit:
                    self.offsetx = left_limit
                else:
                    self.offsetx = max(left_limit, min(ideal, right_limit))
            except Exception:
                self.offsetx = ideal
        super().draw()
        try:
            for w in self.bar.widgets:
                if getattr(w, "name", None) in ("windowname", "windowname_box"):
                    if getattr(w, "box_is_open", False) or w.name == "windowname":
                        w.draw()
        except Exception:
            pass
