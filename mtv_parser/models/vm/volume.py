from ..base import ParserBaseModel
from ..metadata import TemplateMetaData


class DataVolumeSpec(ParserBaseModel):
    pass


class DataVolumeTemplate(ParserBaseModel):
    metadata: TemplateMetaData
    spec: DataVolumeSpec
