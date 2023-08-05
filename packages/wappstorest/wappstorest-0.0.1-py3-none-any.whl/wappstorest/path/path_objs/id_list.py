from enum import Enum

from typing import Any

from pydantic import BaseModel
from pydantic import Extra
from pydantic import UUID4


class WappstoVersion(Enum):
    V2_0 = "2.0"
    V2_1 = "2.1"


class ApiMetaTypes(Enum):
    IDLIST = "idlist"
    DELETELIST = "deletelist"
    ATTRIBUTELIST = "attributelist"


class ApiMetaInfo(BaseModel):
    type: ApiMetaTypes  # Merge with MetaAPIData?
    version: WappstoVersion


class childInfo(BaseModel):
    type: str
    version: WappstoVersion


class IdList(BaseModel):
    child: list[ApiMetaInfo]
    id: list[UUID4]
    more: bool
    limit: int
    count: int
    meta: ApiMetaInfo

    # TODO: Remove: 'Extra.forbid' and use meta->type to force type.
    class Config:
        extra = Extra.forbid


class DeleteList(BaseModel):
    deleted: list[UUID4]
    code: int
    message: str = "Deleted"
    meta: ApiMetaInfo

    # TODO: Remove: 'Extra.forbid' and use meta->type to force type.


class AttributeList(BaseModel):
    data: dict[UUID4, Any]
    more: bool
    path: str
    meta: ApiMetaInfo
