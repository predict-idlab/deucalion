from typing import Dict, Any, Set

import deucalion as dc
from deucalion.strategies.factory import StrategyType


class AnomalyDetector(dc.Observer):

    def __init__(self, desired_metrics: Set[str]):
        super().__init__(desired_metrics)

    def on_next(self, data: Dict[str, Dict[str, Any]]):
        if len(data):
            for target in data:
                print("new data from target: " + target)
                print(data[target])
                # pred = self.model.predict(targets_data_dict[target])
                # print(target + ': ' + str(targets_data_dict[target].index[0]) + ', anomaly score: ' + str(pred))
        else:
            print("Data object received was empty")
        return 'ups' # TODO: anomaly rate (percentage for overhead testing) eventueel variabel anomaly rate
        # TODO: create alert return body instead of just value


if __name__ == '__main__':
    observer = AnomalyDetector({
        'go_goroutines',
        'go_gc_heap_allocs_by_size_bytes_total_bucket',
        'node_cpu_seconds_total'
    })
    provisioner = dc.Provisioner(strategy=StrategyType.DIRECT_TARGET_SCRAPING)
    provisioner.register(observer=observer)
    provisioner.run()
