# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import difflib

import utila


def lower(*items):
    """Lowercase list of strings.
    >>> lower('Helmut', 'MANFRED')
    ['helmut', 'manfred']
    """
    return [item.lower() for item in items]


def splitlines(raw: str, lowers: bool = True) -> set:
    r"""Split string by newlines and convert to set.

    >>> splitlines('First\nThird\nSecond')
    {'third', 'second', 'first'}
    """
    splitted = raw.splitlines()
    if lowers:
        splitted = lower(*splitted)
    return set(splitted)


utila.splitlines = splitlines


def similar(expected: str, current: str, maxdiff=0.6) -> bool:
    """\
    >>> similar('Abbildungsverzeichnis', 'ab_ildungsverzeichnis')
    True
    >>> similar('Helm', 'Konrad')
    False
    >>> similar(['Abbildungsverzeichnis', 'Abbildungen'], 'Abbildung', maxdiff=0.1)
    True
    """
    if isinstance(expected, (list, tuple, set)):
        for item in expected:
            if similar(item, current, maxdiff):
                return True
        return False
    expected, current = expected.lower(), current.lower()
    if expected == current:
        return True
    matched = difflib.get_close_matches(
        current,
        [expected],
        n=1,
        cutoff=maxdiff,
    )
    if matched:
        return True
    return False


utila.similar = similar
