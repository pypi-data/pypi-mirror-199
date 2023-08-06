from abml_dataclass import Abml_Registry, to_object_key_based_type
from abaqusConstants import UNIFORM, ISOTROPIC


@Abml_Registry.register("materials")
class Abml_Material:
    """
    A class representing a material in an Abaqus/Standard simulation.

    Parameters
    ----------
    model : AbaqusModel
        The Abaqus model to which the material belongs.
    name : str
        The name of the material.
    behaviors : dict
        A dictionary of material behaviors, where the keys are the behavior names
        and the values are the corresponding behavior parameters.
    description : str, optional
        A description of the material.
    **kwargs
        Additional keyword arguments to be passed to the Abaqus API.

    Attributes
    ----------
    model : AbaqusModel
        The Abaqus model to which the material belongs.
    description : str
        A description of the material.
    name : str
        The name of the material.
    behaviors : dict
        A dictionary of material behaviors, where the keys are the behavior names
        and the values are the corresponding behavior parameters.

    Methods
    -------
    create()
        Creates the material in the Abaqus model.

    Notes
    -----
    This class is a wrapper around the Abaqus/Standard API for creating and managing
    materials in a finite element simulation. It provides a more user-friendly
    interface for defining material properties and behaviors.

    Examples
    --------
    # python
    >>> model = AbaqusModel()
    >>> behaviors = {"elastic": {"youngs_modulus": 100e9, "poissons_ratio": 0.3}}
    >>> material = Abml_Material(model, "steel", behaviors, "steel")
    >>> material.create()

    .. code-block:: yaml

        key1: value1
        key2: value2
        key3:
            - item1
            - item2
    """

    def __init__(self, model, name, behaviors, description="", **kwargs):  # noqa
        self.model = model
        self.description = description
        self.name = name
        self.create()
        self.behaviors = to_object_key_based_type(behaviors, material=self)

    def create(self):
        self.model.m.Material(name=self.name, description=self.description)


@Abml_Registry.register("density")
class Abml_Density:
    def __init__(self, density, material, distribution="uniform"):
        self.material = material
        self.distribution = distribution
        self.density = float(density)

        self.create()

    def create(self):
        distribution_type = {"uniform": UNIFORM}
        kwargs = {"table": ((self.density,),), "distributionType": distribution_type[self.distribution]}
        self.material.model.m.materials[self.material.name].Density(**kwargs)


@Abml_Registry.register("elastic")
class Abml_Elastic:
    def __init__(self, E, nu, material, type="isotropic"):  # noqa
        self.material = material
        self.E = float(E)
        self.nu = float(nu)
        self.type = type
        self.types_map = {
            "isotropic": ISOTROPIC,
        }

        self.elastic_map = {"isotropic": self.isotrtopic}

        self.create()

    def create(self):
        self.elastic_map[self.type]()

    def isotrtopic(self):
        kwargs = {"table": ((self.E, self.nu),), "type": self.types_map[self.type]}
        self.material.model.m.materials[self.material.name].Elastic(**kwargs)
