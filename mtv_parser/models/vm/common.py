from enum import StrEnum

from pydantic import Field

from ..base import ParserBaseModel


class RunStrategy(StrEnum):
    UNKNOWN = ""
    ALWAYS = "Always"
    HALTED = "Halted"
    MANUAL = "Manual"
    RERUNONFAILURE = "RerunOnFailure"
    ONCE = "Once"


class InferFromVolumeFailurePolicy(StrEnum):
    REJECT = "Reject"
    IGNORE = "Ignore"


class RefMatcher(ParserBaseModel):
    name: str | None = Field(default=None)
    kind: str | None = Field(default=None)
    revision_name: str | None = Field(default=None)
    infer_from_volume: str | None = Field(default=None)
    infer_from_volume_failure_policy: InferFromVolumeFailurePolicy = Field(default=InferFromVolumeFailurePolicy.REJECT)
