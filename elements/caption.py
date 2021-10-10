# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re


def iscaption(text: str) -> bool:
    """\
    >>> iscaption('Abbildung 4.2.: Softwareentwicklung Übersicht')
    True
    """
    text = text.strip()
    if iscaption_figure(text):
        return True
    if iscaption_code(text):
        return True
    return False


FIGURE = re.compile(
    r"""^
    (Abb.?|Abbildung|Fig.?|Figure)
    [ ]{0,3}
    (
        \d{1,2}\.?(\d{1,2}.?)?|
        [A-Z]
    )
    [ ]{0,3}
    :?
    .{0,50}$
""",
    re.X | re.I,
)


def iscaption_figure(text: str) -> bool:
    """\
    >>> iscaption_figure('Abbildung11.1 Entwicklungsstand der Proﬁle')
    True
    >>> iscaption_figure('Figure1 : Valence and arousal describe emotions')
    True
    """
    text = text.strip()
    if FIGURE.match(text):
        return True
    return False


LISTING = re.compile(
    r"""^
    Listing
    [ ]{0,3}
    (\d{1,2}.\d{1,2}.?|)
    [ ]{0,3}
    :?
    """,
    re.X | re.I,
)


def iscaption_code(text: str) -> bool:
    """\
    >>> iscaption_code('Listing3.1:Bewertung von Tweets')
    True
    """
    text = text.strip()
    if LISTING.match(text):
        return True
    return False
