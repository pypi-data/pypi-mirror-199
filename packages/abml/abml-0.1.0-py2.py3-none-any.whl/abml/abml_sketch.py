import abml_helpers
from abml.abml_dataclass import Abml_Registry
from numpy import array


@Abml_Registry.register("sketch")
class Abml_Sketch:
    def __init__(self, model, **kwargs):
        self.model = model
        self.type = kwargs.pop("cmd", "rect")
        self.kwargs = kwargs

        self._sketch_reg = {
            "rect": self._create_sketch_rect,
            "line": self._create_sketch_line,
            "pline": self._create_sketch_pline,
            "circle": self._create_sketch_circle,
            "ellipse": self._create_sketch_ellipse,
            "arc_center_2points": self._create_sketch_arc_c2p,
            "arc_3points": self._create_sketch_arc_3p,
            "autotrim": self._autotrim,
        }

        self.create()

    def create(self):
        self.model.m.ConstrainedSketch(name="__profile__", sheetSize=200.0)
        self._sketch_reg.get(self.type, self._create_sketch_rect)(**self.kwargs)

    def _create_sketch_rect(self, p1, p2):
        s = self.model.m.sketches["__profile__"]
        s.rectangle(point1=p1, point2=p2)

    def _create_sketch_line(self, p1, p2):
        s = self.model.m.sketches["__profile__"]
        s.Line(point1=p1, point2=p2)

    def _create_sketch_pline(self, points):
        s = self.model.m.sketches["__profile__"]
        lines = create_lines_from_points(array(points))
        for line in lines:
            s.Line(point1=line[0], point2=line[1])

    def _create_sketch_circle(self, center, r):
        s = self.model.m.sketches["__profile__"]
        s.CircleByCenterPerimeter(center=center, point1=r)

    def _create_sketch_ellipse(self, center, r1, r2):
        s = self.model.m.sketches["__profile__"]
        s.EllipseByCenterPerimeter(center=center, axisPoint1=r1, axisPoint2=r2)

    def _create_sketch_arc_c2p(self, center, p1, p2, **kwargs):
        s = self.model.m.sketches["__profile__"]

        direction = kwargs.get("direction", "ccw")

        direction_reg = {
            "ccw": "COUNTERCLOCKWISE",
            "counterclockwise": "COUNTERCLOCKWISE",
            "cw": "COUNTERCLOCKWISE",
            "clockwise": "COUNTERCLOCKWISE",
        }

        s.ArcByCenterEnds(center=center, point1=p1, point2=p2, direction=direction_reg[direction.lower()])

    def _create_sketch_arc_3p(self, p1, p2, p3):
        s = self.model.m.sketches["__profile__"]

        s.Arc3Points(point1=p1, point2=p2, point3=p3)

    def _autotrim(self, p1):
        s = self.model.m.sketches["__profile__"]

        geometries = self._point_on_geometry(p1)

        for geometry in geometries:
            s.autoTrimCurve(curve1=geometry, point1=p1, parameter1=None)  # noqq

    def _point_on_geometry(self, p1):
        s = self.model.m.sketches["__profile__"]
        geometries = s.geometry

        geometry_list = []
        for geometry in geometries:  # noqq
            vp1 = geometry.getVertices()[0]
            vp2 = geometry.getVertices()[1]

            if self._point_on_line(p1, vp1, vp2):
                geometry_list.append(geometry)
        return geometry_list

    def _point_on_line(self, p1, vp1, vp2):
        dxc = p1[0] - vp1[0]
        dyc = p1[1] - vp1[1]

        dxl = vp2[0] - vp1[0]
        dyl = vp2[1] - vp1[1]

        cross = dxc * dyl - dyc * dxl

        if cross == 0:
            return True
        return False


def create_lines_from_points(points, lines=[]):
    if len(points) == 0:
        return lines

    if len(lines) == 0:
        if len(points) == 1:
            raise ValueError("Cannot create line from one point")
        return create_lines_from_points(points[2:], [(points[0], points[1])])
    return create_lines_from_points(points[1:], lines + [(lines[-1][1], points[0])])
