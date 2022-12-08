import os
import requests, json, base64, sys

#Login Details, provide pat as system argument during program exection or pipeline arguments 
PAT = sys.argv[1]
#Note: Username can be an empty string and Password will be your PAT
username = ''
login_info = username + ":" + PAT
#Base 64 Encoding for Azure Devops Authorization 
b64 = base64.b64encode(login_info.encode()).decode()

#Creating branches through automation in azuredevops
# Follow this Link for detailed notes : https://learn.microsoft.com/en-us/rest/api/azure/devops/git/refs/update-refs?view=azure-devops-rest-5.1&tabs=HTTP
# POST https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/refs?api-version=5.1


def createAzBranch(organization, project, repositoryid,NewBranchName,commitid):

    url = f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryid}/refs?api-version=5.1'

    #Newbranchname, commit id = jidhr se commit hoga

    #Body for creating the new branch
    Body = [
    {
        "name": f"refs/heads/{NewBranchName}",
        "oldObjectId": "0000000000000000000000000000000000000000",
        "newObjectId": f"{commitid}"
    }
    ]
    # Sending Post Request to trigger the release 
    r = requests.post(url, json=Body, 
        headers={'Content-Type': 'application/json',"Authorization" : f"Basic {b64}"})
    print(r)
    print(r.text)
# print(r.json())

#call this function and pass the relevant values so it can create a new branch for you

createAzBranch("neesh9090" ,"PythonWorks","FLowTrack","users/testBranch","6d163c5739936016e07eccabda99dbe93c0c92d9")