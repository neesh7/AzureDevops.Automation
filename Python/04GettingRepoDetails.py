import requests, json, base64, sys


#Login Details, provide pat as system argument during program exection or pipeline arguments 
PAT = sys.argv[1]
#Note: Username can be an empty string and Password will be your PAT
username = ''
login_info = username + ":" + PAT
#Base 64 Encoding for Azure Devops Authorization 
b64 = base64.b64encode(login_info.encode()).decode()

organization, project, repositoryId ="" ,"", ""
#Note: If Repo id is unknown pass the repo name itself 
#Getting Repository details and Project details as well, like Project ID and Repo ID 
#https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}?api-version=4.1
url = f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}?api-version=4.1'

# Pass the Headers in get requests
response = requests.get(url, 
    headers={'Content-Type': 'application/json-patch+json',"Authorization" : f"Basic {b64}"})
#Printing the response 
print(response.json())