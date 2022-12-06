from enum import Enum

from deucalion.strategies import DirectTargetScraping, PrometheusServerQuerying, PrometheusTargetScraping


class StrategyType(Enum):
    """Deucalion Strategy Types."""
    DIRECT_TARGET_SCRAPING = 'direct_target_scraping'
    PROMETHEUS_SERVER_QUERYING = 'prometheus_server_querying'
    PROMETHEUS_TARGET_SCRAPING = 'prometheus_target_scraping'

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
        StrategyType.DIRECT_TARGET_SCRAPING: DirectTargetScraping,
        StrategyType.PROMETHEUS_SERVER_QUERYING: PrometheusServerQuerying,
        StrategyType.PROMETHEUS_TARGET_SCRAPING: PrometheusTargetScraping,
    }

    def get(self, type_: StrategyType):
        """
        Retrieve a strategy.
        :param type_: StrategyType
        :return: Metric
        """
        cls = self.types_[type_]
        return cls()
