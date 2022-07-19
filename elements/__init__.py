#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import elements.__patch__
from elements.caption import iscaption
from elements.caption import iscaption_code
from elements.caption import iscaption_figure
from elements.caption import iscaption_table
from elements.caption import parse_caption
from elements.headline.decide import isheadline
from elements.headline.decide import noheadline
from elements.headline.decide import noheadline_pattern
from elements.headline.decide import singlechar
from elements.headline.level import determine_patch
from elements.headline.level import level_numbered
from elements.headline.level import level_steps
from elements.headline.lookup import ABBREVIATION
from elements.headline.lookup import ABSTRACT
from elements.headline.lookup import ACKNOWLEDGE
from elements.headline.lookup import APPENDIX
from elements.headline.lookup import BIBLIOGRAPHY
from elements.headline.lookup import CHAPTER
from elements.headline.lookup import FIGURETABLE
from elements.headline.lookup import GLOSSARY
from elements.headline.lookup import HEADLINES
from elements.headline.lookup import LEGAL
from elements.headline.lookup import LISTINGS
from elements.headline.lookup import SYMBOLTABLE
from elements.headline.lookup import TABLETABLE
from elements.headline.lookup import TOC
from elements.headline.lookup import UTILS
from elements.headline.lookup import VITAE
from elements.headline.parser import parse_chapter_level
from elements.headline.parser import parse_headline
from elements.headline.parser import parse_leveled_headline
from elements.pagenumber import InvalidPage
from elements.pagenumber import InvalidPages
from elements.pagenumber import InvalidRomanPageNumber
from elements.pagenumber import isnumber_withgaps
from elements.pagenumber import ispagenumber
from elements.pagenumber import validate_pageorder
from elements.pagenumber import validate_toc
from elements.quote import isquote
from elements.toc import istoc
from elements.toc import istocnolevel
from elements.toc import istocnumbered
from elements.toc import istocsections
from elements.toc import istocstepped
from elements.toc import toc_flat
from elements.toc import toc_style

__version__ = '0.21.4'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# TODO: REMOVE WITH MAJOR
GLOSSAR = GLOSSARY
