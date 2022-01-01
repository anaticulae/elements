# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import elements

NOHEADLINES = utila.splitlines("""\
2.3. Ermittelte charakteristische Punkte mit Standardabweichung . . . . . 7
Abbildung 1.3.: Impulsfolgegruppe besteht aus drei Impulsfolgen
""")


@pytest.mark.parametrize('headline', [
    pytest.param(item, id=str(index)) for index, item in enumerate(NOHEADLINES)
])
def test_no_headline(headline):
    isheadline = elements.isheadline(headline, strict=False)
    assert not isheadline, headline
