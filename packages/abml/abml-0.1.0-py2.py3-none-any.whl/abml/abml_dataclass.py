import types
import json
import inspect
from collections import OrderedDict
from collections import defaultdict
import sys
import yaml
from io import open
from abaqus import mdb
from abaqusConstants import STANDARD_EXPLICIT
from abml import abml_helpers
import interaction


class Abml_Registry:
    registry = defaultdict(lambda: OrderedDict)

    @classmethod
    def register(cls, key):
        def decorator(dataclass):
            cls.registry[key] = dataclass
            return dataclass

        return decorator


@Abml_Registry.register("cae")
class Abml_Cae:
    def __init__(self, models, **kwargs):
        self.models = to_object_key_mode(models["models"], type_="models")

    def save_cae(self, filename):
        mdb.saveAs(pathName=filename)


@Abml_Registry.register("models")
class Abml_Model:
    def __init__(self, name, **kwargs):
        self.name = name
        self.create()
        self.m, self.a, self.p = abml_helpers.get_objects(self.name)

        materials_list = [value for key, value in kwargs.items() if "materials" in key]
        for materials in materials_list:
            if materials is not None:
                materials = OrderedDict(sorted(materials.items()))
                self.materials = to_object_key_mode(materials, "materials", model=self)

        sections_list = [value for key, value in kwargs.items() if "sections" in key]
        for sections in sections_list:
            if sections is not None:
                sections = OrderedDict(sorted(sections.items()))
                self.materials = to_object_key_mode(sections, "sections", model=self)

        parts_list = [value for key, value in kwargs.items() if "parts" in key]
        for parts in parts_list:
            if parts is not None:
                parts = OrderedDict(sorted(parts.items()))
                self.parts = to_object_key_mode(parts, "parts", model=self)

        assembly_list = [value for key, value in kwargs.items() if "assembly" in key]
        for assembly in assembly_list:
            if assembly is not None:
                self.assembly = to_object_hierachy_mode(assembly, "assembly", model=self)

        steps_list = [value for key, value in kwargs.items() if "steps" in key]
        for steps in steps_list:
            if steps is not None:
                steps = OrderedDict(sorted(steps.items()))
                self.interaction_props = to_object_key_mode(steps, "steps", model=self)

        interaction_props_list = [value for key, value in kwargs.items() if "interaction_props" in key]
        for interaction_props in interaction_props_list:
            if interaction_props is not None:
                interaction_props = OrderedDict(sorted(interaction_props.items()))
                self.interaction_props = to_object_key_mode(interaction_props, "interaction_properties", model=self)

        interactions_list = [value for key, value in kwargs.items() if "interactions" in key]
        for interactions in interactions_list:
            if interactions is not None:
                interactions = OrderedDict(sorted(interactions.items()))
                self.interactions = to_object_key_mode(interactions, "interactions", model=self)

        constraints_list = [value for key, value in kwargs.items() if "constraints" in key]
        for constraints in constraints_list:
            if constraints is not None:
                constraints = OrderedDict(sorted(constraints.items()))
                self.constraints = to_object_key_mode(constraints, "constraints", model=self)

        bcs_list = [value for key, value in kwargs.items() if "bcs" in key]
        for bcs in bcs_list:
            if bcs is not None:
                bcs = OrderedDict(sorted(bcs.items()))
                self.bcs = to_object_key_mode(bcs, "bcs", model=self)

        loads_list = [value for key, value in kwargs.items() if "loads" in key]
        for loads in loads_list:
            if loads is not None:
                loads = OrderedDict(sorted(loads.items()))
                self.loads = to_object_key_mode(loads, "loads", model=self)

        jobs_list = [value for key, value in kwargs.items() if "jobs" in key]
        for jobs in jobs_list:
            if jobs is not None:
                jobs = OrderedDict(sorted(jobs.items()))
                self.jobs = to_object_key_mode(jobs, "jobs", model=self)

    def create(self):
        mdb.Model(modelType=STANDARD_EXPLICIT, name=self.name)

        if "Model-1" in mdb.models.keys():
            del mdb.models["Model-1"]


def data_to_object(data, type_="models", key_based=True, **kwargs):
    if data is not None:
        object_ = {}
        if isinstance(data, dict):
            object_ = {}
            if key_based:
                for key, value in data.items():
                    if isinstance(value, dict):
                        value.update(kwargs)
                        object_[key] = Abml_Registry.registry[type_](name=key, **value)
                    elif isinstance(value, (list)):
                        object_[key] = Abml_Registry.registry[type_](name=key, *value)
            else:
                data.update(kwargs)
                object_ = Abml_Registry.registry[type_](**data)
        elif isinstance(data, list):
            object_ = []
            for value in data:
                value.update(kwargs)
                object_.append(Abml_Registry.registry[type_](**value))

        return object_


def to_object_key_mode(data, type_, **kwargs):
    object_ = {}
    for key, value in data.items():
        value.update(kwargs)
        object_[key] = Abml_Registry.registry[type_](name=key, **value)

    return object_


def to_object_option_mode(data, type_, **kwargs):
    data.update(kwargs)
    object_ = Abml_Registry.registry[type_](**data)

    return object_


def to_object_key_based_type(data, **kwargs):
    object_ = {}
    for key, value in data.items():
        value.update(kwargs)
        object_[key] = Abml_Registry.registry[key](**value)

    return object_


def to_object_cmd_mode(data, type_, **kwargs):
    object_ = []
    for cmd in data:
        value = cmd.values()[0]
        key = cmd.keys()[0]
        value.update(kwargs)
        object_.append(Abml_Registry.registry[type_](cmd=key, **value))

    return object_


def to_object_hierachy_mode(data, type_, **kwargs):
    # object_ = []
    # data.update(kwargs)
    # object_.append(Abml_Registry.registry[type_](**data))

    data.update(kwargs)
    object_ = Abml_Registry.registry[type_](**data)

    return object_
