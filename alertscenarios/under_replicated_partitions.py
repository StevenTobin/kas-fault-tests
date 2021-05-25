#!/usr/bin/env python3

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import time, datetime
from sys import argv
from scripts import monitor_alerts
from scripts import utils
from scripts.logger import log

topic_name = 'test-auto-' + datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d-%H%M%S')
kafka_cluster = ''
bootstrap_server = ''

def run_scenario():
  # Change to kafka-cluster namespace
  utils.get_cmd_output('oc project kafka-cluster')
  # Create a new topic
  utils.get_cmd_output('oc exec -it ' + kafka_cluster + '-kafka-0 -c kafka -- env - bin/kafka-topics.sh --bootstrap-server ' + bootstrap_server + ' --create --replication-factor 3 --partitions 3 --topic ' + topic_name)
  # Produce messages to the new topic
  utils.get_cmd_output('oc exec -it ' + kafka_cluster + '-kafka-0 -c kafka -- bin/kafka-producer-perf-test.sh --producer-props bootstrap.servers=' + bootstrap_server + ' --record-size=100 --throughput 1 --num-records 10 --topic ' + topic_name)
  # Force kafka broker pod termination for a minute
  t_end = time.time() + 60 # 1 minute
  while time.time() < t_end:
    time.sleep(5)
    utils.get_cmd_output('oc delete pod ' + kafka_cluster + '-kafka-2 --grace-period=0 --force')
  # Check under-replicated partitions
  utils.get_cmd_output('oc exec -it ' + kafka_cluster + '-kafka-0 -c kafka -- env - bin/kafka-topics.sh --bootstrap-server ' + bootstrap_server + ' --describe --under-replicated-partitions')
  # Delete topic
  utils.get_cmd_output('oc exec -it ' + kafka_cluster + '-kafka-0 -c kafka -- env - bin/kafka-topics.sh --bootstrap-server ' + bootstrap_server + ' --delete --topic ' + topic_name)

def init_args(args: list):
  global kafka_cluster
  global bootstrap_server
  if len(args) > 2:
    print('Usage: ./under_replicated_partitions.py <kafka-cluster-ns> <booststrap-server-url>')
    exit(1)
  kafka_cluster = args[0] if len(args) > 0 else 'my-cluster'
  bootstrap_server = args[1] if len(args) > 1 else 'my-cluster-kafka-bootstrap.kafka-cluster.svc:9092'
  log.info('Kafka cluster: ' + kafka_cluster)
  log.info('Bootstrap server URL: ' + bootstrap_server)

if __name__== '__main__':
  init_args(argv[1:])
  run_scenario()
  alerts = monitor_alerts.get_alerts("all", "managed-services-monitoring-prometheus")
  monitor_alerts.is_alert_present(alerts, "UnderReplicatedPartitions")
