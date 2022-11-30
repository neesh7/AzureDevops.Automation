#This is Pipeline Code
#Login Part
$Pat =$(PAT)
#Authentication
$Base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}"-f"",$PAT)))

# Use Try catch Block to avoid Pipeline Failures
try {
#Getting Pr ID through Pre-defined Variable 
$PRID = $(System.PullRequest.PullRequestId)

#Api Call
#Follow this Link to learn more
#https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.0&tabs=HTTP
$url = "https://dev.azure.com/{organization}/{project}/_apis/git/pullrequests/{0}?api-version=7.0"  -f $PRID
$response = Invoke-RestMethod -Uri $url -Method Get -ContentType "application/json" -Headers @{Authorization=("Basic {0}" -f $Base64AuthInfo)}
#Getting objects out of json for later comparision
write-host "writing PR title"
write-host $response.title 
$targetbranchname, $status, $title = $response.targetRefName,$response.status,$response.title
write-host $targetbranchname 
#Checks, using multiple and to compare multiple conditions
#condition 1: Branch check
#condition 2: Title Check 
#condition 3: Status of Pr check
$BranchCheck = $targetbranchname.Contains("main")
$StatusCheck = $status.Contains("active")
$TitleCheck = $title.Contains("Owners")
# Write-Host $StatusCheck $TitleCheck
if (($BranchCheck) -and ($StatusCheck) -and ($TitleCheck))
{
    Write-Host "PR TITLE: $title"
    Write-Host "Pull Request $PRID status is $status"
    Write-Host "All Required Checks Passed"
    Write-Host "Pull Request $title will be approved in next step"
    #use this variable in Custom Conditions of Pipeline 
    #custom condition for next task will be (Approval Code) --> 01Approval.ps1
    # and(succeeded(), eq(variables['AutoApprovePR'], 'yes'))
    Write-Host "##vso[task.setvariable variable=AutoApprovePR;]yes"
}
else
{
    Write-Host "Required checks Failed Hence Pr will not be approved Automatically"
}
}
catch {
    {Write-Host "Exception Occured. This Build Doesn't have any PRID"}
}