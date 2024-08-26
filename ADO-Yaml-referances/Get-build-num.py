import requests, json, base64, sys

# All Command Line args is provided here 

PAT = sys.argv[1]
weeklybranch = f"refs/heads/{sys.argv[2]}"
OfficialBuild = sys.argv[3]
BuildReason = sys.argv[4]
SourcePublishBuild_BuildNumber = sys.argv[5]
SourcePublishBuild_BuildBranch = sys.argv[6]
SourcePublishBuild_Build_id = sys.argv[7]
#############

print("Official build id is ",OfficialBuild)
print("Build Reason and it's type is: ",BuildReason, type(BuildReason))
print("Source pipeline publish build number",SourcePublishBuild_BuildNumber)

# Variable declaration

organization, project, definationID = "", "", OfficialBuild

#Login Details 
username = ''
login_info = username + ":" + PAT
#Base 64 Encoding for Azure Devops Authorization 
b64 = base64.b64encode(login_info.encode()).decode()
# weeklyBranch = f"refs/heads/{weeklybranch}"
weeklyBranch_vg = f"{weeklybranch}"



def scheduled_trigger(organization, project, OfficialBuild, weeklybranch_vg):
    #URI
    organization, project, definationID, weeklybranch = organization, project, OfficialBuild, weeklybranch_vg
    # url = f"https://dev.azure.com/{organization}/{project}/_apis/build/builds?definitions={definationID}&api-version=7.1-preview.7"
    # only Successfull build will be selected as per api filter
    url = f"https://dev.azure.com/{organization}/{project}/_apis/build/builds?definitions={OfficialBuild}&resultFilter=succeeded&branchName={weeklybranch}&api-version=7.2-preview.7"

    #Sending a Requests
    r = requests.get(url =url,headers={"Authorization" : f"Basic {b64}"}).json()

    Build_count = r["count"]
    #########
    if Build_count != 0:
        print(r["value"][0]["buildNumber"])
        uptake_version = r["value"][0]["buildNumber"]
        buildID = r["value"][0]["id"]
        print(f"Scheduled Build, Uptake Build Number : {uptake_version} is from weekly branch: {weeklybranch}")
        print(f"https://dev.azure.com/{organization}/{project}/_build/results?buildId={buildID}&view=results")
        print(f"##vso[task.setvariable variable=uptakeBuild]{uptake_version}")
        print(f"##vso[task.setvariable variable=uptakeBranch]{weeklybranch}")
    else:
        print(f"Didn't find any valid build over provided branch {weeklyBranch}")
        print(f"Total number of Builds over this branch {weeklyBranch} is {Build_count}")
        print("CancelBuild")

def manual_trigger(organization, project, SourceBuildNumber, SourceBuildBranch, SourcePublishBuild_Build_id):
    uptake_version = SourceBuildNumber
    SourceBranch = SourceBuildBranch
    print(f"Manual Build, Uptake Build Number : {uptake_version} is from branch: {SourceBranch}")
    print(f"https://dev.azure.com/{organization}/{project}/_build/results?buildId={SourcePublishBuild_Build_id}&view=results")
    print(f"##vso[task.setvariable variable=uptakeBuild]{SourceBuildNumber}")
    print(f"##vso[task.setvariable variable=uptakeBranch]{SourceBuildBranch}")
    
if BuildReason == "Manual":
    manual_trigger(organization, project, SourcePublishBuild_BuildNumber, SourcePublishBuild_BuildBranch, SourcePublishBuild_Build_id)
elif BuildReason == "IndividualCI":
    scheduled_trigger(organization, project, OfficialBuild, weeklybranch_vg)

#Printing the json response. Also Please use json editor to better process through the response: https://jsoneditoronline.org/
# print(r)

# Use $(uptakeBuild) and $(uptakeBuild) in upcoming tasks
