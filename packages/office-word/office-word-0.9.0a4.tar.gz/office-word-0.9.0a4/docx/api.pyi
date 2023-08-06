#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   api.pyi
# @Created At:  2023-03-20 14:08:26
# @Modified At: 2023-03-20 14:31:40
# @Modified By: thepoy

from pathlib import Path
from docx.document import Document as DocumentClass

StrPath = Path | str

def new_document(docx: StrPath | None = None) -> DocumentClass: ...
def Document(docx: StrPath | None = None) -> DocumentClass: ...
def _default_docx_path() -> Path: ...
