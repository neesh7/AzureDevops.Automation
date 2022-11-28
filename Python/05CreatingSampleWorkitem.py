import requests, json, base64, sys

# PAT Will be supplied through Pipeline Variables 
PAT = sys.argv[1]
#Login Details 
username = ''
login_info = username + ":" + PAT
#Base 64 Encoding for Azure Devops Authorization 
b64 = base64.b64encode(login_info.encode()).decode()
organization, project  ="" ,""
#URI
url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$task?api-version=5.1'

# Body of the requests 
data = [
 {
 "op": "add",
 "path": "/fields/System.Title",
 "value": "Write Python scritps -2 "
 }
]

#Sending a Requests
r = requests.post(url, json=data, 
    headers={'Content-Type': 'application/json-patch+json',"Authorization" : f"Basic {b64}"})

print(r.json())


# Note : This code uses Base-64 authorization method inside headers to create WorkItems 