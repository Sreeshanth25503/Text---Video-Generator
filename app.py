# -*- coding: utf-8 -*-
"""
HuggingFace Spaces entry point.
Wraps web_interface.py and launches with HF Spaces defaults.
"""

from web_interface import build_ui

if __name__ == "__main__":
    demo, theme, css = build_ui()
    demo.launch(theme=theme, css=css)   # HF Spaces handles port/host
