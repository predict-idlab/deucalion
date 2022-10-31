import logging
import os
import time
from multiprocessing import Pool
import yaml
from optparse import OptionParser

from deucalion import Observer
from deucalion.strategies.factory import StrategyFactory, StrategyType


class Provisioner:
    BILLION = 10 ** 9
    STRATEGIES = {}

    def __init__(self, strategy: StrategyType):

        self.logger = logging.getLogger('Provisioner')

        self.alert_api_instance = None
        self.api_client = None

        strategy_factory = StrategyFactory()
        self.strategy = strategy_factory.get(strategy)

        self.currentScrapeInterval = None
        self.INTERVAL_ORIG = None
        self.alert_name = None

        parser = OptionParser()
        parser.add_option("-c", "--config-file", dest="config_filename",
                          help="config file to configure the topology of deucalion", metavar="CONFIG_FILE")
        (options, args) = parser.parse_args()
        config_filename = options.config_filename
        if config_filename is None:
            config_filename = '/etc/deucalion/config.yaml'

        self.configure(config_filename)

        # list of observers to notify
        self.observers: [Observer] = []

        # process pool to distribute tasks
        self.processPool = None

        # a set of metrics that has to be fetched to provide all observers with the data they expect
        self.metrics = set()

    def configure(self, config_filename):
        file_found = False
        while not file_found:
            try:
                with open(config_filename) as config_file:
                    file_found = True
                    config = yaml.safe_load(config_file)

                    self.INTERVAL_ORIG = float(config['config']['metrics_interval'])
                    self.currentScrapeInterval = self.INTERVAL_ORIG
                    self.strategy.set_config(config['config'])

                    # AlertManager configuration from environment variables set by the sidecar injector
                    self.alert_name = config['alert_manager']['alert_name']
                    alert_manager_host = config['alert_manager']['host']
                    alert_manager_port = config['alert_manager']['port']
                    if self.alert_name is None or alert_manager_port is None or alert_manager_host is None:
                        self.logger.error('alert manager environment variables not set. Are you injecting this application with the deucalion sidecar injector?')
                        exit(1)
                    # alert_config = pac.Configuration()
                    # alert_config.host = 'http://' + alert_manager_host + ':' + str(alert_manager_port) + '/api/v2/'
                    # self.api_client = pac.ApiClient(alert_config)
                    # self.alert_api_instance = pac.AlertApi(self.api_client)
            except FileNotFoundError:
                self.logger.error('Configuration file not found. Did you put the configuration file in the right place?'
                                  + '\t(default /etc/deucalion/deucalion_config.yaml)'
                                  + '\tRetrying in 5 seconds')
                time.sleep(5)

    def register(self, observer: Observer):
        self.metrics = self.metrics.union(observer.metrics)
        self.observers.append(observer)

    def run(self):  # TODO: new_data roepen per target per metrics of werken met dictionary?
        if len(self.observers) == 0:
            self.logger.error("No observers registered, exiting...")
            exit(1)
        self.logger.info('deucalion metrics provisioner started')

        self.processPool = Pool(len(self.observers))
        execute_time = self.INTERVAL_ORIG * Provisioner.BILLION + time.time_ns()
        while True:
            metrics = self.strategy.get_metrics(self.metrics)
            if metrics is not None:
                for observer in self.observers:
                    self.logger.info('sending data to observer...')
                    self.processPool.apply_async(observer.on_next, args=(metrics,), callback=self.send_event)
                # self.processPool.join()  # TODO: is joining really necessary? or should you use callback?

            time_delta = execute_time - time.time_ns()
            wait_time_s = time_delta / Provisioner.BILLION
            if time_delta > 0:
                if wait_time_s > (0.5 * self.currentScrapeInterval) and wait_time_s > self.INTERVAL_ORIG:
                    self.logger.debug("decreasing scrape_interval by 5%")
                    self.currentScrapeInterval *= 0.95
                time.sleep(wait_time_s)

            else:
                self.logger.debug('Scraping interval too low: increasing with 20%')
                self.currentScrapeInterval *= 1.2
            execute_time += self.currentScrapeInterval * Provisioner.BILLION

    def send_event(self, data):
        if data is not None:
            label_set = {
                "alertname": self.alert_name,
                "alert_data": data
            }
            # alert = pac.Alert(label_set)
            # try:
            #     self.alert_api_instance.post_alerts([alert])
            # except ApiException as e:
            #     self.logger.error('Alert manager error: ', e)
            # except MaxRetryError:
            #     self.logger.error('Could not reach Alert Manager. Is the AlertManager running and reachable via the endpoint specified in the configuration file? ')
