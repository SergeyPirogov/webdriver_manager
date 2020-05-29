
# Sadly registry keys for chromium based browsers aren't set properly on the worker (it does on PC).
# This is why it needs to be set manually.
function set_registry_verion_key {
    param([string]$version, [string]$registryPath)
    if(!(Test-Path $registryPath))
    {
        New-Item -Path $registryPath -Force | Out-Null
        New-ItemProperty -Path $registryPath -Name version -Value $version -PropertyType String -Force | Out-Null}

    else {
        New-ItemProperty -Path $registryPath -Name version -Value $version -PropertyType String -Force | Out-Null}

    Get-ItemProperty -Path $registryPath -Name version
}

"#####################"
"Setting Registry Keys"
"#####################"

$edge_version = (Get-Item "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe").VersionInfo.FileVersion
$edge_registryPath = "HKCU:\SOFTWARE\Microsoft\Edge\BLBeacon"
set_registry_verion_key $edge_version $edge_registryPath

$cromium_version = (choco info chromium -l).Split("\n")[1]
$cromium_registryPath = "HKCU:\Software\Chromium\BLBeacon"
set_registry_verion_key $cromium_version $cromium_registryPath

$googlechrome_version = (Get-Item "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion
$googlechrome_registryPath = "HKCU:\Software\Google\Chrome\BLBeacon"
set_registry_verion_key $googlechrome_version $googlechrome_registryPath
