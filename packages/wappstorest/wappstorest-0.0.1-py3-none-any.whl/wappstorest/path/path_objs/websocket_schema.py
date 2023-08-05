import datetime
import random
import string
import uuid

from enum import Enum

from typing import Any

from pydantic import BaseModel
from pydantic import Extra
from pydantic import validator

from ..WappstoPath import Network
from ..WappstoPath import Device
from ..WappstoPath import Value
from ..WappstoPath import State


class BaseMeta(BaseModel):  # Base Meta
    id: uuid.UUID | None = None
    # NOTE: Set in the children-class.
    # #  type: Optional[WappstoMetaType] = None
    version: str | None = None

    manufacturer: uuid.UUID | None = None
    # owner: uuid.UUID | Assigned | None = None
    parent: uuid.UUID | None = None

    created: datetime.datetime | None = None
    updated: datetime.datetime | None = None
    changed: datetime.datetime | None = None

    application: uuid.UUID | None = None
    # deletion: Deletion | None = None
    deprecated: bool | None = None

    iot: bool | None = None
    revision: int | None = None
    size: int | None = None
    path: str | None = None

    oem: str | None = None
    accept_manufacturer_as_owner: bool | None = None
    redirect: str | None = None

    error: uuid.UUID | None = None
    # warning: list[WarningItem] | None = None
    trace: str | None = None

    set: list[uuid.UUID] | None = None
    contract: list[uuid.UUID] | None = None

    historical: bool | None = None


class EventStreamType(str, Enum):
    eventstream = "eventstream"


class MetaEventSchema(BaseModel):
    id: uuid.UUID
    type: EventStreamType
    version: str


class StreamEvents(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    DIRECT = "direct"


class HttpMethods(str, Enum):
    PATCH = "PATCH"
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    DELETE = "DELETE"


class RpcVersion(str, Enum):
    v2_0 = "2.0"


class EventStreamSchema(BaseModel):
    data: Network | Device | Value | State
    event: StreamEvents
    meta: MetaEventSchema
    meta_object: BaseMeta
    path: str
    timestamp: datetime.datetime

    # @validator('path')
    # def path_check(cls, v, values, **kwargs):
    #     for selftype, selfid in parwise(v.split("/")[1:]):
    #         WappstoMetaType(selftype)
    #         lasttype = selftype
    #         if selfid:
    #             uuid.UUID(selfid)
    #     if "meta_object" in values and "type" in values["meta_object"]:
    #         if values["meta_object"].type != lasttype:
    #             raise ValueError('Path do not match Type')
    #     return v


__session_count: int = 0
__session_id: str = "".join(random.choices(string.ascii_letters + string.digits, k=10))


def _id_gen():
    """Create an unique Rpc-id."""
    global __session_count
    global __session_id
    __session_count += 1
    return f"{__session_id}_WSS_CONFIGS_{__session_count}"


class RPCRequest(BaseModel):
    params: Any | None
    method: HttpMethods
    jsonrpc: RpcVersion | None = RpcVersion.v2_0
    id: str | int | None = None

    class Config:
        extra = Extra.forbid

    @validator("id", pre=True, always=True)
    def id_autofill(cls, v):
        return v or _id_gen()


class RPCSuccess(BaseModel):
    result: Any
    jsonrpc: RpcVersion | None = RpcVersion.v2_0
    id: str | int | None = None

    class Config:
        extra = Extra.forbid

    @validator("id", pre=True, always=True)
    def id_autofill(cls, v):
        return v or _id_gen()
