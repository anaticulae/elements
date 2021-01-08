# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def level_numbered(raw: str) -> int:
    """Convert number to raw level.

    >>> level_numbered('5 Geology')
    1
    >>> level_numbered('2. Zentrum')
    1
    >>> level_numbered('2.1.3. Abschluss')
    3
    >>> level_numbered('2.1 Anhang')
    2
    >>> level_numbered('2..1... Fehlerfrei') # ignore typos
    2
    >>> level_numbered('2020 This is not a headline level')
    False
    >>> level_numbered('04.03.2016. No Headline')
    False
    """
    # TODO: SUPPORT LEVEL WITHOUT SPACE
    # TODO: MOVE TESTS?
    raw = raw.strip()
    if not raw:
        return None
    raw = raw.split()[0]
    try:
        splitted = [int(item) for item in raw.split('.') if item]
        if max(splitted) > 20:
            return False
    except ValueError:
        return None
    return len(splitted)
