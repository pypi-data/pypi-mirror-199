from bsb import config
from bsb.config import types, compose_nodes
from bsb.simulation.device import DeviceModel
from bsb.simulation.targetting import CellTargetting
from .connection import NestConnectionSettings


@config.dynamic(attr_name="device", auto_classmap=True, default="custom")
class NestDevice(compose_nodes(NestConnectionSettings, DeviceModel)):
    pass


@config.node
class ExtNestDevice(NestDevice, classmap_entry="custom"):
    nest_model = config.attr(type=str, required=True)
    targetting = config.attr(type=CellTargetting)
    parameters = config.catch_all(type=types.any_())
