import requests, json, base64, sys

# Declare variables
PAT = "Enter_Your_PAT"
organization, project = "org","Project"
new_branch_name = "test226"
baseCommitID = "f6dd12563bc2082a37dfec00cf61e9deb01b17d0"
repositoryId = "my_daily_repo"
default_branch_name = "main"
# b64 authentication
b64auth = base64.b64encode(f":{PAT}".encode('ascii')).decode('ascii')

# API Url
url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/refs?filter=heads/{default_branch_name}&api-version=7.2-preview.2"

# Sending a Requests
response = requests.get(url =url,headers={"Authorization" : f"Basic {b64auth}"})

# Handling Response

if response.status_code == 200:
    response = response.json()
    print("API Call Worked")
    commitID = response["value"][0]["objectId"]
    print(f"{default_branch_name} is pointing at commit {commitID}")
else:
    print(f"Api call resulted in status_Code{response.status_code}")