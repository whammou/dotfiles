from __future__ import annotations

from typing import TYPE_CHECKING, cast

from qtile_bonsai.core.nodes import Axis, SplitContainer, TabContainer
from qtile_bonsai.layout import BonsaiPane

if TYPE_CHECKING:
    from qtile_bonsai.tree import BonsaiTree


def smart_split(tree: BonsaiTree) -> BonsaiPane:
    if tree.is_empty:
        return cast(BonsaiPane, tree.tab())
    visible = list(tree.iter_panes(visible=True))
    if not visible:
        return cast(BonsaiPane, tree.tab())
    largest = max(visible, key=lambda p: p.principal_rect.w * p.principal_rect.h)
    w = largest.principal_rect.w
    h = largest.principal_rect.h
    axis = Axis.x if w > h else Axis.y
    return cast(BonsaiPane, tree.split(largest, axis, normalize=True))


def _focused_container(tree: BonsaiTree):
    try:
        mru = tree.find_mru_pane()
    except Exception:
        return None
    deepest = None
    for tc in mru.get_ancestors(TabContainer):
        if tc.tab_level > 1:
            if deepest is None or tc.tab_level > deepest.tab_level:
                deepest = tc
    return deepest


def smart_split_optimal(tree: BonsaiTree) -> BonsaiPane:
    """Isolated split: L1 excluded, L2+ isolated, L3/L4... deep isolation.

    - If MRU inside L2+ deepest container, split MRU directly (inside that container only).
    - Else (no L2+ focus), ignore all containers: split largest L1-visible pane; if none, split L1 SplitContainer outside.
    """
    if tree.is_empty:
        return cast(BonsaiPane, tree.tab())

    focused_tc = _focused_container(tree)
    if focused_tc is not None and tree.is_visible(focused_tc):
        try:
            mru = tree.find_mru_pane()
            if focused_tc in mru.get_ancestors(TabContainer):
                w = mru.principal_rect.w
                h = mru.principal_rect.h
                axis = Axis.x if w > h else Axis.y
                return cast(BonsaiPane, tree.split(mru, axis, normalize=True))
        except Exception:
            pass
        # fallback: scoped visible inside focused container
        visible = list(tree.iter_panes(visible=True))
        filtered = [p for p in visible if focused_tc in p.get_ancestors(TabContainer)]
        if filtered:
            largest = max(filtered, key=lambda p: p.principal_rect.w * p.principal_rect.h)
            w = largest.principal_rect.w
            h = largest.principal_rect.h
            axis = Axis.x if w > h else Axis.y
            return cast(BonsaiPane, tree.split(largest, axis, normalize=True))

    visible = list(tree.iter_panes(visible=True))
    if not visible:
        return cast(BonsaiPane, tree.tab())

    l1_visible = [p for p in visible if not any(tc.tab_level > 1 for tc in p.get_ancestors(TabContainer))]
    if l1_visible:
        largest = max(l1_visible, key=lambda p: p.principal_rect.w * p.principal_rect.h)
        w = largest.principal_rect.w
        h = largest.principal_rect.h
        axis = Axis.x if w > h else Axis.y
        return cast(BonsaiPane, tree.split(largest, axis, normalize=True))

    try:
        root_tc = tree.root
        if root_tc is not None and len(root_tc.children) > 0:
            active_tab = root_tc.active_child
            if active_tab is not None and len(active_tab.children) > 0:
                l1_sc = active_tab.children[0]
                if isinstance(l1_sc, SplitContainer):
                    w = l1_sc.principal_rect.w
                    h = l1_sc.principal_rect.h
                    axis = Axis.x if w > h else Axis.y
                    return cast(BonsaiPane, tree.split(l1_sc, axis, normalize=True))
    except Exception:
        pass
    return cast(BonsaiPane, tree.tab())


_focused_l2_container = _focused_container
