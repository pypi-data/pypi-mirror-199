#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   text.pyi
# @Created At:  2023-03-20 17:47:55
# @Modified At: 2023-03-20 18:02:58
# @Modified By: thepoy

from .base import XmlEnumeration, EnumValue

class WD_PARAGRAPH_ALIGNMENT(XmlEnumeration):
    LEFT: EnumValue
    CENTER: EnumValue
    RIGHT: EnumValue
    JUSTIFY: EnumValue
    DISTRIBUTE: EnumValue
    JUSTIFY_MED: EnumValue
    JUSTIFY_HI: EnumValue
    JUSTIFY_LOW: EnumValue
    THAI_JUSTIFY: EnumValue

WD_ALIGN_PARAGRAPH = WD_PARAGRAPH_ALIGNMENT

class WD_BREAK_TYPE:
    COLUMN: int
    LINE: int
    LINE_CLEAR_LEFT: int
    LINE_CLEAR_RIGHT: int
    LINE_CLEAR_ALL: int  # added for consistency, not in MS version
    PAGE: int
    SECTION_CONTINUOUS: int
    SECTION_EVEN_PAGE: int
    SECTION_NEXT_PAGE: int
    SECTION_ODD_PAGE: int
    TEXT_WRAPPING: int

class WD_COLOR_INDEX(XmlEnumeration):
    AUTO: EnumValue
    BLACK: EnumValue
    BLUE: EnumValue
    BRIGHT_GREEN: EnumValue
    DARK_BLUE: EnumValue
    DARK_RED: EnumValue
    DARK_YELLOW: EnumValue
    GRAY_25: EnumValue
    GRAY_50: EnumValue
    GREEN: EnumValue
    PINK: EnumValue
    RED: EnumValue
    TEAL: EnumValue
    TURQUOISE: EnumValue
    VIOLET: EnumValue
    WHITE: EnumValue
    YELLOW: EnumValue

WD_COLOR = WD_COLOR_INDEX

class WD_LINE_SPACING(XmlEnumeration):
    ONE_POINT_FIVE: EnumValue
    AT_LEAST: EnumValue
    DOUBLE: EnumValue
    EXACTLY: EnumValue
    MULTIPLE: EnumValue
    SINGLE: EnumValue

class WD_TAB_ALIGNMENT(XmlEnumeration):
    LEFT: EnumValue
    CENTER: EnumValue
    RIGHT: EnumValue
    DECIMAL: EnumValue
    BAR: EnumValue
    LIST: EnumValue
    CLEAR: EnumValue
    END: EnumValue
    NUM: EnumValue
    START: EnumValue

class WD_TAB_LEADER(XmlEnumeration):
    SPACES: EnumValue
    DOTS: EnumValue
    DASHES: EnumValue
    LINES: EnumValue
    HEAVY: EnumValue
    MIDDLE_DOT: EnumValue

class WD_UNDERLINE(XmlEnumeration):
    NONE: EnumValue
    SINGLE: EnumValue
    WORDS: EnumValue
    DOUBLE: EnumValue
    DOTTED: EnumValue
    THICK: EnumValue
    DASH: EnumValue
    DOT_DASH: EnumValue
    DOT_DOT_DASH: EnumValue
    WAVY: EnumValue
    DOTTED_HEAVY: EnumValue
    DASH_HEAVY: EnumValue
    DOT_DASH_HEAVY: EnumValue
    DOT_DOT_DASH_HEAVY: EnumValue
    WAVY_HEAVY: EnumValue
    DASH_LONG: EnumValue
    WAVY_DOUBLE: EnumValue
    DASH_LONG_HEAVY: EnumValue
