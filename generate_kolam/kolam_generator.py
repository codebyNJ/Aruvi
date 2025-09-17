import random
from typing import List, Dict, Any
from datetime import datetime
from models import KolamPattern, KolamGrid, GridCell, Dot, Line, Point, CurvePoint, KolamType
from kolam_patterns import KOLAM_CURVE_PATTERNS

class KolamGenerator:
    CELL_SPACING = 60.0
    
    # Core constants for kolam generation
    pt_dn = [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1]
    pt_rt = [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1]
    
    mate_pt_dn = {
        1: [2, 3, 5, 6, 9, 10, 12],
        2: [4, 7, 8, 11, 13, 14, 15, 16]
    }
    
    mate_pt_rt = {
        1: [2, 3, 4, 6, 7, 11, 13],
        2: [5, 8, 9, 10, 12, 14, 15, 16]
    }
    
    h_inv = [1, 2, 5, 4, 3, 9, 8, 7, 6, 10, 11, 12, 15, 14, 13, 16]
    v_inv = [1, 4, 3, 2, 5, 7, 6, 9, 8, 10, 11, 14, 13, 12, 15, 16]
    
    @classmethod
    def find_self_inverse(cls, inv: List[int]) -> List[int]:
        """Find self-inverse elements"""
        result = []
        for i in range(len(inv)):
            if inv[i] == i + 1:  # 1-indexed array handling
                result.append(i + 1)
        return result
    
    @classmethod
    def intersect(cls, arr1: List[int], arr2: List[int]) -> List[int]:
        """Array intersection function"""
        return [x for x in arr1 if x in arr2]
    
    @classmethod
    def random_choice(cls, arr: List[int]) -> int:
        """Random array element selector"""
        if not arr:
            return 1  # Default fallback
        return random.choice(arr)
    
    @classmethod
    def ones(cls, size: int) -> List[List[int]]:
        """Create matrix filled with ones"""
        return [[1 for _ in range(size)] for _ in range(size)]
    
    @classmethod
    def propose_kolam_1d(cls, size_of_kolam: int) -> List[List[int]]:
        """Literal translation of propose_kolam1D.m"""
        odd = (size_of_kolam % 2) != 0
        
        if odd:
            hp = (size_of_kolam - 1) // 2
        else:
            hp = size_of_kolam // 2
        
        Mat = cls.ones(hp + 2)  # Need hp+2 for the algorithm
        
        # Grid iteration
        for i in range(1, hp + 1):
            for j in range(1, hp + 1):
                pt_dn_value = cls.pt_dn[Mat[i - 1][j] - 1]  # Convert to 0-indexed
                valid_by_up = cls.mate_pt_dn[pt_dn_value + 1]
                
                pt_rt_value = cls.pt_rt[Mat[i][j - 1] - 1]  # Convert to 0-indexed
                valid_by_lt = cls.mate_pt_rt[pt_rt_value + 1]
                
                valids = cls.intersect(valid_by_up, valid_by_lt)
                
                try:
                    v = cls.random_choice(valids)
                    Mat[i][j] = v
                except:
                    Mat[i][j] = 1
        
        # Set boundary values
        Mat[hp + 1][0] = 1
        Mat[0][hp + 1] = 1
        
        # Column iteration
        for j in range(1, hp + 1):
            pt_dn_value = cls.pt_dn[Mat[hp][j] - 1]
            valid_by_up = cls.mate_pt_dn[pt_dn_value + 1]
            
            pt_rt_value = cls.pt_rt[Mat[hp + 1][j - 1] - 1]
            valid_by_lt = cls.mate_pt_rt[pt_rt_value + 1]
            
            valids = cls.intersect(valids, cls.find_self_inverse(cls.v_inv))
            
            try:
                v = cls.random_choice(valids)
                Mat[hp + 1][j] = v
            except:
                Mat[hp + 1][j] = 1
        
        # Row iteration
        for i in range(1, hp + 1):
            pt_dn_value = cls.pt_dn[Mat[i - 1][hp + 1] - 1]
            valid_by_up = cls.mate_pt_dn[pt_dn_value + 1]
            
            pt_rt_value = cls.pt_rt[Mat[i][hp] - 1]
            valid_by_lt = cls.mate_pt_rt[pt_rt_value + 1]
            
            valids = cls.intersect(valid_by_up, valid_by_lt)
            valids = cls.intersect(valids, cls.find_self_inverse(cls.h_inv))
            
            try:
                v = cls.random_choice(valids)
                Mat[i][hp + 1] = v
            except:
                Mat[i][hp + 1] = 1
        
        # Corner element
        pt_dn_value = cls.pt_dn[Mat[hp][hp + 1] - 1]
        valid_by_up = cls.mate_pt_dn[pt_dn_value + 1]
        
        pt_rt_value = cls.pt_rt[Mat[hp + 1][hp] - 1]
        valid_by_lt = cls.mate_pt_rt[pt_rt_value + 1]
        
        valids = cls.intersect(valid_by_up, valid_by_lt)
        valids = cls.intersect(valids, cls.find_self_inverse(cls.h_inv))
        valids = cls.intersect(valids, cls.find_self_inverse(cls.v_inv))
        
        try:
            v = cls.random_choice(valids)
            Mat[hp + 1][hp + 1] = v
        except:
            Mat[hp + 1][hp + 1] = 1
        
        # Extract the main pattern
        Mat1 = [[Mat[i][j] for j in range(1, hp + 1)] for i in range(1, hp + 1)]
        
        # Create symmetric patterns
        Mat3 = [[cls.v_inv[Mat1[hp - 1 - i][j] - 1] for j in range(hp)] for i in range(hp)]
        Mat2 = [[cls.h_inv[Mat1[i][hp - 1 - j] - 1] for j in range(hp)] for i in range(hp)]
        Mat4 = [[cls.v_inv[Mat2[hp - 1 - i][j] - 1] for j in range(hp)] for i in range(hp)]
        
        # Final assembly based on odd/even
        if odd:
            size = 2 * hp + 1
            M = [[1 for _ in range(size)] for _ in range(size)]
            
            # Copy Mat1
            for i in range(hp):
                for j in range(hp):
                    M[i][j] = Mat1[i][j]
            
            # Column vector from Mat
            for i in range(hp):
                M[i][hp] = Mat[i + 1][hp + 1]
            
            # Copy Mat2
            for i in range(hp):
                for j in range(hp):
                    M[i][hp + 1 + j] = Mat2[i][j]
            
            # Row vector from Mat
            for j in range(hp + 1):
                M[hp][j] = Mat[hp + 1][j + 1]
            
            # Transformed row vector
            for j in range(hp, 0, -1):
                M[hp][hp + (hp - j + 1)] = cls.h_inv[Mat[hp + 1][j] - 1]
            
            # Copy Mat3
            for i in range(hp):
                for j in range(hp):
                    M[hp + 1 + i][j] = Mat3[i][j]
            
            # Transformed column vector
            for i in range(hp, 0, -1):
                M[hp + (hp - i + 1)][hp] = cls.v_inv[Mat[i][hp + 1] - 1]
            
            # Copy Mat4
            for i in range(hp):
                for j in range(hp):
                    M[hp + 1 + i][hp + 1 + j] = Mat4[i][j]
        else:
            size = 2 * hp
            M = [[1 for _ in range(size)] for _ in range(size)]
            
            # Copy all four quadrants
            for i in range(hp):
                for j in range(hp):
                    M[i][j] = Mat1[i][j]
                    M[i][hp + j] = Mat2[i][j]
                    M[hp + i][j] = Mat3[i][j]
                    M[hp + i][hp + j] = Mat4[i][j]
        
        return M
    
    @classmethod
    def draw_kolam(cls, M: List[List[int]], kolam_type: KolamType) -> KolamPattern:
        """Convert matrix to visual kolam pattern"""
        m, n = len(M), len(M[0])
        
        # Flip vertically
        flipped_m = [M[m - 1 - i][:] for i in range(m)]
        
        dots = []
        curves = []
        
        for i in range(m):
            for j in range(n):
                if flipped_m[i][j] > 0:
                    # Add dot at grid position
                    dots.append(Dot(
                        id=f"dot-{i}-{j}",
                        center=Point(
                            x=(j + 1) * cls.CELL_SPACING,
                            y=(i + 1) * cls.CELL_SPACING
                        ),
                        radius=3.0,
                        color="#ffffff",
                        filled=True
                    ))
                    
                    # Add curve pattern
                    pattern_index = flipped_m[i][j] - 1
                    if 0 <= pattern_index < len(KOLAM_CURVE_PATTERNS):
                        pattern = KOLAM_CURVE_PATTERNS[pattern_index]
                        
                        # Calculate the base position for this pattern
                        base_x = (j + 0.5) * cls.CELL_SPACING
                        base_y = (i + 0.5) * cls.CELL_SPACING
                        
                        # Scale factor to fit pattern within cell
                        scale = cls.CELL_SPACING * 0.4  # Slightly smaller than cell to prevent overlap
                        
                        curve_points = [
                            CurvePoint(
                                x=base_x + point.x * scale,
                                y=base_y + point.y * scale,
                                control_x=base_x + point.control_x * scale if point.control_x else None,
                                control_y=base_y + point.control_y * scale if point.control_y else None
                            )
                            for point in pattern.points
                        ]
                        
                        curves.append(Line(
                            id=f"curve-{i}-{j}",
                            start=curve_points[0],
                            end=curve_points[-1],
                            curve_points=curve_points,
                            stroke_width=2.0,  # Slightly thicker for better visibility
                            color="#ffffff"
                        ))
        
        # Create grid structure
        grid_cells = []
        for i in range(m):
            row = []
            for j in range(n):
                row.append(GridCell(
                    row=i,
                    col=j,
                    pattern_id=flipped_m[i][j],
                    dot_center=Point(
                        x=(j + 1) * cls.CELL_SPACING,
                        y=(i + 1) * cls.CELL_SPACING
                    )
                ))
            grid_cells.append(row)
        
        grid = KolamGrid(
            size=max(m, n),
            cells=grid_cells,
            cell_spacing=cls.CELL_SPACING
        )
        
        return KolamPattern(
            id=f"kolam-{m}x{n}",
            name=f"Kolam {m}×{n}",
            kolam_type=kolam_type,  
            grid=grid,
            curves=curves,
            dots=dots,
            symmetry_type="1D",
            dimensions={
                "width": (n + 1) * cls.CELL_SPACING,
                "height": (m + 1) * cls.CELL_SPACING
            },
            created=datetime.now(),
            modified=datetime.now(),
            colors={"primary": "#ffffff"}  
        )
    
    @classmethod
    def generate_kolam_1d(cls, size: int) -> KolamPattern:
        """Main entry point - generate kolam pattern using algorithm"""
        print(f"🎨 Generating 1D Kolam of size {size}")
        
        matrix = cls.propose_kolam_1d(size)
        print(f"📊 Generated matrix: {len(matrix)}x{len(matrix[0])}")
        
        pattern = cls.draw_kolam(matrix, KolamType.TRADITIONAL_1D)
        print(f"✅ Created kolam with {len(pattern.dots)} dots and {len(pattern.curves)} curves")
        
        return pattern
