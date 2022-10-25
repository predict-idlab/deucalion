from enum import Enum

from deucalion.strategies import PrometheusFederated, PrometheusSidecar


class StrategyType(Enum):
    """Deucalion Strategy Types."""
    PROMETHEUS_FEDERATED = 'prometheus_federated'
    PROMETHEUS_SIDECAR = 'prometheus_sidecar'

    @classmethod
    def reverse_lookup(cls, value):
        """Reverse lookup."""
        for _, member in cls.__members__.items():
            if member.value == value:
                return member
        raise LookupError


class StrategyFactory:
    """Deucalion Strategy Factory."""
    types_ = {
        StrategyType.PROMETHEUS_FEDERATED: PrometheusFederated,
        StrategyType.PROMETHEUS_SIDECAR: PrometheusSidecar,
    }

    def get(self, type_: StrategyType):
        """
        Retrieve a recommender.
        :param type_: RecommenderType
        :return: Metric
        """
        cls = self.types_[type_]
        return cls
