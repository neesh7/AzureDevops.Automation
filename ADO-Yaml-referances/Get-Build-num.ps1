# Accessing pipeline variables directly as environment variables
$PAT = $env:PAT
$weeklybranch = $env:weeklybranch
$BuildReason = $env:BUILD_REASON
$SourcePublishBuild_BuildNumber = $env:RESOURCES_PIPELINE_MYPIPELINE_RUNNAME
$SourcePublishBuild_BuildBranch = $env:RESOURCES_PIPELINE_MYPIPELINE_SOURCEBRANCH
$SourcePublishBuild_Build_id = $env:RESOURCES_PIPELINE_MYPIPELINE_RUNID
$weeklyBranch_vg = "refs/heads/$weeklybranch"
$OfficialBuild = 9

# Print statements
Write-Host "Official build id is $OfficialBuild"
Write-Host "Build Reason and its type is: $BuildReason", ($BuildReason.GetType().Name)
Write-Host "Source pipeline publish build number: $SourcePublishBuild_BuildNumber"

# Variable declaration
$organization, $project, $definationID = "", "", $OfficialBuild

#Authentication Part
$base64AuthInfo= [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes(":$($PAT)"))

function Scheduled-Trigger {
    param (
        [string]$organization,
        [string]$project,
        [string]$OfficialBuild,
        [string]$weeklybranch_vg
    )

    # URI
    $url = "https://dev.azure.com/$organization/$project/_apis/build/builds?definitions=$OfficialBuild&resultFilter=succeeded&branchName=$weeklybranch_vg&api-version=7.2-preview.7"

    # Sending a Request
    $response = Invoke-RestMethod -Uri $url -Headers @{ Authorization = "Basic $b64" } -Method Get

    $Build_count = $response.count

    if ($Build_count -ne 0) {
        $uptake_version = $response.value[0].buildNumber
        $buildID = $response.value[0].id
        Write-Host "Scheduled Build, Uptake Build Number: $uptake_version is from weekly branch: $weeklybranch_vg"
        Write-Host "https://dev.azure.com/$organization/$project/_build/results?buildId=$buildID&view=results"
        Write-Host "##vso[task.setvariable variable=uptakeBuild]$uptake_version"
        Write-Host "##vso[task.setvariable variable=uptakeBranch]$weeklybranch_vg"
    } else {
        Write-Host "Didn't find any valid build over provided branch $weeklybranch_vg"
        Write-Host "Total number of Builds over this branch $weeklybranch_vg is $Build_count"
        Write-Host "CancelBuild"
    }
}

function Manual-Trigger {
    param (
        [string]$organization,
        [string]$project,
        [string]$SourceBuildNumber,
        [string]$SourceBuildBranch,
        [string]$SourcePublishBuild_Build_id
    )

    $uptake_version = $SourceBuildNumber
    $SourceBranch = $SourceBuildBranch
    Write-Host "Manual Build, Uptake Build Number: $uptake_version is from branch: $SourceBranch"
    Write-Host "https://dev.azure.com/$organization/$project/_build/results?buildId=$SourcePublishBuild_Build_id&view=results"
    Write-Host "##vso[task.setvariable variable=uptakeBuild]$SourceBuildNumber"
    Write-Host "##vso[task.setvariable variable=uptakeBranch]$SourceBuildBranch"
}

if ($BuildReason -eq "Manual") {
    Manual-Trigger -organization $organization -project $project -SourceBuildNumber $SourcePublishBuild_BuildNumber -SourceBuildBranch $SourcePublishBuild_BuildBranch -SourcePublishBuild_Build_id $SourcePublishBuild_Build_id
} elseif ($BuildReason -eq "Schedule") {
    Scheduled-Trigger -organization $organization -project $project -OfficialBuild $OfficialBuild -weeklybranch_vg $weeklyBranch_vg
}
