###############################################################################################
#######################################Approve#################################################


$Pat =$(PAT)
$PRID = $(System.PullRequest.PullRequestId)
#Authentication
$Base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}"-f"",$PAT)))

#URL
# url = ""
# $url = "https://{organization}.visualstudio.com//{project}/_apis/git/repositories/{RepoID}/pullRequests/{PRID}/reviewers/481c775e-51e8-6d2a-8b82-ab2865280ded?api-version=7.1-preview.1" -f $PRID 
$url = "https://{0}.visualstudio.com/{1}/_apis/git/repositories/{2}/pullRequests/{3}/reviewers/{4}?api-version=7.1-preview.1" -f $Organization,$Project, $RepoID, $PRID, $CodeReviewerID

#Body of request
$Body = @{
    vote =10
}
Write-Host "Approving the PR"
Invoke-RestMethod -Uri $url -ContentType "application/json" -Headers @{Authorization=("Basic {0}" -f $Base64AuthInfo)} -Method Put -Body(ConvertTo-Json -InputObject $Body)
Write-Host "Approved the PR"