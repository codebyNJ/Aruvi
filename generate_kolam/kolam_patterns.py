import json
from typing import List
from models import KolamCurvePattern, CurvePoint

def load_kolam_patterns() -> List[KolamCurvePattern]:
    """Load kolam curve patterns from JSON data file"""
    with open('data/kolamPatternsData.json', 'r') as f:
        data = json.load(f)
    
    patterns = []
    for pattern_data in data['patterns']:
        curve_points = [
            CurvePoint(
                x=point['x'],
                y=point['y'],
                control_x=point.get('controlX'),
                control_y=point.get('controlY')
            )
            for point in pattern_data['points']
        ]
        
        pattern = KolamCurvePattern(
            id=pattern_data['id'],
            points=curve_points,
            has_down_connection=pattern_data['hasDownConnection'],
            has_right_connection=pattern_data['hasRightConnection']
        )
        patterns.append(pattern)
    
    return patterns

# Load patterns at module level
KOLAM_CURVE_PATTERNS = load_kolam_patterns()
