import os
import requests, json, base64, sys

PAT = sys.argv[1]

organization, project, groupIds = "" ,"DeOps_Projects", 121

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
    print(json.dumps(response.json()["value"][0]["variables"], indent = 4))
    return my_vg_data


def updateVG(organization, project, groupIds):
    b64auth = ADO_login(PAT)

    # Hitting this function we will get the existing vg in json format
    existing_vars = getVG(organization, project, groupIds)

    # These are new VG updates we are planning to introduce
    updated_vars = {
    "weeklybranch": {"isSecret": False, "value": "releases/2401.24999"},
    # "myPAT": {"isSecret": True, "value": "NEW_SECRET_VALUE"}
    }
    
    # Merge updates - Updating VG with new variable data ( existing vars + updated vars)
    existing_vars.update(updated_vars)
    print(json.dumps(existing_vars, indent = 4))
    
    # Vg Update PUT url
    # url = f"https://dev.azure.com/{organization}/_apis/distributedtask/variablegroups/{groupIds}?api-version=7.1"
    url= f"https://dev.azure.com/{organization}/{project}/_apis/distributedtask/variablegroups/{groupIds}?api-version=7.1-preview.1"

    # Headers including the personal access token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {b64auth}"
    }

    # Request Body

    # vg_body = {
    #     "id": int("2"),  # Ensure this is an integer, not a string
    #     "type": "Vsts",
    #     "vgname": "myvariable-group-",
    #     "variables": {
    #         "variable1": {"isSecret": False, "value": "z"},
    #         "variable2": {"isSecret": False, "value": "w"},
    #         "variable3": {"isSecret": False, "value": "t"}
    #     }
    # }
    vg_body = {
        "id": int("2"),  # Ensure this is an integer, not a string
        "type": "Vsts",
        "name": "myvariable-group-dev",
        "variables": existing_vars
    }
    # Call API

    # Make the POST request
    response = requests.put(url, headers=headers, data=json.dumps(vg_body))
    print(json.dumps(response.json(), indent=4))

########## Driver Code ####################
updateVG(organization, project, groupIds)