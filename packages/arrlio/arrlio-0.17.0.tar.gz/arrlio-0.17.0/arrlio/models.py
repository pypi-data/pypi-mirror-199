import datetime
from dataclasses import asdict, dataclass, field
from functools import cached_property
from types import TracebackType
from typing import Any, Callable, Dict, List, Set, Tuple, Union
from uuid import UUID, uuid4

from roview import rodict, roset

from arrlio.exc import GraphError
from arrlio.settings import (
    EVENT_TTL,
    MESSAGE_ACK_LATE,
    MESSAGE_EXCHANGE,
    MESSAGE_PRIORITY,
    MESSAGE_TTL,
    TASK_ACK_LATE,
    TASK_BIND,
    TASK_EVENT_TTL,
    TASK_EVENTS,
    TASK_PRIORITY,
    TASK_QUEUE,
    TASK_RESULT_RETURN,
    TASK_RESULT_TTL,
    TASK_TIMEOUT,
    TASK_TTL,
)


@dataclass
class TaskData:
    """
    Args:
        meta (dict, optional): additional task function keyword argument.
    """

    task_id: UUID = field(default_factory=uuid4)
    args: tuple = field(default_factory=tuple)
    kwds: dict = field(default_factory=dict)
    meta: dict = field(default_factory=dict)

    queue: str = TASK_QUEUE
    priority: int = TASK_PRIORITY
    timeout: int = TASK_TIMEOUT
    ttl: int = TASK_TTL
    ack_late: bool = TASK_ACK_LATE
    result_ttl: int = TASK_RESULT_TTL
    result_return: bool = TASK_RESULT_RETURN
    thread: bool = None
    events: Union[bool, Set[str]] = TASK_EVENTS
    event_ttl: int = EVENT_TTL

    extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.task_id, str):
            object.__setattr__(self, "task_id", UUID(self.task_id))
        if isinstance(self.args, list):
            object.__setattr__(self, "args", tuple(self.args))

    def dict(self, exclude=None):
        if exclude:
            return {k: v for k, v in asdict(self).items() if k not in exclude}
        return asdict(self)


@dataclass(frozen=True)
class Task:
    func: Callable
    name: str
    bind: bool = TASK_BIND

    queue: str = TASK_QUEUE
    priority: int = TASK_PRIORITY
    timeout: int = TASK_TIMEOUT
    ttl: int = TASK_TTL
    ack_late: bool = TASK_ACK_LATE
    result_ttl: int = TASK_RESULT_TTL
    result_return: bool = TASK_RESULT_RETURN
    thread: bool = None
    events: Union[bool, Set[str]] = TASK_EVENTS
    event_ttl: int = TASK_EVENT_TTL

    extra: dict = field(default_factory=dict)

    loads: Callable = None
    dumps: Callable = None

    @cached_property
    def _exclude(self):
        return {"loads", "dumps"}

    def dict(self, exclude=None):
        exclude = exclude or []
        return {k: v for k, v in asdict(self).items() if k not in self._exclude and k not in exclude}

    def instantiate(self, extra: dict = None, **kwds) -> "TaskInstance":
        data: TaskData = TaskData(
            **{
                **{
                    "queue": self.queue,
                    "priority": self.priority,
                    "timeout": self.timeout,
                    "ttl": self.ttl,
                    "ack_late": self.ack_late,
                    "result_ttl": self.result_ttl,
                    "result_return": self.result_return,
                    "thread": self.thread,
                    "events": self.events,
                    "event_ttl": self.event_ttl,
                    "extra": {**self.extra, **(extra or {})},
                },
                **kwds,
            }
        )
        return TaskInstance(task=self, data=data)

    def __call__(self, *args, **kwds) -> Any:
        return self.instantiate(args=args, kwds=kwds)()


@dataclass(frozen=True)
class TaskInstance:
    task: Task
    data: TaskData

    def __call__(self, meta: bool = False):
        task = self.task
        data = self.data
        args = data.args
        kwds = data.kwds
        if meta is True:
            kwds["meta"] = data.meta
        if task.bind:
            args = (self,) + args
        if isinstance(task.func, type):
            func = task.func()
        else:
            func = task.func
        return func(*args, **kwds)

    def dict(self, exclude=None):
        exclude = exclude or []
        task_exclude = [x.split("task.", 1)[-1] for x in exclude if x.startswith("task.")]
        data_exclude = [x.split("data.", 1)[-1] for x in exclude if x.startswith("data.")]
        return {"task": self.task.dict(exclude=task_exclude), "data": self.data.dict(exclude=data_exclude)}


@dataclass(frozen=True)
class TaskResult:
    res: Any = None
    exc: Union[Exception, Tuple[str, str, str]] = None
    trb: Union[TracebackType, str] = None
    idx: Tuple[str, int] = None
    routes: Union[str, List[str]] = None

    def set_idx(self, idx: Tuple[str, int]):
        object.__setattr__(self, "idx", idx)

    def dict(self):
        return {
            "res": self.res,
            "exc": self.exc,
            "trb": self.trb,
            "idx": self.idx,
            "routes": self.routes,
        }


@dataclass(frozen=True)
class Message:
    data: Any
    message_id: UUID = field(default_factory=uuid4)
    exchange: str = MESSAGE_EXCHANGE
    priority: int = MESSAGE_PRIORITY
    ttl: int = MESSAGE_TTL
    ack_late: bool = MESSAGE_ACK_LATE
    extra: dict = field(default_factory=dict)

    def dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Event:
    type: str
    data: dict
    event_id: UUID = field(default_factory=uuid4)
    dt: datetime.datetime = None
    ttl: int = EVENT_TTL

    def __post_init__(self):
        if not isinstance(self.event_id, UUID):
            object.__setattr__(self, "event_id", UUID(self.event_id))
        if self.dt is None:
            object.__setattr__(self, "dt", datetime.datetime.now(tz=datetime.timezone.utc))
        elif isinstance(self.dt, str):
            object.__setattr__(self, "dt", datetime.datetime.fromisoformat(self.dt))

    def dict(self):
        return asdict(self)


class Graph:
    def __init__(
        self,
        name: str,
        nodes: Dict = None,
        edges: Dict = None,
        roots: Set = None,
    ):
        self.name = name
        self.nodes: Dict[str, List[str]] = rodict({}, nested=True)
        self.edges: Dict[str, List[str]] = rodict({}, nested=True)
        self.roots: Set[str] = roset(set())
        nodes = nodes or {}
        edges = edges or {}
        roots = roots or set()
        for node_id, (task, kwds) in nodes.items():
            self.add_node(node_id, task, root=node_id in roots, **kwds)
        for node_id_from, nodes_to in edges.items():
            for node_id_to, routes in nodes_to:
                self.add_edge(node_id_from, node_id_to, routes=routes)

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name} nodes={self.nodes} edges={self.edges} roots={self.roots}"

    def __repr__(self):
        return self.__str__()

    def add_node(self, node_id: str, task: Union[Task, str], root: bool = None, **kwds):
        if node_id in self.nodes:
            raise GraphError(f"Node '{node_id}' already in graph")
        if isinstance(task, Task):
            task = task.name
        self.nodes.__original__[node_id] = [task, kwds]
        if root:
            self.roots.__original__.add(node_id)

    def add_edge(self, node_id_from: str, node_id_to: str, routes: Union[str, List[str]] = None):
        if node_id_from not in self.nodes:
            raise GraphError(f"Node '{node_id_from}' not found in graph")
        if node_id_to not in self.nodes:
            raise GraphError(f"Node '{node_id_to}' not found in graph")
        if isinstance(routes, str):
            routes = [routes]
        self.edges.__original__.setdefault(node_id_from, []).append([node_id_to, routes])

    def dict(self):
        return {
            "name": self.name,
            "nodes": self.nodes,
            "edges": self.edges,
            "roots": self.roots,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            nodes=data["nodes"],
            edges=data["edges"],
            roots=data["roots"],
        )
