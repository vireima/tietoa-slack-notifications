from pydantic import BaseModel, BeforeValidator, Field
from typing_extensions import Annotated


def validate_tags(tags: list[str]):
    return [] if tags is None else [tag for tag in tags if tag != "L"]


Tags = Annotated[
    list[str],
    BeforeValidator(validate_tags),
]


class UserOutputModel(BaseModel):
    username: str
    user: str
    tags: Tags
    active: bool
    notifications: bool
