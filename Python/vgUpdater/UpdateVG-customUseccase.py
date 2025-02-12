import os
import requests, json, base64, sys
import get_updated_vars as get_newdata_vg

PAT = sys.argv[1]

# required for all ado api calls
organization, project = "", ""
# These variables needed to update the VG
groupIds, vg_name = "121" ,"my-vg"
# These variables required to read csv file remotely for ado files api
RepoID, branchName, path = "","",""

def ADO_login(PAT):
    username = ''
    login_info = username + ":" + PAT
    b64 = base64.b64encode(login_info.encode()).decode()
    return b64


def getVG(organization, project, groupIds):
    b64 = ADO_login(PAT)
    url = f"https://dev.azure.com/{organization}/{project}/_apis/distributedtask/variablegroups?groupIds={groupIds}&api-version=7.1"

    # Sending Get request to get the vg data    
    response = requests.get(url, 
        headers={'Content-Type': 'application/json-patch+json',"Authorization" : f"Basic {b64}"})
    #Printing the response 
    # print(response.json())
    my_vg_data = response.json()["value"][0]["variables"]
    print("\nBelow is the variable group data as of now\n")
    print(json.dumps(response.json()["value"][0]["variables"], indent = 4))
    return my_vg_data


def updateVG(PAT, organization, project, groupIds, vg_name, RepoID, path,branchName):
    b64auth = ADO_login(PAT)

    # Hitting this function we will get the existing vg in json format
    existing_vars = getVG(organization, project, groupIds)
    # These are new VG updates we are planning to introduce
    updated_vars = get_newdata_vg.updated_vars(PAT ,organization, project, RepoID, branchName, path)

    # updated_vars = {
    # "weeklybranch": {"isSecret": False, "value": "releases/2401.24999"},
    # # "myPAT": {"isSecret": True, "value": "NEW_SECRET_VALUE"}
    # }
    
    # Merge updates - Updating VG with new variable data ( existing vars + updated vars)
    existing_vars.update(updated_vars)
    print("\nExisitng variable data merged with incoming changes will be printed now\n")
    print(json.dumps(existing_vars, indent = 4),end="\n")
    
    # Vg Update PUT url
    # url = f"https://dev.azure.com/{organization}/_apis/distributedtask/variablegroups/{groupIds}?api-version=7.1"
    url= f"https://dev.azure.com/{organization}/{project}/_apis/distributedtask/variablegroups/{groupIds}?api-version=7.1-preview.1"

    # Headers including the personal access token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {b64auth}"
    }

    # Request Body
    vg_body = {
        "id": int("2"),  # Ensure this is an integer, not a string
        "type": "Vsts",
        "name": vg_name,
        "variables": existing_vars
    }
    # Call API

    # Make the POST request
    response = requests.put(url, headers=headers, data=json.dumps(vg_body))
    print(json.dumps(response.json(), indent=4))
    print("The VG got updated Thanks !")

########## Driver Code ####################
updateVG(PAT, organization, project, groupIds, vg_name, RepoID, path,branchName)