#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os
from importlib.metadata import version as metaversion

import elementae.__patch__
from elementae.caption import iscaption
from elementae.caption import iscaption_code
from elementae.caption import iscaption_figure
from elementae.caption import iscaption_table
from elementae.caption import parse_caption
from elementae.headline.decide import isheadline
from elementae.headline.decide import noheadline
from elementae.headline.decide import noheadline_pattern
from elementae.headline.decide import singlechar
from elementae.headline.level import determine_patch
from elementae.headline.level import level_numbered
from elementae.headline.level import level_steps
from elementae.headline.lookup import ABBREVIATION
from elementae.headline.lookup import ABSTRACT
from elementae.headline.lookup import ACKNOWLEDGE
from elementae.headline.lookup import APPENDIX
from elementae.headline.lookup import BIBLIOGRAPHY
from elementae.headline.lookup import CHAPTER
from elementae.headline.lookup import FIGURETABLE
from elementae.headline.lookup import GLOSSARY
from elementae.headline.lookup import HEADLINES
from elementae.headline.lookup import LEGAL
from elementae.headline.lookup import LISTINGS
from elementae.headline.lookup import PUBLICATION
from elementae.headline.lookup import SYMBOLTABLE
from elementae.headline.lookup import TABLETABLE
from elementae.headline.lookup import TOC
from elementae.headline.lookup import UTILS
from elementae.headline.lookup import VITAE
from elementae.headline.parser import parse_chapter_level
from elementae.headline.parser import parse_headline
from elementae.headline.parser import parse_leveled_headline
from elementae.pagenumber import InvalidPage
from elementae.pagenumber import InvalidPages
from elementae.pagenumber import InvalidRomanPageNumber
from elementae.pagenumber import isnumber_withgaps
from elementae.pagenumber import ispagenumber
from elementae.pagenumber import validate_pageorder
from elementae.pagenumber import validate_toc
from elementae.quote import isquote
from elementae.toc import istoc
from elementae.toc import istocnolevel
from elementae.toc import istocnumbered
from elementae.toc import istocsections
from elementae.toc import istocstepped
from elementae.toc import toc_flat
from elementae.toc import toc_style

__version__ = metaversion('elementae')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# TODO: REMOVE WITH MAJOR
GLOSSAR = GLOSSARY
