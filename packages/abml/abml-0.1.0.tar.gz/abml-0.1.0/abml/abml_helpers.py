from abaqus import mdb
import sys
import os
import re


class IterReg(type):
    # Register of all objects for iteration
    def __iter__(cls):
        return iter(cls._reg.values())


class Abml_Helpers(object):
    @classmethod
    def map_function(cls, key):
        def decorator(func):
            cls.map[key] = func
            return func

        return decorator

    @classmethod
    def get_boundary_rect(cls, sketch, depth, orientation):
        p1 = sketch.kwargs["p1"]
        p2 = sketch.kwargs["p2"]
        x, y, z = abs(p1[0] - p2[0]), abs(p1[1] - p2[1]), depth

        offset = 1e-5
        boundaries = {
            "W": (-offset, 0, 0, 0, y, z),
            "N": (0, -offset, 0, x, 0, z),
            "T": (0, 0, -offset, x, y, 0),
            "top": (0, 0, -offset, x, y, 0),
            "E": (x - offset, 0, 0, x, y, z),
            "S": (0, y - offset, 0, x, y, z),
            "B": (0, 0, z - offset, x, y, z),
            "bot": (0, 0, z - offset, x, y, z),
        }

        return boundaries[orientation]

    @classmethod
    def convert_position_list(cls, position_list):
        if position_list is not None:

            def depth(list_):
                if isinstance(list_, list) and len(list_) != 0:
                    return 1 + max(depth(item) for item in list_)
                return 0

            depth_list = depth(position_list)
            if depth_list == 1 and all(isinstance(x, (int, float)) for x in position_list):
                position_list = [position_list]
            elif depth_list == 0:
                position_list = [position_list]
            return position_list
        return None


def exit_handler():
    for file in os.listdir("."):
        if ".rpy" in file:
            try:
                os.remove(file)
            except WindowsError:
                pass
        if ".rec" in file:
            try:
                os.remove(file)
            except WindowsError:
                pass
        if ".dmp" in file:
            try:
                os.remove(file)
            except WindowsError:
                pass


def cprint(string, prefix="info"):
    print >> sys.__stdout__, prefix + " " + str(string)  # type: ignore # noqa


patter_camel_to_snake = re.compile(r"(?<!^)(?=[A-Z])")
patter_snake_to_camel = re.compile(r"(.*?)_([a-zA-Z])")


def _camel(match):
    return match.group(1) + match.group(2).upper()


def camel_to_snake(name):
    return patter_camel_to_snake.sub("_", name).lower()


def snake_to_camel(name):
    return patter_snake_to_camel.sub(_camel, name, 0)


def get_objects(model_name):
    m = mdb.models[model_name]
    a = m.rootAssembly
    p = m.parts

    return m, a, p
