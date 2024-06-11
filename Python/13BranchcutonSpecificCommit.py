import requests, json, base64, sys

# Declare variables
# neesh90900/DevOps_Projects/_git/node-todo-cicd
PAT = "Enter_Your_PAT"
organization, project = "org","Project"
new_branch_name = "test226"
baseCommitID = "f6dd12563bc2082a37dfec00cf61e9deb01b17d0"
repositoryId = "my_daily_repo"
default_branch_name = "main"
# b64 authentication
b64auth = base64.b64encode(f":{PAT}".encode('ascii')).decode('ascii')

def get_commit():        
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/refs?filter=heads/{default_branch_name}&api-version=7.2-preview.2"
    response = requests.get(url =url,headers={"Authorization" : f"Basic {b64auth}"})
    if response.status_code == 200:
        response = response.json()
        commitID = response["value"][0]["objectId"]
        print(f"{default_branch_name} is pointing at commit {commitID}")
        return commitID
    else:
        print(f"Api call resulted in status_Code{response.status_code}")
        return None
    
def create_new_branch(new_branch_name,baseCommitID):
    # API URL
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/refs?api-version=7.2-preview.2"
    # Headers including the personal access token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {b64auth}"
    }
    # Request Body
    payload = [
    {
        "name": f"refs/heads/{new_branch_name}",
        "oldObjectId": "0000000000000000000000000000000000000000",
        "newObjectId": f"{baseCommitID}"
    }
    ]
    # Call API
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check the response
    if response.status_code in [200, 201]:
        print("Branch creation response:")
        print(response.json())
        # Check if the updateStatus is succeeded
        result = response.json().get('value', [])[0]
        if result.get('updateStatus') == 'succeeded' and result.get('success'):
            print(f"Branch '{new_branch_name}' created successfully in repository '{repositoryId}'.")
        else:
            print(f"Branch creation failed with update status: {result.get('updateStatus')}")
    else:
        print(f"Failed with status code {response.status_code}")
        print(response.text)

# Driver Code here
basecommitid = get_commit()
create_new_branch(new_branch_name,basecommitid)