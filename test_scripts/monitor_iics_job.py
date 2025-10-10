import requests
import os
import sys
import time

# 前のステップからの情報を取得
task_id = os.environ['TASK_ID']
run_id = os.environ['RUN_ID']
server_url = os.environ['SERVER_URL']
session_id = os.environ['SESSION_ID']
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
headers['icSessionId'] = session_id

# --- ステータスのポーリング ---
monitor_url = f'{server_url}/api/v2/activity/activityLog?taskId={task_id}&runId={run_id}'
timeout_seconds = 600  # 10分
start_time = time.time()

while True:
    if time.time() - start_time > timeout_seconds:
        print("ジョブ監視がタイムアウトしました。")
        sys.exit(1)

    status_resp = requests.get(monitor_url, headers=headers)
    if status_resp.status_code != 200 or not status_resp.json():
        print("アクティビティログにジョブが表示されるのを待機中...")
        time.sleep(15)
        continue

    job_details = status_resp.json()[0]
    state = job_details.get('state') # 1 = 成功、2 = 警告、3 = 失敗
    
    if state == 1:
        print("ジョブが正常に完了しました。")
        break
    elif state == 3:
        print("ジョブが失敗しました。")
        print(f"エラーメッセージ: {job_details.get('errorMsg')}")
        sys.exit(1)
    else:
        print(f"ジョブは実行中...（現在のステータス: {job_details.get('status')}）")
        time.sleep(30)