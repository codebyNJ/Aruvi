from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class KolamType(Enum):
    GEOMETRIC = "geometric"
    IYAL = "iyal"
    RANGOLI = "rangoli"
    KAVI = "kavi"
    TRADITIONAL_1D = "traditional_1d"

@dataclass
class Point:
    x: float
    y: float

@dataclass
class CurvePoint:
    x: float
    y: float
    control_x: Optional[float] = None
    control_y: Optional[float] = None

@dataclass
class KolamCurvePattern:
    id: int
    points: List[CurvePoint]
    has_down_connection: bool
    has_right_connection: bool

@dataclass
class GridCell:
    row: int
    col: int
    pattern_id: int
    dot_center: Point

@dataclass
class KolamGrid:
    size: int
    cells: List[List[GridCell]]
    cell_spacing: float

@dataclass
class Line:
    id: str
    start: Point
    end: Point
    stroke_width: Optional[float] = None
    color: Optional[str] = None
    curve_points: Optional[List[CurvePoint]] = None

@dataclass
class Dot:
    id: str
    center: Point
    radius: Optional[float] = None
    color: Optional[str] = None
    filled: Optional[bool] = None

@dataclass
class KolamPattern:
    id: str
    name: str
    kolam_type: KolamType
    grid: Optional[KolamGrid]
    curves: List[Line]
    dots: List[Dot]
    symmetry_type: str
    dimensions: Dict[str, float]
    created: datetime
    modified: datetime
    colors: Optional[Dict[str, str]] = None
    mathematical_params: Optional[Dict[str, Any]] = None

@dataclass
class SVGOptions:
    background: Optional[str] = None
    brush: Optional[str] = None
    padding: Optional[float] = None
