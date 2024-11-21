from typing import Self

from pydantic import Field

from ..base import K8SBaseModel
from .plan import Plan


class PlanList(K8SBaseModel):
    kind: str = Field(pattern=r"^(Plan)?List$")
    api_version: str = Field(pattern=r"^v1$")
    items: list[Plan]

    @property
    def successful_migrations(self: Self) -> list[Plan]:
        return [plan for plan in self.items if plan.duration and plan.succeeded]

    @property
    def failed_migrations(self: Self) -> list[Plan]:
        return [plan for plan in self.items if plan.duration and not plan.succeeded]
