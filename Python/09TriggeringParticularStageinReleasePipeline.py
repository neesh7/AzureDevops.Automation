import os
import requests, json, base64, sys

#Login Details, provide pat as system argument during program exection or pipeline arguments 
PAT = sys.argv[1]
#Note: Username can be an empty string and Password will be your PAT
username = ''
login_info = username + ":" + PAT
#Base 64 Encoding for Azure Devops Authorization 
b64 = base64.b64encode(login_info.encode()).decode()

#Creating releases through automation
# Follow this Link for detailed notes : https://learn.microsoft.com/en-us/rest/api/azure/devops/release/releases/create?view=azure-devops-rest-6.0&tabs=HTTP
# POST https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases?api-version=6.0
organization, project, definitionId ="" ,"", 1
url = f'https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases?api-version=6.0'
# Release Body
ReleaseBody = {
  "definitionId": f"{definitionId}",
  "description": "Creating Sample release",
  "isDraft": False,
  "reason": "none",
  "manualEnvironments": None
}
# Sending Post Request to trigger the release 
r = requests.post(url, json=ReleaseBody, 
    headers={'Content-Type': 'application/json',"Authorization" : f"Basic {b64}"})
print(r)
print(r.text)

releaseId = r.text['id']
print(releaseId)
# print(r.json())