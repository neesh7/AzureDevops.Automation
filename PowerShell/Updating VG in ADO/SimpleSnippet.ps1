#getting pipeline variable
$name = "$(Name)"
#setting environment variable 
Write-Host ("##vso[task.setvariable variable=VGval1;]$name")