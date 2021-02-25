def createAccounts(detailsNewUser):
    # This module will take the information that the user provided and build a
    # PowerShell script to create the new account in example.com.  The
    # PowerShell script will be saved in and run from the user's home directory.
    import subprocess, os
    from pathlib import Path

    # Good morning, Vietnam!
    scriptText = "Function New-DevNetUser() {\n"
    scriptText += "   # This file is safe to delete.\n"

    # Begin of PowerShell command to create the account.
    psNewUserCMD = '     New-AdUser -Name "'
    psNewUserCMD += detailsNewUser['displayName'] + '"'
    psNewUserCMD += ' -GivenName "'
    psNewUserCMD += detailsNewUser['nameFull'][0] + '"'

    # Middle name accomodation
    if len(detailsNewUser['nameFull']) == 3:
        # Include the middle initial if it is present.
        psNewUserCMD += ' -Initials "'
        psNewUserCMD += detailsNewUser['nameFull'][1][0].title() + '."'
        psNewUserCMD += ' -Surname "'
        psNewUserCMD += detailsNewUser['nameFull'][2] + '"'
        nameDisplay = detailsNewUser['nameFull'][2] + ', ' + detailsNewUser['nameFull'][0] + detailsNewUser['nameFull'][1][0].title()
    elif len(detailsNewUser['nameFull']) == 2:
        # Otherwise, only the first and surnames are present.
        psNewUserCMD += ' -Surname "'
        psNewUserCMD += detailsNewUser['nameFull'][1] + '"'
        nameDisplay = detailsNewUser['nameFull'][1] + ', ' + detailsNewUser['nameFull'][0]
    # End, middle name logic

    psNewUserCMD += ' -DisplayName "'
    psNewUserCMD += detailsNewUser['displayName'] + '"'
    psNewUserCMD += ' -SamAccountName "'
    psNewUserCMD += detailsNewUser['samAccountName'] + '"'
    psNewUserCMD += ' -UserPrincipalName "'
    psNewUserCMD += detailsNewUser['samAccountName'] + '@example.com"'
    psNewUserCMD += ' -EmailAddress "'
    psNewUserCMD += detailsNewUser['email'] + '"'
    psNewUserCMD += ' -HomePage '
    psNewUserCMD += detailsNewUser['homePage']
    psNewUserCMD += ' -OfficePhone "'
    psNewUserCMD += detailsNewUser['telephone'] + '"'
    psNewUserCMD += ' -Department "'
    psNewUserCMD += detailsNewUser['department'] + '"'
    psNewUserCMD += ' -Title "'
    psNewUserCMD += detailsNewUser['title'] + '"'
    psNewUserCMD += ' -Description "'
    psNewUserCMD += detailsNewUser['title'] + '"'
    psNewUserCMD += ' -StreetAddress "'
    psNewUserCMD += detailsNewUser['address'][0] + '`r`n' + detailsNewUser['address'][1] + '"'
    psNewUserCMD += ' -City "'
    psNewUserCMD += detailsNewUser['address'][2] + '"'
    psNewUserCMD += ' -State "'
    psNewUserCMD += detailsNewUser['address'][3] + '"'
    psNewUserCMD += ' -PostalCode "'
    psNewUserCMD += detailsNewUser['address'][4] + '"'
    psNewUserCMD += ' -Country US'
    psNewUserCMD += ' -Company "'
    psNewUserCMD += 'Example"'
    psSetPassword = '     Set-ADAccountPassword -Identity "'
    psSetPassword += detailsNewUser['samAccountName'] + '"'
    psSetPassword += ' -NewPassword (ConvertTo-SecureString -AsPlainText "'
    psSetPassword += 'Welcome123!" -Force)'
    psEnableUser = '     Set-ADUser -Identity "'
    psEnableUser += detailsNewUser['samAccountName'] + '"'
    psEnableUser += ' -Enabled $True'
    psGetGUID = '     $objectID = Get-AdUser -Identity '
    psGetGUID += detailsNewUser['samAccountName'] + ' | Select -ExpandProperty DistinguishedName'
    psMoveUser = '     Move-ADObject -Identity "'
    psMoveUser += '$objectID' + '" -TargetPath "OU=Users,DC=example,DC=com"'
    # End of PowerShell logic for new account creation and management.

    # Save the above PowerShell script as a file in the home directory of the
    # person running the script.
    scriptNewAccount = os.path.join(Path.home(), 'nhCreateAccount.ps1')
    snaOpen = open(scriptNewAccount, 'w')
    snaOpen.write(scriptText + '\n')
    snaOpen.write(psNewUserCMD + '\n')
    snaOpen.write(psSetPassword + '\n')
    snaOpen.write(psEnableUser + '\n')
    snaOpen.write(psGetGUID + '\n')
    snaOpen.write(psMoveUser + '\n')
    if len(detailsNewUser['groupsMembership']) > 0:
        for groupSecurity in detailsNewUser['groupsMembership']:
            psCMDu = '     $userName = Get-ADUser -Identity ' + detailsNewUser['samAccountName'] + ' | Select -ExpandProperty DistinguishedName'
            psCMDg = '     $groupName = Get-ADGroup -Identity ' + groupSecurity + ' | Select -ExpandProperty DistinguishedName'
            psCMD = '     Add-ADGroupMember -Identity $groupName -Members $userName'
            snaOpen.write(psCMDu + '\n')
            snaOpen.write(psCMDg + '\n')
            snaOpen.write(psCMD + '\n')
    snaOpen.write(psMoveUser + '\n')

    psEndScript = '\n}\n\n'
    psEndScript += 'New-DevNetuser'
    snaOpen.write(psEndScript + '\n')
    snaOpen.close()

    # Run the script.
    subprocess.run(['powershell.exe', os.path.join(Path.home(), 'nhCreateAccount.ps1')], stdout = subprocess.PIPE)

    # Confirm account creation by pulling its information from Active Directory.
    # adAccountCheck = subprocess.run(['powershell.exe', 'Get-AdUser -Identity ' + detailsNewUser['samAccountName'] + ' -Properties * | Select *' ], stdout = subprocess.PIPE)
    print('\n * Script completed: confirm existence of user account in Active Directory.')
