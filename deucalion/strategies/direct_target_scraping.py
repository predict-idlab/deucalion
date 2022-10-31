import json
import logging
import socket
from typing import Dict, Set, Any
from prometheus_client.parser import text_string_to_metric_families
import requests

from deucalion.strategies.strategy import Strategy


class DirectTargetScraping(Strategy):

    def __init__(self):
        self.logger = logging.getLogger('DirectTargetScraping')

        self.targets: [] = None

    def get_metrics(self, desired_metrics: Set[str]) -> Dict[str, Any]:
        res = {}
        for target in self.targets:
            try:
                res_dict = {}
                target_ = 'http://{host}:{port}/{path}'.format(
                    host=target['host'], port=target['port'], path=target['path'])
                r = requests.get(target_)
                for family in text_string_to_metric_families(r.text):
                    for sample in family.samples:
                        metric_name = sample[0]  # sample[0] is metric name
                        if metric_name in desired_metrics:
                            labels_string = json.dumps(sample[1])
                            if metric_name not in res_dict:
                                res_dict[metric_name] = {}
                            res_dict[metric_name][labels_string] = sample[2]  # value
                    res[target_] = res_dict
            except requests.exceptions.ConnectionError:
                self.logger.error('Could not get metrics from target {}'.format(target))

        return res

    def set_config(self, config):
        self.targets = config['targets']
