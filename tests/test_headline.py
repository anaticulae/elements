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

NOT_IS_HEADLINE = utila.splitlines("""\
2.3. Ermittelte charakteristische Punkte mit Standardabweichung . . . . . 7
Abbildung 1.3.: Impulsfolgegruppe besteht aus drei Impulsfolgen
Gutachter: Prof. Dr. Gjorgji Madjarov
""")

NOHEADLINE = utila.splitlines("""\
Gutachter: Prof. Dr. Gjorgji Madjarov
- Dr.-Ing. -
Vorsitzender: Prof. Dr. Florian Tschorsch Gutachter: Prof. Dr. Odej Kao
s.  Abb.  7a).
0 % 20 % 40 % 60 % 80 % 100 %
""")


@pytest.mark.parametrize('headline', [
    pytest.param(item, id=str(index))
    for index, item in enumerate(NOT_IS_HEADLINE)
])
def test_is_not_headline(headline):
    isheadline = elements.isheadline(headline, strict=False)
    assert not isheadline, headline


@pytest.mark.parametrize('headline', [
    pytest.param(item, id=str(index)) for index, item in enumerate(NOHEADLINE)
])
def test_noheadline(headline):
    noheadline = elements.noheadline(headline)
    assert noheadline, headline


@pytest.mark.timeout(2)
def test_parse_leveled_headline_numbers_timeout():
    longrun = '356891013151618192023252628293031323312471112141721222427'
    assert not elements.parse_leveled_headline(longrun)


@pytest.mark.timeout(2)
def test_parse_leveled_headline_chars_timeout():
    longrun = 'ahsdkfhakhdkfhasdkfhakshdfkjasdhdfkshaskhdkhafsdkh'
    assert not elements.parse_leveled_headline(longrun)
