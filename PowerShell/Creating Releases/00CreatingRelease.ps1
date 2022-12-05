$organization, $project = "", ""

#Autorization
$PAT="Provide your Pat as Env Variable: "
$base64AuthInfo= [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes(":$($PAT)"))

$url = "https://vsrm.dev.azure.com/{0}/{1}/_apis/release/releases?api-version=6.1-preview.8" -f $organization, $project
$body = '{
  "definitionId": 1,
 }'

#Create a release API Call
$releaseInfo = Invoke-RestMethod -Uri $url -Headers @{Authorization = ("Basic {0}" -f $base64AuthInfo)} -Method post -Body  $body -ContentType "application/json"
Write-Host
$releaseId = $releaseInfo.id
Write-Host "Release Id of the release that got created is : $releaseId"