# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import iamraw
import iamraw.toc
import utila

import elements.headline.lookup


class InvalidTocItems(collections.UserList):  # pylint:disable=too-many-ancestors
    pass


def toc_flat(toc: iamraw.Toc):
    """Remove nested order and deliver a top down list of pages and
    sections."""
    result = []

    def godown(item: iamraw.toc.TocLinkMixin):
        result.append(item)
        for children in item:
            godown(children)

    for item in toc:
        godown(item)

    return result


def istoc(headline: str) -> bool:
    """\
    >>> istoc('Inhaltverzeichnis')
    True
    """
    if utila.similar(
            current=headline,
            expected=elements.headline.lookup.TOC,
            maxdiff=0.9,
    ):
        return True
    return False
