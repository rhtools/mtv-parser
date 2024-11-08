import sys

import yaml

from mtv_parser.clioutput import Output
from mtv_parser.models import PlanList


def main():
    parsed_plans: PlanList

    with open(sys.argv[1]) as file:
        data = yaml.safe_load(file)
        parsed_plans = PlanList(**data)
    output = Output()

    vm_names = []
    for plan in parsed_plans.items:
        if plan.vm_count:
            for vm in plan.status.migration.vms:
                vm_names.append(vm.name)

    output.writeline(vm_names)

    output.migration_output(parsed_plans.failed_migrations)
    output.migration_output(parsed_plans.successful_migrations)
    output.close()


if __name__ == "__main__":
    main()
