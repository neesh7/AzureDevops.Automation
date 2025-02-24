import requests
import base64, json

# Configuration (Replace with your details)
ADO_ORG = "Your_orgName"
ADO_PROJECT = "Your_Projects"
REPO_NAME = "Yaml-yourRepoName.repo"
PR_ID = "22"  # Pull Request ID
WORK_ITEM_ID = "27"  # Work Item ID to attach
ADO_PAT = "your_personal_access_token"
AUTO_COMPLETE_SETBY = "6d3c98c3-de4e-6227-8623-18s66c7574cf0"  # Replace with descriptor

# Azure DevOps API Base URL
ADO_BASE_URL = f"https://dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_apis/git/repositories/{REPO_NAME}/pullRequests/{PR_ID}"

# Authentication (Basic Auth with PAT)
auth_header = base64.b64encode(f":{ADO_PAT}".encode()).decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_header}"
}

# Step 1: Set Auto-Complete on PR
def set_auto_complete():
    url = f"{ADO_BASE_URL}?api-version=7.1-preview.1"
    payload = {
        "autoCompleteSetBy": {
            "id": AUTO_COMPLETE_SETBY  # Descriptor ID
        },
        "completionOptions": {
            "deleteSourceBranch": True,
            "mergeStrategy": "squash"
        }
    }
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Auto-complete set successfully!")
    else:
        print(f" Failed to set auto-complete: {response.text}")


# Execute functions
set_auto_complete()
