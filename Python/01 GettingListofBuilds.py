import requests, json, base64, sys

# PAT Will be supplied through Pipeline Variables 
# PAT = sys.argv[1]
PAT = "wrfmomgzgifqp6hs2rpcntmkoedjfefklwqixcfcn446vimgua2q"
#Login Details 
username = ''
login_info = username + ":" + PAT
#Base 64 Encoding for Azure Devops Authorization 
b64 = base64.b64encode(login_info.encode()).decode()

#URI
# URL = https://dev.azure.com/{organization}/{project}/_apis/build/builds?definitions={definationID}&api-version=7.1-preview.7
url = "https://dev.azure.com/neesh9090/PythonWorks/_apis/build/builds?definitions=6&api-version=7.1-preview.7"

#Sending a Requests
r = requests.get(url =url,
    headers={"Authorization" : f"Basic {b64}"}).json()

print(r)
