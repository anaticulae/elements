# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re


def level_numbered(raw: str) -> int:
    """Convert number to raw level.

    >>> level_numbered('5 Geology')
    1
    >>> level_numbered('2.1.3. Abschluss')
    3
    >>> level_numbered('a. Gesamtbewertung')
    4
    """
    # TODO: SUPPORT LEVEL WITHOUT SPACE
    raw = raw.strip()
    if not raw:
        return None

    dots = level_numbered_dots(raw)
    if dots is not None:
        return dots

    chars = level_numbered_chars(raw)
    if chars is not None:
        return chars
    return None


def level_numbered_dots(raw: str) -> int:
    raw = raw.split()[0]
    try:
        splitted = [int(item) for item in raw.split('.') if item]
        if max(splitted) > 20:
            return False
    except ValueError:
        return None
    return len(splitted)


CHAR_PATTERN = re.compile(r'^[a-zA-Z]\.')


def level_numbered_chars(raw: str) -> int:
    """\
    >>> level_numbered_chars('d. Gesamtbewertung')
    4
    """
    if not CHAR_PATTERN.match(raw):
        return None
    return 4
