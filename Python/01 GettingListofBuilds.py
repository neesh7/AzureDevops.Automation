import requests, json, base64, sys



# PAT Will be supplied through Pipeline Variables 
PAT = sys.argv[1]
#Login Details 
username = ''
login_info = username + ":" + PAT
#Base 64 Encoding for Azure Devops Authorization 
b64 = base64.b64encode(login_info.encode()).decode()
#URI
organization, project, definationID = "orgname", "Project", 12121

url = f"https://dev.azure.com/{organization}/{project}/_apis/build/builds?definitions={definationID}&api-version=7.1-preview.7"
#Sending a Requests
r = requests.get(url =url,headers={"Authorization" : f"Basic {b64}"}).json()
print(r)
