import requests, json, base64, sys, yaml, os, subprocess
import xml.etree.ElementTree as ET
PAT = "DOIAp4Pfhp7RahDs5sSOrbnJx6y5LWqYMCK1Rn7tEVUdisolZBYmJQQJ99BBACAAAAAXbmUZAAASAZDO2ysZ"

def ADO_login(PAT):
    username = ''
    login_info = username + ":" + PAT
    b64 = base64.b64encode(login_info.encode()).decode()
    return b64


def create_workItem(organization,project):
    b64 = ADO_login(PAT)
    # some variables 
    workItem_title = "Sample workitem for testing automation"
    #URI
    # url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$task?api-version=5.1'
    url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Task?api-version=5.1'

    # Body of the requests 
    data = [
    {
    "op": "add",
    "path": "/fields/System.Title",
    "value": workItem_title
    }
    ]

    #Sending a Requests
    r = requests.post(url, json=data, 
        headers={'Content-Type': 'application/json-patch+json',"Authorization" : f"Basic {b64}"})

    if r.status_code in (200, 201):  # Check for 200 or 201
        try:
            response_data = r.json()
            workitem_id = response_data.get('id')  # Extract the ID
            if workitem_id:
                print(f"Work item successfully created. ID: {workitem_id}")
                return workitem_id # Return the ID
            else:
                print("Work item created, but ID not found in response.") # Handle case where ID is missing
                print(response_data) # print the full response
                return None
        except json.JSONDecodeError:
            print("Work item created, but response was not valid JSON")
            print(r.text)
            return None
    else:
        print(f"Error creating work item. Status code: {r.status_code}")
        try:
            error_data = r.json()
            print(f"Error details: {error_data}")
        except json.JSONDecodeError:
            print(f"Response content: {r.text}")
        return None  # Return None on error


def xml_handler(xmlfilepath, updateby=0.001):
    # Load XML file
    xml_file = xmlfilepath  # Ensure the correct file path

    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()  # Root itself is <BuildNumber>
    print(root)
    # Debug: Print the XML structure
    print("Root tag:", root.tag)
    print("Current BuildNumber value:", root.text)

    # Update the build number by adding 0.001
    try:
        build_number = float(root.text)  # Convert text to float
        build_number += updateby  # Increment by 0.001
        root.text = f"{build_number:.3f}"  # Keep 3 decimal places

        # Save changes back to XML file
        tree.write(xml_file, encoding="utf-8", xml_declaration=True)
        print("Updated BuildNumber:", root.text)
        print("Build number updated successfully.")
    except ValueError:
        print("Error: BuildNumber is not a valid number.")


def yaml_handler(yamlfilepath, updateby=1):

    # Load YAML file
    yaml_file = yamlfilepath  # Change this to your actual YAML file name

    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)  # Parse YAML file

    # Debug: Print the original YAML content
    print("Original YAML Data:", data)

    # Update the 'Minor' value
    if "variables" in data and "Minor" in data["variables"]:
        data["variables"]["Minor"] += updateby  # Increment by 1

        # Save changes back to the YAML file
        with open(yaml_file, "w") as file:
            yaml.dump(data, file, default_flow_style=False)

        print("Updated Minor:", data["variables"]["Minor"])
        print("Minor version updated successfully.")
    else:
        print("Error: 'variables' or 'Minor' key not found in YAML.")

def pr_raiser_ADO(organization,project, repoID, ADO_PAT, topicbranch, defaultbranch, prtitle, prdescp):
    
    # Some variable definitions
    SOURCE_BRANCH = topicbranch
    TARGET_BRANCH = defaultbranch
    PR_TITLE, PR_DESCRIPTION = prtitle, prdescp

    auth_header = base64.b64encode(f":{ADO_PAT}".encode()).decode()
    # API URL
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repoID}/pullrequests?api-version=7.0"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_header}",
    }

    pr_data = {
        "sourceRefName": f"refs/heads/{SOURCE_BRANCH}",
        "targetRefName": f"refs/heads/{TARGET_BRANCH}",
        "title": PR_TITLE,
        "description": PR_DESCRIPTION,
    }

    response = requests.post(url, headers=headers, data=json.dumps(pr_data))

    if response.status_code == 201:
        print(" PR Created Successfully!")
        print(" PR URL:", response.json().get("url"))
    else:
        print(" Failed to create PR:", response.status_code, response.text)

def pr_raiser_ADO_extended(organization,project, repoID, ADO_PAT, topicbranch, defaultbranch):
    
    # Some variable definitions
    SOURCE_BRANCH = topicbranch
    TARGET_BRANCH = defaultbranch
    PR_TITLE, PR_DESCRIPTION = "", ""

    auth_header = base64.b64encode(f":{ADO_PAT}".encode()).decode()
    # API URL
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repoID}/pullrequests?api-version=7.0"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_header}",
    }

    pr_data = {
        "sourceRefName": f"refs/heads/{SOURCE_BRANCH}",
        "targetRefName": f"refs/heads/{TARGET_BRANCH}",
        "title": PR_TITLE,
        "description": PR_DESCRIPTION,
    }

    response = requests.post(url, headers=headers, data=json.dumps(pr_data))

    if response.status_code == 201:
        print(" PR Created Successfully!")
        print("PR URL:", response.json().get("url"))
    else:
        print("Failed to create PR:", response.status_code, response.text)
    # Add autocomplete codes below and wit updater as well

def update_workitem_to_pr():
    pass


def set_pr_autoComplete():
    pass