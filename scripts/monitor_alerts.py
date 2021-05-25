#!/usr/bin/env python3

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import json
from scripts.logger import log
from scripts import utils

def get_alerts_endpoint(namespace: str) -> (str):
  prometheus_route = utils.get_cmd_output(
      "oc get route -n" + namespace).split("\n")[1].split()[1]
  prometheus_alerts_endpoint = prometheus_route + "/api/v1/alerts"
  return prometheus_alerts_endpoint

def filter_alerts(severity:str, alerts:list) -> (list):
  if(severity == "all"):
    return alerts
  filtered_alerts = []
  for alert in alerts:
    if(alert["labels"]["severity"] == severity):
      filtered_alerts.append(alert)
  return filtered_alerts  

def get_all_alerts(prometheus_alerts_endpoint:str) -> (list): 
  prometheus_json = json.loads(utils.get_cmd_output("curl -s " + prometheus_alerts_endpoint))
  return prometheus_json["data"]["alerts"]

def get_alerts(severity:str, namespace:str) -> (list):
  log.info("Fetching alerts...")
  alerts = get_all_alerts(get_alerts_endpoint(namespace))
  if(len(alerts) == 0):
    return []
  return filter_alerts(severity, alerts)

def is_alert_present(alerts:list, alert_name:str):
  for alert in alerts:
    if(alert["labels"]["alertname"] == alert_name): 
      log.info("### SUCCESS ### Alert " + alert_name + " has been triggered")
      exit(0)
  log.error("### FAILED ### Alert " + alert_name + " has NOT been triggered")
  exit(1)

def main():
  alerts = get_alerts("all", "managed-services-monitoring-prometheus")
  log.info("Number of alerts: " + str(len(alerts)))

if __name__== "__main__":
  main()
