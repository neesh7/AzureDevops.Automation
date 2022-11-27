import os
import requests, json, base64, sys

#Login Details, provide pat as system argument during program exection or pipeline arguments 
PAT = sys.argv[1]
#Note: Username can be an empty string and Password will be your PAT
username = ''
login_info = username + ":" + PAT
#Base 64 Encoding for Azure Devops Authorization 
b64 = base64.b64encode(login_info.encode()).decode()

#provide URL Parameters here in line 13
organization, project, PipelineID ="" ,"", ""
#Triggering build pipeline through automation
#Note: Follow these links to learn more: 
# https://learn.microsoft.com/en-us/rest/api/azure/devops/build/builds/queue?view=azure-devops-rest-6.1
#https://learn.microsoft.com/en-us/rest/api/azure/devops/pipelines/runs/run-pipeline?view=azure-devops-rest-7.0
# POST https://dev.azure.com/{organization}/{project}/_apis/build/builds?api-version=6.1-preview.7
url = f'https://dev.azure.com/{organization}/{project}/_apis/pipelines/{PipelineID}/runs?api-version=7.0'
data = {}
# a = json.dumps(data)
r = requests.post(url, json=data, 
    headers={'Content-Type': 'application/json',"Authorization" : f"Basic {b64}"})

print(r.json())