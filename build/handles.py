# -*- coding: utf-8 -*-
"""Localization handle generation.

BG3 handles are not free-form strings. They are 'h' followed by a GUID with the
dashes replaced by 'g':

    ha0a9d4d4gdd96g431dgb386g6a35a5eb2878

Fixed length, hex only. The first build used readable names like
`hEssDaoPill_Foundation_Name`, and the toolkit rejected every one of them:

    !ASSERT!Code: Translation not found for handle [hEssDaoPill_Foundation_Name]

It also broke `divine -a convert-loca`, which writes fixed-width handle records
and overran its buffer on a name that did not fit.

Handles are derived deterministically from the readable key with uuid5, so the
same key always yields the same handle and regenerating never invalidates a
save or an existing translation.
"""
import uuid

NS = uuid.UUID("6bb08ffe-62bc-4cd7-82e5-726d9cd62898")


def handle(key: str) -> str:
    """Readable key -> a valid BG3 handle."""
    return "h" + str(uuid.uuid5(NS, "loca:" + key)).replace("-", "g")


def is_valid(h: str) -> bool:
    import re
    return bool(re.fullmatch(r"h[0-9a-f]{8}g[0-9a-f]{4}g[0-9a-f]{4}"
                             r"g[0-9a-f]{4}g[0-9a-f]{12}", h))


if __name__ == "__main__":
    for k in ("hEssenceDaoResourceName", "hEssDaoPill_Foundation_Name"):
        h = handle(k)
        print(f"{k:<34} -> {h}  valid={is_valid(h)}")
