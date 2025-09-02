"""
pure-visual-grounding package

A package for processing PDFs with vision-based language models.
Specialized for technical document OCR operations using LLMs.
"""

from .core import process_pdf_with_vision

__version__ = "1.0.6"
__author__ = "Hamid Khalid"
__email__ = "hamid.khalid@uni-saarland.de"

__all__ = ["process_pdf_with_vision"]