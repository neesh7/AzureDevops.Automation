import xml.etree.ElementTree as ET
import requests, json, base64, sys


# PAT Will be supplied through Pipeline Variables 
PAT = sys.argv[1]

#Login Details 
username = ''
login_info = username + ":" + PAT
#Base 64 Encoding for Azure Devops Authorization 
b64 = base64.b64encode(login_info.encode()).decode()

#URI

#Below url fetches file from default branch only
# url = "https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{RepoID}/items?path={Path}&api-version=7.1-preview.1"

#To Fetch data from any Topic Branch use this url  
url = "https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{RepoID}/items?path={Path}&versionDescriptor.version={branchName}&api-version=7.1-preview.1"

#Sending a Requests
r = requests.get(url =url,headers={"Authorization" : f"Basic {b64}"})
print('status code','=',r)

#Reading and finding any specific thing from xml response
root = ET.fromstring(r.content)
for version in root.iter('version'):
    version = version.text
print("Package version is :",version.text)