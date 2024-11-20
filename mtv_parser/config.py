from functools import partial
from pathlib import Path
from typing import Annotated, Any, get_args, get_origin

import click
from click.types import convert_type
from pydanclick import from_pydantic
from pydanclick.types import _ParameterKwargs
from pydantic import Field, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Configuration object for mtv_parser."""

    model_config = SettingsConfigDict(env_prefix="mtv_")

    files: list[FilePath] = Field(description="File to load")

    @classmethod
    def _make_extra_options(cls: type[BaseSettings]) -> dict[str, _ParameterKwargs]:
        """Create dict of click options for model fields.

        Sets required to false if field is supplied through non-cli means.
        Parse List types to multiples with correct type.

        This function is only neccessary to patch pydanclick to support our use case.
        Everything in this is either available in unreleased pydanclick versions, or
        partially available with open PRs or Issues.  It will be able to go away completely.

        Returns:
            dict[str, _ParameterKwargs]: extra_args dict for pydanclick
        """
        # create dict of options set via all supported non-cli methods
        alt_settings = cls.model_construct()._settings_build_values({})

        # Extra options dict is applied by pydanclick after model parsing.
        extra_options: dict[str, _ParameterKwargs] = {}

        def update_extra_options(field: str, **kwargs: Any) -> None:
            """update extra_options with passed values

            Uses pydanclick TypedDict to validate option names

            Args:
                field (str): name of field in extra_options dict
                kwargs: any valid option in pydanclick
            """
            _ParameterKwargs(**kwargs)
            if field in extra_options:
                extra_options[field].update(_ParameterKwargs(**kwargs))
            else:
                extra_options[field] = _ParameterKwargs(**kwargs)

        for setting in alt_settings.keys():
            # set flag for each option that is set elsewhere as not required
            update_extra_options(setting, required=False)

        for name, field_info in cls.model_fields.items():
            # handle list types.
            if get_origin(field_info.annotation) is list:
                update_extra_options(name, multiple=True)
                field_args = get_args(field_info.annotation)
                field_type = next(field_arg for field_arg in field_args if field_arg is not None)
                if get_origin(field_type) is Annotated:
                    field_args = get_args(field_type)
                    field_type = next(field_arg for field_arg in field_args if field_arg is not None)
                click_type: click.ParamType
                if field_type is Path:
                    click_type = click.Path(path_type=Path)
                else:
                    click_type = convert_type(field_type)
                update_extra_options(name, type=click_type)

        return extra_options


# partial of from_pydantic decorator to prevent repeats and allow it to exist in config module
ClickConfig = partial(
    from_pydantic,
    Config,
    extra_options=Config._make_extra_options(),
    rename={"files": "--file"},
    shorten={"files": "-f"},
)
