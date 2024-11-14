from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from pydantic import ValidationError

from mtv_parser.models.vms import Phase as VMPhase

from . import utils

TEST_SUCCESS_CONDITION = (
    "- status: true\n"
    "  type: Succeeded\n"
    "  lastTransitionTime: 2024-04-10T17:33:25Z\n"
    "  message: ''\n"
    "  category: Advisory"
)

TEST_FAILED_CONDITION = (
    "- status: true\n"
    "  type: Failed\n"
    "  lastTransitionTime: 2024-04-10T17:33:25Z\n"
    "  message: ''\n"
    "  category: Advisory"
)

TEST_MODEL_YAML = {
    "TimedBaseModel": {
        "30_min": "started: 2024-04-10T17:03:25Z\ncompleted: 2024-04-10T17:33:25Z\n",
        "3_min": "started: 2024-04-10T17:30:25Z\ncompleted: 2024-04-10T17:33:25Z\n",
        "30_sec": "started: 2024-04-10T17:32:55Z\ncompleted: 2024-04-10T17:33:25Z\n",
        "not_completed": "started: 2024-04-10T17:32:55Z\n",
        "not_started": "{}",
    },
    "VMStatus": {
        "no_condition_no_phase": "id: testid\nname: testname\n",
        "no_condition_pending": "id: testid\nname: testname\nphase: Pending\n",
        "no_condition_completed": "id: testid\nname: testname\nphase: Completed\n",
        "succeeded": f"id: testid\nname: testname\nphase: Completed\nconditions:\n{TEST_SUCCESS_CONDITION}",
        "not_succeeded": f"id: testid\nname: testname\nphase: Completed\nconditions:\n{TEST_FAILED_CONDITION}",
    },
    "Plan": {
        "base": (
            "apiVersion: forklift.konveyor.io/v1beta1\n"
            "kind: Plan\n"
            "metadata:\n"
            "  name: testplan\n"
            "spec:\n"
            "  targetNamespace: testns\n"
            "  vms: []\n"
            "status: {}\n"
        ),
        "invalid_kind": (
            "apiVersion: forklift.konveyor.io/v1beta1\n"
            "kind: NotPlan\n"
            "metadata:\n"
            "  name: testplan\n"
            "spec:\n"
            "  targetNamespace: testns\n"
            "  vms: []\n"
            "status: {}\n"
        ),
        "invalid_api_version": (
            "apiVersion: forklift.konveyor.io/v1alpha1\n"
            "kind: NotPlan\n"
            "metadata:\n"
            "  name: testplan\n"
            "spec:\n"
            "  targetNamespace: testns\n"
            "  vms: []\n"
            "status: {}\n"
        ),
        "success_by_condition": (
            "apiVersion: forklift.konveyor.io/v1beta1\n"
            "kind: Plan\n"
            "metadata:\n"
            "  name: testplan\n"
            "spec:\n"
            "  targetNamespace: testns\n"
            "  vms: []\n"
            "status:\n"
            "  conditions:\n"
            f"{utils.yaml_indent(TEST_SUCCESS_CONDITION, 2)}"
        ),
    },
}

TEST_MODEL_RESULTS = {
    "TimedBaseModel": {
        "30_min": {
            "duration": timedelta(minutes=30),
            "started": datetime(year=2024, month=4, day=10, hour=17, minute=3, second=25, tzinfo=ZoneInfo("UTC")),
            "completed": datetime(year=2024, month=4, day=10, hour=17, minute=33, second=25, tzinfo=ZoneInfo("UTC")),
        },
        "3_min": {
            "duration": timedelta(minutes=3),
            "started": datetime(year=2024, month=4, day=10, hour=17, minute=30, second=25, tzinfo=ZoneInfo("UTC")),
            "completed": datetime(year=2024, month=4, day=10, hour=17, minute=33, second=25, tzinfo=ZoneInfo("UTC")),
        },
        "30_sec": {
            "duration": timedelta(seconds=30),
            "started": datetime(year=2024, month=4, day=10, hour=17, minute=32, second=55, tzinfo=ZoneInfo("UTC")),
            "completed": datetime(year=2024, month=4, day=10, hour=17, minute=33, second=25, tzinfo=ZoneInfo("UTC")),
        },
        "not_completed": {
            "duration": None,
            "started": datetime(year=2024, month=4, day=10, hour=17, minute=32, second=55, tzinfo=ZoneInfo("UTC")),
            "completed": None,
        },
        "not_started": {
            "duration": None,
            "started": None,
            "completed": None,
        },
    },
    "VMStatus": {
        "no_condition_no_phase": {"raises": ValidationError},
        "no_condition_pending": {
            "id": "testid",
            "name": "testname",
            "phase": VMPhase.PENDING,
            "conditions": list(),
            "succeeded": False,
        },
        "no_condition_completed": {
            "id": "testid",
            "name": "testname",
            "phase": VMPhase.COMPLETED,
            "conditions": list(),
            "succeeded": False,
        },
        "succeeded": {
            "id": "testid",
            "name": "testname",
            "phase": VMPhase.COMPLETED,
            "succeeded": True,
        },
        "not_succeeded_by_type": {
            "id": "testid",
            "name": "testname",
            "phase": VMPhase.COMPLETED,
            "succeeded": False,
        },
    },
    "Plan": {
        "base": {
            "duration": None,
            "duration_minutes": None,
            "average_duration": None,
            "vm_count": 0,
            "succeeded": False,
        },
        "invalid_kind": {"raises": ValidationError},
        "invalid_api_version": {"raises": ValidationError},
        "success_by_condition": {"succeeded": True},
    },
}