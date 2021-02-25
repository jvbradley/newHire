def userChecker(nameFull):
    # This module generates a PowerShell script to validate the availability of
    # a username based on current Key Methods standardss.
    import os, subprocess
    from pathlib import Path

    # Based on the name provided, create a primary user ID that follows the
    # corporate standard of "first name, last initial".  Create an alternative
    # of "first initial, last name".
    usernamePreferred = nameFull[0].lower() + nameFull[-1][0].lower()
    usernameAlternate = nameFull[0][0].lower() + nameFull[-1].lower()

    # Generate a PowerShell script to verify username availability.
    scriptText = "Function Get-AdUserStatus() {\n"
    scriptText += "   # This file is safe to delete.\n"
    scriptText += "   # Argument definition\n"
    scriptText += "   $usernamePreferred = '" + usernamePreferred + "'\n"
    scriptText += "   $usernameAlternate = '" + usernameAlternate + "'\n"
    scriptText += "   $preferredExists = Get-AdUser -Filter 'SamAccountName -eq $usernamePreferred'\n"
    scriptText += "   $alternateExists = Get-AdUser -Filter 'SamAccountName -eq $usernameAlternate'\n"
    scriptText += "\n"
    scriptText += "   If ($preferredExists.samAccountName -eq $usernamePreferred) {\n"
    scriptText += "       If ($alternateExists.samAccountName -eq $usernameAlternate) {\n"
    scriptText += "           # If the preferred and alternate usernames are in use, this script will fail.\n"
    scriptText += "           return $FALSE\n"
    scriptText += "       } ElseIf ($alternateExists.samAccountName -ne $usernameAlternate) {\n"
    scriptText += "           # If the preferred username is in use and the alternate is available, the alternate is returned.\n"
    scriptText += "           return $usernameAlternate\n"
    scriptText += "       }\n"
    scriptText += "   }\n"
    scriptText += "\n"
    scriptText += "   If ($preferredExists.samAccountName -ne $usernamePreferred) {\n"
    scriptText += "       # Our preferred username is available.\n"
    scriptText += "       return $usernamePreferred\n"
    scriptText += "   }\n"
    scriptText += "}"
    scriptText += "\n\nGet-AdUserStatus"

    # Save the above PowerShell script as a file in the home directory of the
    # person running the script.
    userCheckScript = os.path.join(Path.home(), 'checkUserNames.ps1')
    ucsOpen = open(userCheckScript, 'w')
    ucsOpen.write(scriptText)
    ucsOpen.close()

    # Run the script, and then format/return the result.  The returned data is
    # a string retrieved from checking for name availability in Active Directory.
    # The formatted result removes some additional PowerShell formatting tags.
    checkUserName = subprocess.run(['powershell.exe', os.path.join(Path.home(), 'checkUserNames.ps1')], stdout = subprocess.PIPE)
    strCUNResult = str(checkUserName.stdout)
    return strCUNResult[2:-5]
