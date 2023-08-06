from typing import Any, Dict, List, Protocol, TypedDict


class StreamsyncWebsocketIncoming(TypedDict):
    type: str
    trackingId: int
    payload: Dict[str, Any]


class StreamsyncWebsocketOutgoing(TypedDict):
    type: str
    trackingId: int
    payload: Dict
    mutations: Dict[str, Any]


class InstancePathItem(TypedDict):
    componentId: str
    instanceNumber: int


InstancePath = List[InstancePathItem]


class StreamsyncEvent(TypedDict):
    type: str
    instancePath: InstancePath
    payload: Any


class Readable(Protocol):
    def read(self) -> Any:
        ...
