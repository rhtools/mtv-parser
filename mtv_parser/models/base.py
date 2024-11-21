from pydantic import BaseModel, ConfigDict


def to_k8s_case(name: str) -> str:
    words: list[str] = name.split("_")
    result: str = words.pop(0)
    for word in words:
        result = result + word.capitalize()
    return result


class ParserBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_k8s_case, extra="allow")
