import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse
import os
import json
import sys
import re

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

baseUrl = sys.argv[1]
client_id = sys.argv[2]
client_secret = sys.argv[3]
projectId = sys.argv[4]
exportFileName = sys.argv[5]
exportFormat = sys.argv[6]
outputDir = sys.argv[7]
url = baseUrl + "/graphql"

client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url= baseUrl + '/api/oauth/token', client_id=client_id,
        client_secret=client_secret)

with open('export.json', 'r') as file:
    payloadString = file.read()
    payload = json.loads(payloadString)
  
payload["variables"]["input"]["fileName"] = exportFileName
payload["variables"]["input"]["projectId"] = projectId
payload["variables"]["input"]["format"] = exportFormat

headers = {
  'Authorization': 'Bearer ' + token['access_token'],
  'Content-Type': 'application/json'
}


response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
if 'json' in response.headers['content-type']:
  jsonResponse = json.loads(response.text.encode('utf8'))
  print(json.dumps(jsonResponse, indent=1))
  if len(jsonResponse["data"]["result"]["fileUrl"]) > 0: 
    fileUrl = jsonResponse["data"]["result"]["fileUrl"]
    os.makedirs(outputDir, exist_ok=True)
  
    while True:
      fileResponse = requests.request("GET", fileUrl)
      if fileResponse.status_code == 200:
        fileResponseUrl = urlparse(fileUrl)
        fileName = os.path.basename(fileResponseUrl.path)
        outputFile = outputDir + '/' + fileName
        open(outputFile, 'wb').write(fileResponse.content)
        print("Success downloading the file. Output file:" + outputFile)
        break;
      elif fileResponse.status_code == 404:
        print("Waiting for the file.")
      elif fileResponse.status_code == 403 or  fileResponse.status_code >=500:
        print("Stop waiting because error.")
else:
  print(response)   
  

