import subprocess


# Install required Python packages
subprocess.run(["pip", "install", "PyYAML", "requests"], check=True)

import os
import json
import sys
import worker_functions as wf

# PAT = sys.argv[1]

#1 Set up variables (replace with your actual values)
PAT = "DOIAp4Pfhp7RahDs5sSOrbnJx6y5LWqYMCK1Rn7tEVUdisolZBYmJQQJ99BBACAAAAAXbmUZAAASAZDO2ysZ"
Username, UserEmail = "",""
ADO_ORG = "neesh90900"
ADO_PROJECT = "DevOps_Projects"
ADO_REPO = "Yaml-xml.repo"
TOPIC_BRANCH = "dev9"  # consider it as topic branch
TARGET_BRANCH = "main"
PR_TITLE = "Automated PR: Update BuildNumber & Minor Version"
PR_DESCRIPTION = "This PR was created automatically by an Azure DevOps Release Pipeline."
XML_FILE, YAML_FILE, version_increment_xml, version_increment_yaml = "buildnum.xml" , "build.yml", 0.001, 1
commitMessege = "Updating ..."# Personal Access Token stored as a pipeline secret
# repo url at line 40

# Assuming the source repo is added as ado artifacts, now queue the release pipeline

#2 Logic behind topic/source branch naming

#3 Navigating  to repo location
repo_path = "Yaml-xml.repo"
os.chdir(repo_path)
print("Current directory:", os.getcwd())

#4 Set up Git user

subprocess.run(["git", "config", "user.email", "neesh9090@gmail.com"], check=True)  # Replace with your actual email
subprocess.run(["git", "config", "user.name", "Avaneesh kumar"], check=True)  # Replace with your actual name

#5 Set up authentication

repo_url = f"https://{PAT}@dev.azure.com/neesh90900/DevOps_Projects/_git/Yaml-xml.repo"
# repo_url = f"https://{PAT}@dev.azure.com/{ADO_ORG}/{ADO_PROJECT}/_git/{ADO_REPO}"
subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True)

#6 Create & switch to the topic branch
subprocess.run(["git", "checkout", "-b", TOPIC_BRANCH], check=True)

#7 Run Python script to update the xml and yaml

wf.xml_handler(xmlfilepath=XML_FILE,updateby=version_increment_xml)
wf.yaml_handler(yamlfilepath=YAML_FILE,updateby=version_increment_yaml)



#8 Commit & push changes of topic branch to remote

subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", commitMessege], check=True)
subprocess.run(["git", "push", "-u", "origin", TOPIC_BRANCH], check=True)


#9 Raise pr from topic to target
wf.pr_raiser_ADO(organization=ADO_ORG , project=ADO_PROJECT, repoID=ADO_REPO, ADO_PAT=PAT, topicbranch=TOPIC_BRANCH, defaultbranch=TARGET_BRANCH, prtitle=PR_TITLE, prdescp= PR_DESCRIPTION)
# wf.pr_raiser_ADO_extended(organization=ADO_ORG , project=ADO_PROJECT, repoID=ADO_REPO, ADO_PAT=PAT, topicbranch=TOPIC_BRANCH, defaultbranch=TARGET_BRANCH)
# Now topic branch is updated with changes and we need to raise pr 

#10 create work item before raising pr
workitem_id = wf.create_workItem(organization=ADO_ORG, project=ADO_PROJECT) # Capture the returned ID
if workitem_id:
    print(f"Work item ID (outside function): {workitem_id}")
else:
    print("Work item creation failed.")


#10 update pr with workitem and set autocomplete


#11 Send Notifications to stakeholder