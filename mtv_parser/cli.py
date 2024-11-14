from collections.abc import Callable
from functools import update_wrapper
from typing import Any

import click
import yaml
from pydanclick import from_pydantic

from mtv_parser.clioutput import Output
from mtv_parser.config import Config
from mtv_parser.models import PlanList


def pass_output(f: Callable):
    """Wrap decorated function to create output module, and tear it down afterwards."""

    @click.pass_context
    def output_func(ctx: click.Context, *args: Any, **kwargs: Any):
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
@from_pydantic(Config, extra_options=Config.make_extra_options())
@pass_output
def summary(output: Output, config: Config) -> None:
    """Generate summary of MTV plan.
    \f
    Args:
        ctx (Context): click context object
        config (Config): Config Object created by cli options, environment variables, and config files
    """
    parsed_plans: PlanList

    with open(config.file) as file:
        data = yaml.safe_load(file)
        parsed_plans = PlanList(**data)

    output.migration_output(parsed_plans.failed_migrations)
    output.migration_output(parsed_plans.successful_migrations)
