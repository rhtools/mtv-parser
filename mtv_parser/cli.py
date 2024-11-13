import click
import yaml
from pydanclick import from_pydantic

from mtv_parser.clioutput import Output
from mtv_parser.config import Config
from mtv_parser.models import PlanList


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
@click.pass_context
def summary(ctx: click.Context, config: Config) -> None:
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

    ctx.obj["Output"].migration_output(parsed_plans.failed_migrations)
    ctx.obj["Output"].migration_output(parsed_plans.successful_migrations)
