#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Asko Soukka.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..form import FormWidget


def test_form_creation_blank():
    w = FormWidget()
    assert w.schema == 'null'
    assert w.data == 'null'
