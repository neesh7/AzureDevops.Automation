

import requests
import json
import base64

# 🔹 Configuration
organization = "Your_orgName"
project = "Your_Projects"
repo_name = "yourRepoName"
pr_id = "22"  # Pull Request ID
wit_id = "26"  # Work Item ID
PAT = "your_personal_access_token"

def link_wit_to_pr(pat, organization, project, repo_name, pr_id, wit_id):
    # Authentication
    HEADERS = {
        "Content-Type": "application/json-patch+json",
        "Authorization": "Basic " + base64.b64encode(f":{pat}".encode()).decode()
    }

    def get_project_id():
        """Fetches project ID using the project name"""
        url = f"https://dev.azure.com/{organization}/_apis/projects?api-version=7.1"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            projects = response.json().get("value", [])
            for proj in projects:  # ✅ Change variable name to avoid conflicts
                if proj["name"] == project:
                    return proj["id"]
        print("❌ Project not found!")
        return None

    def get_repo_id():
        """Fetches repository ID using the repository name"""
        url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=7.1"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            repos = response.json().get("value", [])
            for repo in repos:
                if repo["name"] == repo_name:  # ✅ Use repo_name instead of repo_id
                    return repo["id"]
        print("❌ Repository not found!")
        return None

    def link_work_item_to_pr():
        """Links a work item to a pull request with the correct format"""
        project_id = get_project_id()
        repository_id = get_repo_id()

        if not project_id or not repository_id:
            print("❌ Could not fetch required IDs.")
            return

        # ✅ Correct PR Artifact Link format
        PR_ARTIFACT_URL = f"vstfs:///Git/PullRequestId/{project_id}/{repository_id}/{pr_id}"

        # 🔹 Work Item URL
        WORK_ITEM_URL = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{wit_id}?api-version=7.1"

        # 🔹 Prepare request payload
        patch_data = [
            {"op": "add", "path": "/relations/-", "value": {
                "rel": "ArtifactLink",
                "url": PR_ARTIFACT_URL,
                "attributes": {"name": "Pull Request"}
            }}
        ]

        # 🔹 Send PATCH request
        response = requests.patch(WORK_ITEM_URL, headers=HEADERS, json=patch_data)

        if response.status_code == 200:
            print("✅ Work item successfully linked to Pull Request!")
        else:
            print(f"❌ Failed to link work item. Status: {response.status_code}")
            print(response.text)
     
    # 🔥 Run the linking process
    link_work_item_to_pr()

## The above function will only update the workitem with pr link but it won't update the pr -needs further investigation

## This below function isn't working yet
def link_pr_to_work_item(pat, organization, project, repo_id, pr_id, wit_id):
    """Links the Pull Request to the Work Item explicitly"""
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode(f":{pat}".encode()).decode()
    }

    # ✅ Get the Work Item URL in Azure DevOps format
    WORK_ITEM_URL = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workItems/{wit_id}"

    # ✅ Get the existing PR details
    pr_url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_id}/pullrequests/{pr_id}?api-version=7.1"
    response = requests.get(pr_url, headers=HEADERS)

    if response.status_code == 200:
        pr_data = response.json()
        existing_work_items = pr_data.get("workItemRefs", [])

        # ✅ Check if the work item is already linked
        if any(wi["id"] == wit_id for wi in existing_work_items):
            print("✅ Work item is already linked to PR!")
            return

        # ✅ Update PR with the Work Item link
        patch_data = {
            "workItemRefs": existing_work_items + [{"id": wit_id}]
        }

        response = requests.patch(pr_url, headers=HEADERS, json=patch_data)

        if response.status_code == 200:
            print("✅ Work item successfully linked to Pull Request!")
        else:
            print(f"❌ Failed to link work item to PR. Status: {response.status_code}")
            print(response.text)
    else:
        print(f"❌ Failed to fetch PR details. Status: {response.status_code}")
        print(response.text)


# 🔥 Run the script
link_wit_to_pr(PAT, organization, project, repo_name, pr_id, wit_id)
link_pr_to_work_item(PAT, organization, project, repo_name, pr_id, wit_id)
