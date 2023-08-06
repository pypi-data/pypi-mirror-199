import abml_helpers
from abaqusConstants import THREE_D, DEFORMABLE_BODY, XZPLANE  # noqa
from abaqusConstants import XYPLANE, YZPLANE, XZPLANE  # noqa
from abaqusConstants import MIDDLE_SURFACE, FROM_SECTION  # noqa
from regionToolset import Region
from abml_dataclass import Abml_Registry
from abml_dataclass import to_object_option_mode, to_object_key_mode, to_object_cmd_mode
from abml_helpers import Abml_Helpers
from abml_sketch import Abml_Sketch
from numpy import array, abs
from abaqus import mdb


@Abml_Registry.register("parts")
class Abml_Part:
    def __init__(self, name, model, **kwargs):  # noqa
        self.model = model
        self.name = name
        self.create()

        geometry = kwargs.get("geometry")
        if geometry is not None:
            params = {
                "data": geometry,
                "type_": "geometry",
                "part": self,
            }
            self.geometry = to_object_option_mode(**params)

        planes = kwargs.get("planes")
        if planes is not None:
            params = {
                "data": planes,
                "type_": "planes",
                "part": self,
            }
            self.planes = to_object_key_mode(**params)

        partitions = kwargs.get("partitions")
        if partitions is not None:
            params = {
                "data": partitions,
                "type_": "partitions",
                "part": self,
            }
            self.partitions = to_object_cmd_mode(**params)

        surfaces = kwargs.get("surfaces")
        if surfaces is not None:
            params = {
                "data": surfaces,
                "type_": "surfaces",
                "part": self,
            }
            self.surfaces = to_object_key_mode(**params)

        sets = kwargs.get("sets")

        if sets is not None:
            params = {
                "data": sets,
                "type_": "sets",
                "part": self,
            }
            self.sets = to_object_key_mode(**params)

        section_assignments = kwargs.get("section_assignments")
        if section_assignments is not None:
            params = {
                "data": section_assignments,
                "type_": "section_assignments",
                "part": self,
            }
            self.section_assignments = to_object_key_mode(**params)

        mesh = kwargs.get("mesh")
        if mesh is not None:
            params = {
                "data": mesh,
                "type_": "mesh",
                "part": self,
            }

            self.mesh = to_object_cmd_mode(**params)
            self.generate_mesh()

    def create(self):
        self.model.m.Part(dimensionality=THREE_D, name=self.name, type=DEFORMABLE_BODY)

    def get_sequence_from_set_list(self, set_list):
        face_seq = None
        cell_seq = None
        edge_seq = None
        for set_ in set_list:
            seq = self.model.p[self.name].sets[set_].faces
            if face_seq is None:
                face_seq = seq
            else:
                face_seq += seq

            seq = self.model.p[self.name].sets[set_].cells
            if cell_seq is None:
                cell_seq = seq
            else:
                cell_seq += seq

            seq = self.model.p[self.name].sets[set_].edges
            if edge_seq is None:
                edge_seq = seq
            else:
                edge_seq += seq

        kwargs = {
            "faces": face_seq,
            "cells": cell_seq,
            "edges": edge_seq,
        }

        return kwargs

    def generate_mesh(self):
        self.model.p[self.name].generateMesh()


@Abml_Registry.register("geometry")
class Abml_Geometry(Abml_Helpers):
    def __init__(self, type, sketch, part, **kwargs):  # noqa
        self.type = type
        self.part = part
        self.model = part.model

        params = {"data": sketch, "type_": "sketch", "model": self.model}

        self.sketch = to_object_cmd_mode(**params)

        self.kwargs = kwargs
        self.map = {
            ("3d", "deformable", "solid_extrusion"): self._create_solid_extrusion,
        }

        self.create()

    def create(self):
        self.map[("3d", "deformable", self.type)]()

    def _create_solid_extrusion(self):
        if not isinstance(self.kwargs["depth"], (int, float)) or self.kwargs["depth"] == 0.0:
            error_str = "Extrusion depth for part: {} is no int, float or is 0".format(self.part.name)
            raise ValueError(error_str)
        part = self.model.p[self.part.name]
        sketch = self.model.m.sketches["__profile__"]
        part.BaseSolidExtrude(depth=self.kwargs["depth"], sketch=sketch)
        del sketch

        self.aliases = {}

    def get_face_sequence(self, element):
        part = self.model.p[self.part.name]
        element = array([element]).flatten()
        seq = None
        if element.shape == (3,) and isinstance(element[0], (float, int)):  # findAt
            face = part.faces.findAt(element.astype(float))  # noqa
            if face is not None:
                seq = Region(side1Faces=part.faces[face.index : face.index + 1]).side1Faces
        elif element.shape == (6,) and isinstance(element[0], (float, int)):  # getByBoundingBox
            faces = part.faces.getByBoundingBox(*element.astype(float))
            if len(faces) != 0:
                seq = faces
        elif isinstance(element.item(0), str):  # getByBoundingBox str
            if any(item == element.item(0) for item in ["all"]):
                seq = part.faces[:]
            elif any(item == element.item(0) for item in part.surfaces.keys()):
                seq = part.surfaces[element.item(0)].faces
            else:
                boundaries = self.get_boundary_rect(self.sketch[0], self.kwargs["depth"], element.item(0))
                seq = part.faces.getByBoundingBox(*boundaries)

        return seq

    def get_cell_sequence(self, element):
        part = self.model.p[self.part.name]
        element = array([element]).flatten()
        seq = None
        if element.shape == (3,) and isinstance(element[0], (float, int)):  # findAt
            cell = part.cells.findAt(element.astype(float))
            if cell is not None:
                seq = Region(cells=part.cells[cell.index : cell.index + 1]).cells
        elif element.shape == (6,) and isinstance(element[0], (float, int)):  # getByBoundingBox
            cells = part.cells.getByBoundingBox(*element.astype(float))
            if len(cells) != 0:
                seq = cells
        elif isinstance(element.item(0), str):  # getByBoundingBox
            if element.item(0) == "all":
                seq = part.cells[:]
            else:
                boundaries = self.get_boundary_rect(self.sketch[0], self.kwargs["depth"], element.item(0))
                seq = part.cells.getByBoundingBox(*boundaries)
        return seq

    def get_edge_sequence(self, element):
        part = self.model.p[self.part.name]
        element = array([element]).flatten()
        seq = None
        if element.shape == (3,) and isinstance(element[0], (float, int)):  # findAt
            edge = part.edges.findAt(element.astype(float))
            if isinstance(edge, type(None)):
                seq = None
            else:
                seq = Region(edges=part.edges[edge.index : edge.index + 1]).edges
        elif element.shape == (6,) and isinstance(element[0], (float, int)):  # getByBoundingBox
            edges = part.edges.getByBoundingBox(*element.astype(float))
            if len(edges) != 0:
                seq = edges
        elif isinstance(element.item(0), str):  # getByBoundingBox
            if any(item == element.item(0) for item in ["all"]):
                seq = part.edges[:]
            else:
                boundaries = self.get_boundary_rect(self.sketch[0], self.kwargs["depth"], element.item(0))
                seq = part.edges.getByBoundingBox(*boundaries)

        return seq

    def get_set_sequence_edges(self, element):
        return Region(edges=self.model.p[self.part.name].sets[element].edges).edges

    def get_set_sequence_cells(self, element):
        return Region(cells=self.model.p[self.part.name].sets[element].cells).cells

    def get_set_sequence_faces(self, element):
        return Region(side1Faces=self.model.p[self.part.name].sets[element].faces).faces

    def get_sequence_from_list(self, elements, type_):
        sequence_map = {
            "cell": self.get_cell_sequence,
            "face": self.get_face_sequence,
            "edge": self.get_edge_sequence,
            "set_edges": self.get_set_sequence_edges,
            "set_faces": self.get_set_sequence_faces,
            "set_cells": self.get_set_sequence_cells,
        }

        type_seq = None
        for element in elements:
            if len(element) != 0:
                seq = sequence_map[type_](element)
                if type_seq is None:
                    type_seq = seq
                else:
                    type_seq += seq
        return type_seq


@Abml_Registry.register("planes")
class Abml_Plane:
    def __init__(self, name, part, **kwargs):  # noqa
        self.name = name
        self.part = part
        self.model = part.model
        self.kwargs = kwargs

        self._principal_Plane = {"x": YZPLANE, "y": XZPLANE, "z": XYPLANE}
        self.create()

    def create(self):
        part = self.model.p[self.part.name]
        for key, value in self.kwargs.items():
            part.DatumPlaneByPrincipalPlane(offset=value, principalPlane=self._principal_Plane[key])
            part.features.changeKey(fromName="Datum plane-1", toName=self.name)  # noqa


@Abml_Registry.register("partitions")
class Abml_Partition(Abml_Helpers):
    def __init__(self, part, faces=None, edges=None, cells=None, **kwargs):
        self.method = kwargs.get("cmd", "plane")
        self.part = part
        self.model = part.model
        self.faces = self.convert_position_list(faces)
        self.edges = self.convert_position_list(edges)
        self.cells = self.convert_position_list(cells)
        self.kwargs = kwargs
        self.partition_map = {"plane": self.create_face_plane}

        self.create()

    def create(self):
        self.partition_map[self.method]()

    def create_face_plane(self):
        part_ = self.model.p[self.part.name]
        planes = array([self.kwargs.get("planes", [])]).flatten()

        for plane in planes:
            id_ = part_.features[plane].id

            if self.faces is not None:
                face_seq = self.part.geometry.get_sequence_from_list(self.faces, "face")
                if face_seq is not None:
                    try:
                        part_.PartitionFaceByDatumPlane(datumPlane=part_.datums[id_], faces=face_seq)
                    except Exception as e:
                        error_msg = """
                        part_name: {part_name}
                        number of face seq found: {num_face_seq}
                        plane: {plane}

                        {e}
                        """.format(
                            part_name=self.part.name,
                            e=e,
                            num_face_seq=len(face_seq),
                            plane=plane,
                        )
                        raise ValueError(error_msg)

            if self.cells is not None:
                cell_seq = self.part.geometry.get_sequence_from_list(self.cells, "cell")
                if cell_seq is not None:
                    part_.PartitionCellByDatumPlane(datumPlane=part_.datums[id_], cells=cell_seq)

            if self.edges is not None:
                edge_seq = self.part.geometry.get_sequence_from_list(self.edges, "edge")
                if edge_seq is not None:
                    part_.PartitionEdgeByDatumPlane(datumPlane=part_.datums[id_], edges=edge_seq)


@Abml_Registry.register("surfaces")
class Abml_Surface(Abml_Helpers):
    def __init__(self, name, faces, part, **kwargs):
        self.name = name
        self.part = part
        self.model = self.part.model
        self.faces = self.convert_position_list(faces)

        self.create()

    def create(self):
        part = self.model.p[self.part.name]

        face_seq = self.part.geometry.get_sequence_from_list(self.faces, "face")

        try:
            part.Surface(side1Faces=face_seq, name=self.name)
        except Exception as e:
            error_msg = """
            surface_name: {name}
            {e}
            """.format(
                name=self.name,
                e=e,
            )
            raise ValueError(error_msg)


@Abml_Registry.register("sets")
class Abml_Sets(Abml_Helpers):
    def __init__(self, name, part, faces=[], edges=[], cells=[]):
        self.name = name
        self.part = part
        self.model = part.model
        self.faces = self.convert_position_list(faces)
        self.edges = self.convert_position_list(edges)
        self.cells = self.convert_position_list(cells)
        self.create()

    def create(self):
        part = self.model.p[self.part.name]

        kwargs = {}
        face_seq = self.part.geometry.get_sequence_from_list(self.faces, "face")
        if face_seq is not None:
            kwargs["faces"] = face_seq

        cell_seq = self.part.geometry.get_sequence_from_list(self.cells, "cell")
        if cell_seq is not None:
            kwargs["cells"] = cell_seq

        edge_seq = self.part.geometry.get_sequence_from_list(self.edges, "edge")
        if edge_seq is not None:
            kwargs["edges"] = edge_seq

        part.Set(name=self.name, **kwargs)


@Abml_Registry.register("section_assignments")
class Abml_Section_Assignments(Abml_Helpers):
    def __init__(self, name, part, cells=None, sets=None):
        self.name = name
        self.part = part
        self.model = part.model

        self.cells = self.convert_position_list(cells)
        self.sets = self.convert_position_list(sets)
        self.create()

    def create(self):
        cell_seq = self.part.geometry.get_sequence_from_list(self.cells, "cell")
        if self.sets is not None:
            set_seq = self.part.get_sequence_from_set_list(self.sets)["cells"]
            if set_seq is not None:
                cell_seq += set_seq

        kwargs = {
            "sectionName": self.name,
            "offset": 0.0,
            "offsetType": MIDDLE_SURFACE,
            "offsetField": "",
            "thicknessAssignment": FROM_SECTION,
            "region": Region(cells=cell_seq),
        }

        self.model.p[self.part.name].SectionAssignment(**kwargs)
