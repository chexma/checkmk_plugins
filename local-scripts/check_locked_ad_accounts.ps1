

$allowList = @("aeckstein", "user2", "user3")
$UserSearchBase = "" # "CN=Users,DC=home,DC=intra" 
$warn = 2
$crit = 5

####

# Import the Active Directory module
Import-Module ActiveDirectory


if ($UserSearchBase) {
    $lockedUsers = Get-ADUser -Filter * -Properties LockedOut -SearchBase $UserSearchBase | Where-Object {$_.Enabled -like "*true*" } | Select-Object -Property SamAccountName
} else {
    $lockedUsers = Get-ADUser -Filter * -Properties LockedOut | Where-Object {$_.Enabled -like "*true*" } | Select-Object -Property SamAccountName
}

# Initialize an empty string to store locked account information
$lockedAccountsString = ""

# Concatenate locked account information to the string
foreach ($user in $lockedUsers) {
    # Check if the locked user is in the allowlist
    if ($allowList -notcontains $user.SamAccountName) {
        $lockedAccountsString += "$($user.SamAccountName), "
    }
}

if ($lockedAccountsString -ne "" ) {
    # Remove the trailing comma and space
    $lockedAccountsString = $lockedAccountsString.TrimEnd(", ")
}

# Count the number of locked accounts
$lockedAccountsCount = ($lockedAccountsString -split ',').Count

if ($lockedAccountsCount -eq 0) {
    $statuscode = 0
    $statustext = "There are no locked accounts present in Active Directory."
} else {
    if ($lockedAccountsCount -gt $crit) {
    $statuscode = 2
    } elseif ($lockedAccountsCount -gt $warn) {
    $statuscode = 1
    }
    $statustext = "There are currently $lockedAccountsCount locked accounts: $lockedAccountsString"
}

Write-Output "<<<local>>>"
Write-Output "$statuscode LockedUsers locked_count=$lockedAccountsCount $statustext"