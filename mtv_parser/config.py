from pydanclick.types import _ParameterKwargs
from pydantic import Field, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Configuration object for mtv_parser."""

    model_config = SettingsConfigDict(env_prefix="mtv_")

    file: FilePath = Field(description="File to load")

    @classmethod
    def make_extra_options(cls: type[BaseSettings]) -> dict[str, _ParameterKwargs]:
        """Create dict of click options for model fields.

        Sets required to false if field is supplied through non-cli means.

        Returns:
            dict[str, _ParameterKwargs]: extra_args dict for pydanclick
        """
        # create dict of options set via all supported non-cli methods
        alt_settings = cls.model_construct()._settings_build_values({})

        extra_options = {}
        for setting in alt_settings.keys():
            # set flag for each option that is set elsewhere as not required
            extra_options[setting] = {"required": False}

        return extra_options
