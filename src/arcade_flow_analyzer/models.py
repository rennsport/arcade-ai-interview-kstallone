"""
Arcade Flow pydantic models

Only verifies the data used in project analysis.

Most fields are optional as they are not always present in the data.

TODO: Add more fields as project expands.
Current fields are thought to be enough for basic analysis
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Timestamp(BaseModel):
    seconds: int = Field(alias="_seconds")
    nanoseconds: int = Field(alias="_nanoseconds")


class CapturedEvent(BaseModel):
    type: str
    timeMs: Optional[int] = None
    startTimeMs: Optional[int] = None
    endTimeMs: Optional[int] = None
    clickId: Optional[str] = None
    frameX: Optional[float] = None
    frameY: Optional[float] = None


class ClickContext(BaseModel):
    text: Optional[str] = None
    elementType: Optional[str] = None


class PageContext(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None


class Hotspot(BaseModel):
    id: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    label: Optional[str] = None
    style: Optional[str] = None
    defaultOpen: Optional[bool] = None
    textColor: Optional[str] = None
    bgColor: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None


class Step(BaseModel):
    id: Optional[str] = None
    type: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    clickContext: Optional[ClickContext] = None
    pageContext: Optional[PageContext] = None
    hotspots: Optional[List[Hotspot]] = None


class FlowData(BaseModel):
    name: str
    description: str
    createdBy: str
    teamId: str
    useCase: str
    hasUsedAI: bool
    schemaVersion: str
    status: int
    created: Timestamp
    capturedEvents: List[CapturedEvent]
    steps: List[Step]

    class Config:
        populate_by_name = True
        validate_assignment = True
