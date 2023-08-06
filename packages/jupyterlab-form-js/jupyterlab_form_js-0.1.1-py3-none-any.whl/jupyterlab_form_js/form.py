#!/usr/bin/env python

# Copyright (c) Asko Soukka.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import CallbackDispatcher
from ipywidgets import DOMWidget
from traitlets import Unicode
from traitlets import Dict
from ._frontend import module_name, module_version


class FormJSWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('FormJSViewerModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('FormJSView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    schema = Dict().tag(sync=True)
    data = Dict().tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._submit_handlers = CallbackDispatcher()
        self.on_msg(self._handle_form_msg)

    def on_submit(self, callback, remove=False):
        self._submit_handlers.register_callback(callback, remove=remove)

    def submit(self, data, errors):
        self._submit_handlers(self, data, errors)

    def _handle_form_msg(self, _, content, buffers):
        if content.get("event", "") == "submit":
            self.submit(
                data=content.get("data", "{}"),
                errors=content.get("errors", "{}"),
            )
