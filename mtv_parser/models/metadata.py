from typing import Any

from pydantic import Field

from .base import ParserBaseModel


class TemplateMetaData(ParserBaseModel):
    annotations: dict[str, Any] = Field(default_factory=dict)
    labels: dict[str, str] = Field(default_factory=dict)


class MetaData(TemplateMetaData):
    name: str | None = Field(kw_only=True, default=None)
    namespace: str | None = Field(kw_only=True, default=None)
