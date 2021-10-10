# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import utila

PATTERN = r"""
    ^
    (%s)
    [ ]{0,3}
    (
        \d{1,2}\.?(\d{1,2}.?)?|
        [A-Z]
    )
    [ ]{0,3}
    :?
    .{0,50}
    $
"""


def compiles(caption: str):
    pattern = PATTERN % caption
    result = re.compile(
        pattern,
        flags=utila.NOCASE_VERBOSE,
    )
    return result


CAPTIONS = r"""
Abb.?|Abbildung|Fig.?|Figure|
Listing|
Tab.?|Tabelle|Table
"""

CAPTIONX = compiles(CAPTIONS)


def iscaption(text: str) -> bool:
    """\
    >>> iscaption('Abbildung 4.2.: Softwareentwicklung Übersicht')
    True
    """
    text = text.strip()
    if CAPTIONX.match(text):
        return True
    return False


FIGUREX = compiles(r'Abb.?|Abbildung|Fig.?|Figure')


def iscaption_figure(text: str) -> bool:
    """\
    >>> iscaption_figure('Abbildung11.1 Entwicklungsstand der Proﬁle')
    True
    >>> iscaption_figure('Figure1 : Valence and arousal describe emotions')
    True
    """
    text = text.strip()
    if FIGUREX.match(text):
        return True
    return False


LISTINGX = compiles(r'Listing')


def iscaption_code(text: str) -> bool:
    """\
    >>> iscaption_code('Listing3.1:Bewertung von Tweets')
    True
    """
    text = text.strip()
    if LISTINGX.match(text):
        return True
    return False


TABLEX = compiles(r'Tab.?|Tabelle|Table')


def iscaption_table(text: str) -> bool:
    """\
    >>> iscaption_table('Tab. 3: Mittelwerte und Standardabweichungen')
    True
    """
    text = text.strip()
    if TABLEX.match(text):
        return True
    return False
