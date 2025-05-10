import os
import requests

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")

def notify_slack(message):
    if SLACK_WEBHOOK:
        data = { "text": message }
        requests.post(SLACK_WEBHOOK, json=data)

def notify_teams(message):
    if TEAMS_WEBHOOK:
        data = { "text": message }
        requests.post(TEAMS_WEBHOOK, json=data)

def notify_all(message):
    notify_slack(message)
    notify_teams(message)
