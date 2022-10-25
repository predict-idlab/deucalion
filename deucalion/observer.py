from abc import ABC, abstractmethod
from typing import Dict, Any, Set


class Observer(ABC):
    @abstractmethod
    def on_next(self, data: Dict[str, Dict[str, Any]]):
        raise NotImplementedError

    def __init__(self, metrics: Set[str]):
        self.metrics = metrics
