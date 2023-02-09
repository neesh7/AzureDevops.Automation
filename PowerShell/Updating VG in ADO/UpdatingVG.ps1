$organization, $project, $groupId = "Orgname","ProjectName", "VGID but it's an int"

#Autorization
$PAT="Enter your PAT"
$base64AuthInfo= [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes(":$($PAT)"))


# VG UPDATE URI 
$URL = "https://dev.azure.com/{0}/{1}/_apis/distributedtask/variablegroups/{2}?api-version=5.1-preview.1" -f $organization,$project, $groupId

# body of the variable group update
$body ='{
            "id":"Group Id in int","type":"Vsts","name":"VG Name",
                "variables":{

                    "Name":{"isSecret":false,"value":"$(VGval1)"},
                    "ID":{"isSecret":false,"value":"$(VGval2)"},
                    "rest-var3":{"isSecret":false,"value":"$(VGval3)"}

                            }
            }'

#VG Update API Call
$VGUpdate = Invoke-RestMethod -Uri $URL -Headers @{Authorization = ("Basic {0}" -f $base64AuthInfo)} -Method Put -Body  $body -ContentType "application/json"
Write-Host "VG Updated "


# Code by TrueShinobi

