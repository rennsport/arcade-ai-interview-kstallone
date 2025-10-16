"""
Arcade Flow Analyzer

A Python package for analyzing Arcade flow data and generating reports.
"""

from .models import FlowData, CapturedEvent, Step, Timestamp, ClickContext, PageContext
from .extractors import process_flow, save_to_csv, basic_extractor_main
from .analysis import preprocess_csv, summarize_actions
from .visualization import generate_flow_image

__version__ = "0.1.0"
__all__ = [
    "FlowData",
    "CapturedEvent", 
    "Step",
    "Timestamp",
    "ClickContext",
    "PageContext",
    "process_flow",
    "save_to_csv",
    "basic_extractor_main",
    "preprocess_csv",
    "summarize_actions",
    "generate_flow_image"
]
