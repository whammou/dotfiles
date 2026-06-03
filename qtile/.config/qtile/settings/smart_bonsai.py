from __future__ import annotations

from typing import TYPE_CHECKING

from qtile_bonsai.core.nodes import Axis
from qtile_bonsai.layout import BonsaiPane

if TYPE_CHECKING:
    from qtile_bonsai.tree import BonsaiTree


def smart_split(tree: BonsaiTree) -> BonsaiPane:
    """Adaptively split the largest visible pane in the bonsai tree.

    If the tree is empty, creates a single tab for the first window.
    Otherwise finds the largest pane among **visible** tabs (the
    currently active tab chain) and splits it along its longer axis
    — horizontally (``Axis.x``, left/right) if the pane is wider
    than tall, vertically (``Axis.y``, top/bottom) if taller or
    square. Background/inactive tabs are never targeted. Falls back
    to creating a new tab if no visible panes exist.
    """
    if tree.is_empty:
        return tree.tab()

    visible = list(tree.iter_panes(visible=True))
    if not visible:
        return tree.tab()

    largest = max(visible, key=lambda p: p.principal_rect.w * p.principal_rect.h)
    w = largest.principal_rect.w
    h = largest.principal_rect.h
    axis = Axis.x if w > h else Axis.y

    return tree.split(largest, axis, normalize=True)
