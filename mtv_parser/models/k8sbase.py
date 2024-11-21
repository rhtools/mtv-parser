from pydantic import UUID4, Field

from .base import ParserBaseModel
from .metadata import MetaData


class K8SRef(ParserBaseModel):
    generation: int | None = Field(default=None)
    name: str
    namespace: str | None = Field(kw_only=True, default=None)
    uid: UUID4 | None = Field(default=None)


class K8SBaseModel(ParserBaseModel):
    api_version: str
    kind: str
    metadata: MetaData
