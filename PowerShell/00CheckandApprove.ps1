#This is Pipeline Code
#Login Part
$Pat =$(PAT)
#Authentication
$Base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}"-f"",$PAT)))
#Getting Pr ID through Pre-defined Variable 
$PRID = $(System.PullRequest.PullRequestId)

#Api Call
#Follow this Link to learn more
#https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/get-pull-request-by-id?view=azure-devops-rest-7.0&tabs=HTTP

$url = "https://dev.azure.com/neesh9090/PythonWorks/_apis/git/pullrequests/{0}?api-version=7.0"  -f $PRID
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
}
else
{
    Write-Host "Required checks Failed Hence Pr will not be approved Automatically"
}

###############################################################################################
#######################################Approve#################################################


$Pat =$(PAT)
$PRID = $(System.PullRequest.PullRequestId)
#Authentication
$Base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}"-f"",$PAT)))

#URL
# url = ""
$url = "https://neesh9090.visualstudio.com/PythonWorks/_apis/git/repositories/AzDevops.AutomationCodes/pullRequests/{0}/reviewers/481c775e-51e8-6d2a-8b82-ab2865280ded?api-version=7.1-preview.1" -f $PRID 

#Body of request
$Body = @{
    vote =10
}
Write-Host "Approving the PR"
Invoke-RestMethod -Uri $url -ContentType "application/json" -Headers @{Authorization=("Basic {0}" -f $Base64AuthInfo)} -Method Put -Body(ConvertTo-Json -InputObject $Body)
Write-Host "Approved the PR"