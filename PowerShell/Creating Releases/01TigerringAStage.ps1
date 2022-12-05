#Creating a Release
$organization, $project, $definitionId = "", "", 1

#Authentication Part
$PAT="PAT"
$base64AuthInfo= [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes(":$($PAT)"))

#Create a Release

$url = "https://vsrm.dev.azure.com/{0}/{1}/_apis/release/releases?api-version=6.1-preview.8" -f $organization, $project
$body = '{
  "definitionId": 1,
 }'

#Creating release
$releaseInfo = Invoke-RestMethod -Uri $url -Headers @{Authorization = ("Basic {0}" -f $base64AuthInfo)} -Method post -Body  $body -ContentType "application/json"
Write-Host
Write-Host $releaseInfo
Write-Host
$releaseId = $releaseInfo.id
Write-Host $releaseId
$EnvironmentIds = $releaseInfo.environments | Select-Object id
#use indexing here to refer the stage
Write-Host "Environment id $EnvironmentIds[1].id"

#Triggering Particular Stage 
$Stage2 = $EnvironmentIds[1].id
#Note: Index is 0 for triggering stage1 and index is 1 for triggering stage2
#PATCH https://vsrm.dev.azure.com/{organization}/{project}/_apis/Release/releases/{releaseId}/environments/{environmentId}?api-version=6.1-preview.7
$EnvUrl = "https://vsrm.dev.azure.com/{0}/{1}/_apis/Release/releases/{2}/environments/{3}?api-version=6.1-preview.7" -f $organization, $project, $releaseId, $Stage2
$envBody='{
    "status": "inProgress"
    }'
#Trigger the second stage
Invoke-RestMethod -Uri $EnvUrl -Headers @{Authorization = ("Basic {0}" -f $base64AuthInfo)} -Method patch -Body $envBody -ContentType "application/json"