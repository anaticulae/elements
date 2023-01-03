# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import elements

EXAMPLE = iamraw.Toc(children=[
    iamraw.SectionRaw(
        raw_level='6.1.2',
        title='Funktionalität und Benutzbarkeit',
        page=63,
        raw='6.1.2 Funktionalität und Benutzbarkeit . . . . . . . . . . . . 63',
        level='3',
    ),
    iamraw.SectionRaw(
        raw_level='6.2',
        title='Demonstration des Prototypen',
        page=66,
        raw='6.2 Demonstration des Prototypen . . . . 66',
        level='2',
    ),
    iamraw.SectionRaw(
        raw_level='6',
        title='Evaluierung und Demonstration des Prototypen',
        page=62,
        raw='6 Evaluierung und Demonstration des Prototypen 62',
        level='1',
    ),
    iamraw.SectionRaw(
        raw_level='7',
        title='Zusammenfassung und Ausblick',
        page=76,
        raw='7 Zusammenfassung und Ausblick 76',
        level='1',
    ),
])


def test_toc_flat():
    flat = elements.toc_flat(EXAMPLE)
    assert len(flat) == 4


def test_toc_numbered():
    flat = elements.toc_flat(EXAMPLE)
    style = elements.toc_style(flat, toc_length_min=1)
    assert style == iamraw.TocStyle.NUMBERED
    assert elements.istocnumbered(flat) == iamraw.TocStyle.NUMBERED


INVALID_TOC = [
    elements.InvalidPage(
        current=62,
        before=66,
        text='Evaluierung und Demonstration des Prototypen',
        raw_location=0,
    )
]


def test_toc_validate():
    invalids = elements.validate_toc(EXAMPLE)
    assert invalids == INVALID_TOC
