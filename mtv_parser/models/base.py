from pydantic import UUID4, BaseModel, ConfigDict, Field


def to_k8s_case(name: str) -> str:
    words: list[str] = name.split("_")
    result: str = words.pop(0)
    for word in words:
        result = result + word.capitalize()
    return result


class ParserBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_k8s_case, extra="allow")


class MetaData(ParserBaseModel):
    name: str | None = Field(kw_only=True, default=None)


class K8SRef(ParserBaseModel):
    generation: int
    name: str
    namespace: str
    uid: UUID4


class K8SBaseModel(ParserBaseModel):
    api_version: str
    kind: str
    metadata: MetaData
