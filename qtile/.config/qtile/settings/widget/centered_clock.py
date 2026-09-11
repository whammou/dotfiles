from libqtile.widget.clock import Clock


class CenteredClock(Clock):
    def draw(self):
        if self.bar and self.width:
            self.offsetx = (self.bar.width - self.width) // 2
        super().draw()
