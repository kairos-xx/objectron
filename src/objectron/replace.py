from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from ctypes import c_int, py_object, pythonapi
from gc import get_referrers
from hashlib import sha256
from inspect import getmembers_static, stack
from threading import Lock
from time import sleep
from types import FrameType
from typing import Any, Callable, List, Tuple, TypeVar

from .exceptions import TransformationError

T = TypeVar("T")


def generate_object_id(obj: Any) -> str:
    """Generate a unique ID for an object using its id and type."""
    return sha256(f"{id(obj)}-{type(obj)}".encode()).hexdigest()


class DeepObjectReplacer:
    """Replace object references throughout Python's runtime object graph.
    The replacement operations use a thread pool to ensure controlled
    concurrency.
    Warning:
        1. This is experimental and may cause race conditions or data
           corruption due to concurrent modifications.
        2. Global side effects can break Python internals.
        3. True CPU parallelism is limited by the GIL.
    Usage:
        replacer = DeepObjectReplacer(old_obj=obj_a, new_obj=obj_b,
                                    max_workers=4)
    """

    def __init__(self,
                 old_obj: object,
                 new_obj: object,
                 max_workers: int = 4) -> None:
        """Initialize replacer and execute replacement logic.
        Args:
            old_obj: Object to replace throughout runtime.
            new_obj: Object that will replace old_obj.
            max_workers: Maximum number of concurrent worker threads.
        Raises:
            TypeError: If old_obj or new_obj is not a Python object.
            ValueError: If max_workers is less than 1.
        """
        if old_obj is None or isinstance(old_obj, str):
            raise TransformationError("old_obj must be a Python object")
        if new_obj is None or isinstance(new_obj, str):
            raise TypeError("new_obj must be a Python object")
        if not isinstance(max_workers, int) or max_workers < 1:
            raise ValueError("max_workers must be a positive integer")

        self.old_obj = old_obj
        self.new_obj = new_obj
        self.visited = set()
        self.visited_lock = Lock()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._futures = []

        try:
            self._replace_references()
            self._wait_for_all_tasks(0.2)
            self._executor.shutdown(wait=True)
        except Exception as e:
            raise TransformationError(str(e)) from e

    def _replace_references(self) -> None:
        """Replace references in object graph and active stack frames."""
        self._replace_all_refs(self.old_obj, self.new_obj)
        frames = reversed(stack())
        for frame_info in frames:
            self._schedule_task(self._handle_frame, (frame_info, ))

    def _schedule_task(self, func: Callable[..., None],
                       args: Tuple[Any, ...]) -> None:
        """Schedule a task for execution in the thread pool."""
        try:
            future = self._executor.submit(
                self._safe_execute,
                func,
                *args,
            )
            self._futures.append(future)
        except RuntimeError:
            pass  # Ignore scheduling after shutdown

    def _safe_execute(
        self,
        func: Callable[..., None],
        *args: Any,
    ) -> None:
        """Execute a function with error handling."""
        self._wait_for_all_tasks()
        with suppress(Exception):
            func(*args)

    def _handle_frame(self, frame_info: Any) -> None:
        frame = frame_info.frame
        globals_dict = frame.f_globals
        locals_dict = frame.f_locals
        changed_locals = [False]
        for key, val in list(globals_dict.items()):
            if val is self.old_obj:
                globals_dict[key] = self.new_obj
            self._schedule_task(self._replace_in_members, (val, ))
        if locals_dict is not None:
            for key, val in list(locals_dict.items()):
                if val is self.old_obj:
                    locals_dict[key] = self.new_obj
                    changed_locals[0] = True
                self._schedule_task(self._replace_in_members, (val, ))
        if changed_locals[0]:
            pythonapi.PyFrame_LocalsToFast(py_object(frame), c_int(0))

    def _replace_all_refs(self, org_obj: Any, new_obj_: Any) -> None:
        referrers = get_referrers(org_obj)

        self._schedule_task(self._process_referrers,
                            (org_obj, new_obj_, referrers))

    def _process_referrers(self, org_obj: Any, new_obj_: Any,
                           referrers: List[Any]) -> None:
        for referrer in referrers:
            with suppress(Exception):
                if isinstance(referrer, FrameType):
                    continue
                if isinstance(referrer, dict):
                    for key, value in list(referrer.items()):
                        if value is org_obj:
                            referrer[key] = new_obj_
                        if key is org_obj:
                            referrer[new_obj_] = referrer.pop(key)
                elif isinstance(referrer, list):
                    for i, value in enumerate(referrer):
                        if value is org_obj:
                            referrer[i] = new_obj_
                elif isinstance(referrer, set):
                    if org_obj in referrer:
                        referrer.remove(org_obj)
                        referrer.add(new_obj_)
                else:
                    self._schedule_task(self._replace_in_members, (referrer, ))

    def _replace_in_members(self, obj: Any) -> None:
        obj_id = generate_object_id(obj)
        with self.visited_lock:
            if obj_id in self.visited:
                return
            self.visited.add(obj_id)
        for attr_name in dir(type(obj)):
            if attr_name == "add":
                attr_value = type(obj).__dict__.get(attr_name)
                print(attr_name, attr_value)
                if attr_value:

                    with suppress(Exception):
                        object.__setattr__(type(self.new_obj), attr_name,
                                           attr_value)
        for attr_name, attr_value in getmembers_static(obj):
            if attr_value is self.old_obj:
                with suppress(Exception):
                    setattr(obj, attr_name, self.new_obj)
                continue

    def _wait_for_all_tasks(self, time: float = 0.01) -> None:
        """Wait for all scheduled tasks to complete."""
        sleep(time)
