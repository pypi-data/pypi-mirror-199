#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   document.pyi
# @Created At:  2023-03-20 14:32:58
# @Modified At: 2023-03-20 18:49:00
# @Modified By: thepoy

from typing import BinaryIO
from pathlib import Path
from lxml.etree import ElementBase as Element
from docx.blkcntnr import BlockItemContainer
from docx.opc.part import Part
from docx.oxml.document import CT_Document
from docx.parts.document import DocumentPart
from docx.shared import ElementProxy, Emu
from docx.text.paragraph import Paragraph
from docx.shape import InlineShape, InlineShapes
from docx.enum.section import WD_SECTION_START as WD_SECTION
from docx.section import Section, Sections
from docx.table import Table
from docx.opc.parts.coreprops import CoreProperties
from docx.settings import Settings
from docx.styles.style import BaseStyle
from docx.styles.styles import Styles
from docx.table import Table

StrPath = Path | str

class Document(ElementProxy):
    _element: CT_Document
    _part: DocumentPart

    def __init__(self, element: Element, part: Part) -> None: ...
    def add_heading(self, text: str = ..., level: int = ...) -> Paragraph: ...
    def add_page_break(self) -> Paragraph: ...
    def add_paragraph(
        self, text: str = ..., style: BaseStyle | None = ...
    ) -> Paragraph: ...
    def add_picture(
        self,
        image_path_or_stream: StrPath | BinaryIO,
        width: int = ...,
        height: int = ...,
    ) -> InlineShape: ...
    def add_section(self, start_type: WD_SECTION = ...) -> Section: ...
    def add_table(
        self, rows: int, cols: int, style: BaseStyle | None = ...
    ) -> Table: ...
    @property
    def core_properties(self) -> CoreProperties: ...
    @property
    def inline_shapes(self) -> InlineShapes: ...
    @property
    def paragraphs(self) -> list[Paragraph]: ...
    @property
    def part(self) -> Part: ...
    def save(self, path_or_stream: StrPath | BinaryIO) -> None: ...
    @property
    def sections(self) -> Sections: ...
    @property
    def settings(self) -> Settings: ...
    @property
    def styles(self) -> Styles: ...
    @property
    def tables(self) -> list[Table]: ...
    @property
    def _block_width(self) -> Emu: ...
    @property
    def _body(self) -> _Body: ...

class _Body(BlockItemContainer): ...
