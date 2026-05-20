# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilo

import elementae

HEADLINE_LEVEL = utilo.splitlines("""\
1   2. Zentrum
2   2.1 Anhang
2   2..1... Fehlerfrei
""")


@pytest.mark.parametrize('line', [
    pytest.param(item, id=str(index))
    for index, item in enumerate(HEADLINE_LEVEL)
])
def test_headline_level(line):
    expected, raw = line.split(maxsplit=1)
    expected = int(expected)
    level = elementae.level_numbered(raw)
    assert level == expected


NOHEADLINE_LEVEL = utilo.splitlines("""\
2020 This is not a headline level
04.03.2016. No Headline
""")


@pytest.mark.parametrize('noheadline', [
    pytest.param(item, id=str(index))
    for index, item in enumerate(NOHEADLINE_LEVEL)
])
def test_noheadline_level(noheadline):
    nolevel = elementae.level_numbered(noheadline)
    assert nolevel is False  # pylint:disable=C2001
