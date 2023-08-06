__title__ = 'fastocrtools'
__author__ = 'SpeakerC'
__license__ = 'MIT'
__version__ = '3.0.1'
from .tools import*
from .config import*

__all__ = [
    'ocr',
    'high_accuracy_ocr',
    'Handwritten_ocr',
    'ocr_with_location'
    ]