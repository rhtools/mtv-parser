from ..base import ParserBaseModel
from ..metadata import TemplateMetaData
from .instance import VirtualMachineInstanceSpec


class VirtualMachineInstanceTemplate(ParserBaseModel):
    metadata: TemplateMetaData
    spec: VirtualMachineInstanceSpec
