import json
import requests
import time
import os

def main():
    with open('auth/token.json') as f:
        token = json.load(f)['token']

    headers = {'Authorization': f'Bearer {token}'}

    steps_source_id = 'raw:com.google.step_count.delta:com.fitbit.FitbitMobile:health_platform'
    hr_source_id = 'raw:com.google.heart_rate.bpm:com.fitbit.FitbitMobile:health_platform'
    sleep_source_id = 'derived:com.google.sleep.segment:com.google.android.gms:merged'

    now_ms = int(time.time() * 1000)
    start_ms = now_ms - (24 * 60 * 60 * 1000)
    start_ns = start_ms * 1_000_000
    end_ns = now_ms * 1_000_000
    dataset_id = f'{start_ns}-{end_ns}'

    os.makedirs('data', exist_ok=True)

    steps_url = f'https://www.googleapis.com/fitness/v1/users/me/dataSources/{steps_source_id}/datasets/{dataset_id}'
    steps_resp = requests.get(steps_url, headers=headers)
    with open('data/steps_data.json', 'w') as f:
        json.dump(steps_resp.json(), f, indent=4)

    hr_url = f'https://www.googleapis.com/fitness/v1/users/me/dataSources/{hr_source_id}/datasets/{dataset_id}'
    hr_resp = requests.get(hr_url, headers=headers)
    with open('data/heart_rate_data.json', 'w') as f:
        json.dump(hr_resp.json(), f, indent=4)

    sleep_url = f'https://www.googleapis.com/fitness/v1/users/me/dataSources/{sleep_source_id}/datasets/{dataset_id}'
    sleep_resp = requests.get(sleep_url, headers=headers)
    with open('data/sleep_data.json', 'w') as f:
        json.dump(sleep_resp.json(), f, indent=4)

if __name__ == '__main__':
    main()