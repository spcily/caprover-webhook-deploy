import requests
import json
import time
import os

base_url=os.environ.get('INPUT_SERVER')
password=os.environ.get('INPUT_PASSWORD')
app_name=os.environ.get('INPUT_APPNAME')
webhook=os.environ.get('INPUT_WEBHOOK')

last_line_number_printed = 0

def get_token(path):
    url = base_url + path
    data = json.dumps({'password': password})
    headers = {'Content-Type': 'application/json', "x-namespace":"captain"}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code != 200:
      print("Error: Unable to login")
      exit(1)

    parsed = r.json() 
    if 'data' in parsed:
      if 'token' in parsed['data']:
        return parsed['data']['token'] 
    return None 
def deploy():
  global webhook
  r = requests.post(webhook)
  if r.status_code != 200:
    print("Error: Failed triggering webhook")
    exit(1)

def output(message):
  print(message, end="")

def on_log_received(log, auth_token):
  global last_line_number_printed
  if log:
    lines = log['data']['logs']['lines']
    first_line_number_of_logs = log['data']['logs']['firstLineNumber']
    first_lines_to_print = 0

    if first_line_number_of_logs > last_line_number_printed:
      if first_line_number_of_logs < 0:
        first_lines_to_print = -first_line_number_of_logs
      else:
        output("[[ TRUNCATED ]]\n") 
    else:
      first_lines_to_print = last_line_number_printed - first_line_number_of_logs
    
    last_line_number_printed = first_line_number_of_logs + len(lines)
    for i in range(first_lines_to_print, len(lines)):
      output(lines[i])

  if log and not log['data']['isAppBuilding']:
    if not log['data']['isBuildFailed']:
      output("\nDeployed successfully for " + app_name)
      exit(0)
    else:
      output("\nDeployment failed " + app_name)
      exit(1)  
  else:
    time.sleep(2)
    get_build_logs('/api/v2/user/apps/appData/', auth_token)

def get_build_logs(path, auth_token, handle_messages=True):
    url = base_url + path + app_name
    headers = {'Content-Type': 'application/json', "x-namespace":"captain", "x-captain-auth":auth_token}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
      print("Error: " + r.text)
      exit(1)
    parsed = r.json() 
    if handle_messages:
      on_log_received(parsed, auth_token)
    return parsed

if __name__ == '__main__':
  try:
    token = get_token('/api/v2/login')
    if token is None:
        print('Error: Login failed')
        exit(1)

    log = get_build_logs('/api/v2/user/apps/appData/', token, False)
    if log['data']['isAppBuilding']:
      print('Error: An active deployment is already in progress')
      exit(1)
    
    deploy()
    get_build_logs('/api/v2/user/apps/appData/', token)

  except Exception as e:
    print('Error: Failed to get build logs')
    print(e)
    exit(1)
