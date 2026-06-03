from __future__ import annotations

from typing import TYPE_CHECKING

from qtile_bonsai.core.nodes import Axis
from qtile_bonsai.layout import BonsaiPane

if TYPE_CHECKING:
    from qtile_bonsai.tree import BonsaiTree


def smart_split(tree: BonsaiTree) -> BonsaiPane:
    """Adaptively split the largest pane in the bonsai tree.

    If the tree is empty, creates a single tab for the first window.
    Otherwise finds the pane with the largest area (width × height)
    and splits it along its longer axis — horizontally (``Axis.x``,
    left/right) if the pane is wider than tall, vertically
    (``Axis.y``, top/bottom) if taller or square. The new window is
    placed at the next position along the split direction
    (``Direction1D.next``, the default).
    """
    if tree.is_empty:
        return tree.tab()

    largest = max(tree.iter_panes(), key=lambda p: p.principal_rect.w * p.principal_rect.h)
    w = largest.principal_rect.w
    h = largest.principal_rect.h
    axis = Axis.x if w > h else Axis.y

    return tree.split(largest, axis, normalize=True)
