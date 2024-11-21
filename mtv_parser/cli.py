from collections.abc import Callable
from functools import update_wrapper
from typing import Any

import click

from mtv_parser.clioutput import Output
from mtv_parser.config import ClickConfig, Config
from mtv_parser.loader import load_files
from mtv_parser.models import PlanList


def pass_output(f: Callable) -> Callable:
    """Wrap decorated function to create output module, and tear it down afterwards."""

    @click.pass_context
    def output_func(ctx: click.Context, *args: Any, **kwargs: Any) -> Any:
        output = Output()

        response = ctx.invoke(f, output, *args, **kwargs)
        output.close()
        return response

    return update_wrapper(output_func, f)


@click.group()
@click.pass_context
def root(ctx: click.Context) -> None:
    """Generate report artifacts based on MTV data.
    \f
    Args:
        ctx (Context): click context object
    """
    ctx.ensure_object(dict)

    ctx.obj["Output"] = Output()


@root.command()
@ClickConfig()
@pass_output
def summary(output: Output, config: Config) -> None:
    """Generate summary of MTV plan.
    \f
    Args:
        ctx (Context): click context object
        config (Config): Config Object created by cli options, environment variables, and config files
    """
    parsed_plans: PlanList
    for parsed_model in load_files(config.files):
        if isinstance(parsed_model, PlanList):
            parsed_plans = parsed_model
            break
    else:
        raise ValueError("Cannot create summary without PlanList")
    output.migration_output(parsed_plans.failed_migrations)
    output.migration_output(parsed_plans.successful_migrations)
