import requests
import os
import sys
import json

username = os.environ['IICS_USER']
password = os.environ['IICS_PASS']
task_id = os.environ['TASK_ID']
task_type = os.environ['TASK_TYPE']

base_url = 'https://dm-us.informaticacloud.com'

# --- ログイン ---
login_payload = {"@type": "login", "username": username, "password": password}
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
login_response = requests.post(f'{base_url}/ma/api/v2/user/login', json=login_payload, headers=headers)

if login_response.status_code != 200:
    print("ログインに失敗しました。")
    sys.exit(1)

login_info = login_response.json()
session_id = login_info['icSessionId']
server_url = login_info['serverUrl']
headers['icSessionId'] = session_id

# --- ジョブ開始 ---
start_job_payload = {
    "@type": "job",
    "taskId": task_id,
    "taskType": task_type 
}
start_job_resp = requests.post(f'{server_url}/api/v2/job', json=start_job_payload, headers=headers)

if start_job_resp.status_code != 200:
    print("ジョブの起動に失敗しました。")
    print(start_job_resp.text)
    sys.exit(1)

run_id = start_job_resp.json()['runId']
print(f"ジョブの起動に成功しました。Run ID: {run_id}")

print(f"::set-output name=runId::{run_id}")
print(f"::set-output name=serverUrl::{server_url}")
print(f"::set-output name=sessionId::{session_id}")