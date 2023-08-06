from dataclasses import dataclass, field
from typing import Any, List, Mapping
import heapq

# @dataclass(order=True)
# class PrioritizedItem:
#     priority: int
#     item: Any=field(compare=False)

# pq = []                         # list of entries arranged in a heap
# entry_finder = {}               # mapping of tasks to entries
# REMOVED = '<removed-task>'      # placeholder for a removed task
# counter = itertools.count()     # unique sequence count

# def add_task(task, priority=0):
#     'Add a new task or update the priority of an existing task'
#     if task in entry_finder:
#         remove_task(task)
#     count = next(counter)
#     entry = [priority, count, task]
#     entry_finder[task] = entry
#     heappush(pq, entry)

# def remove_task(task):
#     'Mark an existing task as REMOVED.  Raise KeyError if not found.'
#     entry = entry_finder.pop(task)
#     entry[-1] = REMOVED

# def pop_task():
#     'Remove and return the lowest priority task. Raise KeyError if empty.'
#     while pq:
#         priority, count, task = heappop(pq)
#         if task is not REMOVED:
#             del entry_finder[task]
#             return task
#     raise KeyError('pop from an empty priority queue')


@dataclass(order=True)
class _HeapEntry:
    priority: Any=field(compare=True)
    count: int=field(compare=True) # ensure sort stability, item with same priority will be returned in order of update
    item: Any=field(compare=False)

class HeapDict:
    _removed_marker = object() # unique marker for removed item
    
    def __init__(self) -> None:
        """
        Add a new item or update the priority of an existing item
        """
        self._heap: List[_HeapEntry] = []
        self._entry_finder: Mapping[Any, _HeapEntry] =  {}
        self._cur_count: int = 0

    def update(self, item: Any, priority: int):
        if item in self._entry_finder:
            self.remove(item)
        entry = _HeapEntry(priority=priority, count=self._cur_count, item=item)
        self._cur_count += 1
        
        self._entry_finder[item] = entry
        heapq.heappush(self._heap, entry)
    
    def __setitem__(self, item: Any, priority: int):
        self.update(item, priority)
    
    def remove(self, item: Any):
        """
        Mark an existing item as removed.  Raise KeyError if not found.
        """
        entry = self._entry_finder.pop(item)
        entry.item = HeapDict._removed_marker
    
    def __delitem__(self, item: Any):
        self.remove(item)

    def pop(self) -> Any:
        """
        Remove and return the lowest priority item. Raise KeyError if empty.
        """
        while self._heap:
            entry = heapq.heappop(self._heap)
            if entry.item is not HeapDict._removed_marker:
                del self._entry_finder[entry.item]
                return entry.item
        raise KeyError('pop from an empty heap')
    
    def __contains__(self, item: Any) -> bool:
        if item in self._entry_finder:
            entry = self._entry_finder[item]
            return entry.item is not HeapDict._removed_marker
        return False
