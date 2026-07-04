from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
import json
import os
import socket
import requests
import time
import urllib3.util.connection as urllib3_cn

def allowed_gai_family():
    return socket.AF_INET

urllib3_cn.allowed_gai_family = allowed_gai_family

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.heart_rate.read',
    'https://www.googleapis.com/auth/fitness.sleep.read',
]

client_config = {
    "installed": {
        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
        "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
        "redirect_uris": ["http://127.0.0.1:8080/"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
}

flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
creds = flow.run_local_server(host='127.0.0.1', port=8080)

with open('token.json', 'w') as f:
    f.write(creds.to_json())

print("Done — token.json saved")


now_ms = int(time.time() * 1000)
start_ms = now_ms - (24 * 60 * 60 * 1000)

with open('token.json') as f:
    token = json.load(f)['token']
    

headers = {'Authorization': f'Bearer {token}'}

steps_source_id = 'raw:com.google.step_count.delta:com.fitbit.FitbitMobile:health_platform'
hr_source_id = 'raw:com.google.heart_rate.bpm:com.fitbit.FitbitMobile:health_platform'

start_ns = start_ms * 1_000_000
end_ns = now_ms * 1_000_000
dataset_id = f'{start_ns}-{end_ns}'

steps_url = f'https://www.googleapis.com/fitness/v1/users/me/dataSources/{steps_source_id}/datasets/{dataset_id}'
steps_resp = requests.get(steps_url, headers=headers)
with open('steps_data.json', 'w') as f:
    json.dump(steps_resp.json(), f, indent=4)

hr_url = f'https://www.googleapis.com/fitness/v1/users/me/dataSources/{hr_source_id}/datasets/{dataset_id}'
hr_resp = requests.get(hr_url, headers=headers)
with open('heart_rate_data.json', 'w') as f:
    json.dump(hr_resp.json(), f, indent=4)
