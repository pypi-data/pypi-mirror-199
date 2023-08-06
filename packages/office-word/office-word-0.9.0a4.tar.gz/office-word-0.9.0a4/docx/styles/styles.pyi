#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   styles.pyi
# @Created At:  2023-03-20 18:39:16
# @Modified At: 2023-03-20 18:55:13
# @Modified By: thepoy

from docx.shared import ElementProxy
from docx.styles.style import CharacterStyle, ParagraphStyle, TableStyle, NumberingStyle

StyleType = ParagraphStyle | CharacterStyle | TableStyle | NumberingStyle

class Styles(ElementProxy):
    def __contains__(self, name: str) -> bool: ...
    def __getitem__(self, key: str) -> StyleType: ...
    def __iter__(self) -> StyleType: ...
    def __len__(self) -> int: ...
