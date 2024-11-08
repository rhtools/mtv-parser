from typing import Self

from pydantic import Field

from .base import K8SRef, ParserBaseModel
from .status import StatusCondition
from .timed import TimedBaseModel
from .vms import VMStatus


class MigrationHistory(TimedBaseModel):
    conditions: list[StatusCondition]
    migration: K8SRef
    plan: K8SRef


class MigrationStatus(TimedBaseModel):
    history: list[MigrationHistory] = Field(default_factory=list)
    vms: list[VMStatus] = Field(default_factory=list)

    @property
    def succeeded(self: Self) -> bool:
        return all([vm.succeeded for vm in self.vms])


# migration:
#       completed: "2024-07-01T06:29:48Z"
#       history:
#       - conditions:
#         - category: Advisory
#           durable: true
#           lastTransitionTime: "2024-07-01T06:29:48Z"
#           message: The plan execution has FAILED.
#           status: "True"
#           type: Failed
#         map:
#           network:
#             generation: 1
#             name: sat1cdocn00-qz525-network
#             namespace: openshift-mtv
#             uid: 6aa416eb-8eb2-4a04-80ed-e1d60b964c14
#           storage:
#             generation: 1
#             name: sat1cdocn00-qz525-storage
#             namespace: openshift-mtv
#             uid: c69d9578-d5cd-4f51-8890-7c75f0d90bd8
#         migration:
#           generation: 1
#           name: sat1cdocn00-qz525-plan-ps9lr
#           namespace: openshift-mtv
#           uid: 4852dcd6-fe3b-46ba-94d7-c5e2cc67dc13
#         plan:
#           generation: 1
#           name: sat1cdocn00-qz525-plan
#           namespace: openshift-mtv
#           uid: 15fa05dd-89f4-45bb-a3b1-bc9a6e9fb409
#         provider:
#           destination:
#             generation: 1
#             name: host
#             namespace: openshift-mtv
#             uid: 0dbc0450-124a-4df6-baa0-c229553fc316
#           source:
#             generation: 2
#             name: satvcd
#             namespace: openshift-mtv
#             uid: 55091dc0-580d-4da4-87bb-80905706254e
#       started: "2024-07-01T06:26:11Z"
#       vms:
#
