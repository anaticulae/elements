# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import utila

PATTERN = r"""
    ^
    (?P<label>
        (%s)
        [ ]{0,3}
        (
            \d{1,2}\-\d{1,2}|
            \d{1,2}\.?(\d{1,2}\.?)?|
            [A-Z]
        )
    )
    [ ]{0,3}
    \:{0,1}
    [ ]{0,3}
    (?P<text>.{3,})
    $
"""


@configo.cache_large
def parse_caption(text: str) -> tuple:
    """\
    >>> parse_caption('Tab. 4.2.: Wirkungsgrad der elektrischen Komponenten [Pfe14], [IAV15].')
    ('Tab. 4.2.', 'Wirkungsgrad der elektrischen Komponenten [Pfe14], [IAV15].')
    """
    matched = CAPTIONX.match(text)
    if not matched:
        return None
    label = matched['label']
    text = matched['text']
    return label, text


def compiles(caption: str):
    return utila.compiles(PATTERN % caption)


CAPTIONS = r"""
Abbildung|Abb\.?|Figure|Fig\.?|
Listing|Algorithmus|
Tabelle|Table|Tab\.?|
Graph
"""

CAPTIONX = compiles(CAPTIONS)


@configo.cache_large
def iscaption(text: str) -> bool:
    """\
    >>> iscaption('Abbildung 4.2.: Softwareentwicklung Übersicht')
    True
    >>> iscaption('Figure 1). This model can expl')
    False
    >>> iscaption('Abb. 5) eine Paper-and-Pencil-Version des SAM aus.')
    False
    >>> iscaption('Graph 8: scenario 3: slow development of private e-currency.')
    True
    >>> iscaption('Tab. 4.2.: Wirkungsgrad der elektrischen Komponenten [Pfe14], [IAV15].')
    True
    >>> iscaption('Graph6:scenario 1: fast developing private e-currency.')
    True
    >>> iscaption('Abbildung 7-22: Vergleich der Massen und Volumina zwischen einem')
    True
    """
    text = text_limit(text)
    matched = CAPTIONX.match(text)
    if not matched:
        return False
    txt = matched['text']
    if txt[0] == ')':
        # TODO: IMPROVE NEGATIVE LOOKUP
        return False
    return True


FIGUREX = compiles(r'Abb.?|Abbildung|Fig.?|Figure|Graph')


@configo.cache_large
def iscaption_figure(text: str) -> bool:
    """\
    >>> iscaption_figure('Abbildung11.1 Entwicklungsstand der Proﬁle')
    True
    >>> iscaption_figure('Figure1 : Valence and arousal describe emotions')
    True
    """
    text = text_limit(text)
    if FIGUREX.match(text):
        return True
    return False


LISTINGX = compiles(r'Listing|Algorithmus')


@configo.cache_large
def iscaption_code(text: str) -> bool:
    """\
    >>> iscaption_code('Listing3.1:Bewertung von Tweets')
    True
    >>> iscaption_code('Algorithmus 7.3: Prove-Operator für die Aktualisierung ')
    True
    """
    text = text_limit(text)
    if LISTINGX.match(text):
        return True
    return False


TABLEX = compiles(r'Tab.?|Tabelle|Table')


@configo.cache_large
def iscaption_table(text: str) -> bool:
    """\
    >>> iscaption_table('Tab. 3: Mittelwerte und Standardabweichungen')
    True
    >>> iscaption_table('Tab.4.2.: Wirkungsgrad der elektrischen Komponenten [Pfe14], [IAV15].')
    True
    >>> iscaption_table('TabelleA.1.: Konﬁguration Simulink Modell')
    True
    """
    text = text_limit(text)
    if TABLEX.match(text):
        return True
    return False


def text_limit(text):
    text = text.strip()
    text = text[0:25]
    return text
