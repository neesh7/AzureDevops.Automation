import requests, json, base64, sys


# PAT Will be supplied through Command Line arguments 
PAT = sys.argv[1]
weeklybranch = f"refs/heads/{sys.argv[2]}"


#Login Details 
username = ''
login_info = username + ":" + PAT
#Base 64 Encoding for Azure Devops Authorization 
b64 = base64.b64encode(login_info.encode()).decode()
weeklyBranch = f"refs/heads/{weeklybranch}"
OfficialBuild = "9"

#URI
organization, project, definationID = "org", "proj", OfficialBuild
# url = f"https://dev.azure.com/{organization}/{project}/_apis/build/builds?definitions={definationID}&api-version=7.1-preview.7"
url = f"https://dev.azure.com/{organization}/{project}/_apis/build/builds?definitions={OfficialBuild}&resultFilter=succeeded&branchName={weeklybranch}&api-version=7.2-preview.7"

#Sending a Requests
r = requests.get(url =url,headers={"Authorization" : f"Basic {b64}"}).json()

Build_count = r["count"]
#########
if Build_count != 0:
    print(r["value"][0]["buildNumber"])
    uptake_version = r["value"][0]["buildNumber"]
    print(f"##vso[task.setvariable variable=uptakeBuild]{uptake_version}")
else:
    print(f"Didn't find any valid build over provided branch {weeklyBranch}")
    print(f"Total number of Builds over this branch {weeklyBranch} is {Build_count}")

#Printing the json response. Also Please use json editor to better process through the response: https://jsoneditoronline.org/
# print(r)