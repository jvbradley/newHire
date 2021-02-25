def generateGroupList():
    import os, subprocess
    from pathlib import Path

    # This is the organizational unit in Active Directory under which this
    # script will move users.
    sgOrganizationalUnit = 'OU=Groups-Security,DC=example,DC=example,DC=com'

    # Build a PowerShell command that will get the name of available security
    # groups from the O.U. defined above.
    #
    # Get-ADGroup -Filter 'GroupCategory -eq "Security"' -SearchBase 'OU=Groups-Security,DC=example,DC=example,DC=com' | Select -ExpandProperty Name
    adSecurityGroups = "Get-ADGroup -Filter "
    adSecurityGroups += '\'GroupCategory -eq "Security"\' -SearchBase \''
    adSecurityGroups += 'OU=Groups-Security,DC=example,DC=example,DC=com\''
    adSecurityGroups += ' | Select -ExpandProperty Name'

    # Generate a PowerShell script to list groups.
    scriptText = "Function Get-AdGroups() {\n"
    scriptText += "   # This file is safe to delete.\n"
    scriptText += "   # Argument definition\n"
    scriptText += "   $ouSecurityGroups = '" + sgOrganizationalUnit + "'\n"
    scriptText += "   $sgLocated = " + adSecurityGroups + "\n"
    scriptText += "   return $sgLocated" + "\n"
    scriptText += "\n"
    scriptText += "}"
    scriptText += "\n\nGet-AdGroups"

    # Save the above PowerShell script as a file in the home directory of the
    # person running the script.
    scriptListGroups = os.path.join(Path.home(), 'nhSelectGroups.ps1')
    slgOpen = open(scriptListGroups, 'w')
    slgOpen.write(scriptText)
    slgOpen.close()

    # Run the script, and then format/return the result.
    getGroupList = subprocess.run(['powershell.exe', os.path.join(Path.home(), 'nhSelectGroups.ps1')], stdout = subprocess.PIPE)
    groupsListed = str(getGroupList.stdout)
    listedGroups = groupsListed[2:-1].split('\\r\\n')
    listedGroups.remove('')
    return listedGroups

def menuGroups(groupsAvailable):
    # Build and return the menu of groups.
    import pyinputplus as pyip
    groupsMenu = pyip.inputMenu(groupsAvailable, numbered = True, lettered = False, blank = False)
    return groupsMenu

def groupManager():
    # This is the primary function of this module.  Its purpose is to call the
    # groupsAvailable() function, build a menu from which the user may select
    # groups to which the new account should belong, and return the selected
    # groups to the primary function.
    import pyinputplus as pyip

    # Quick introduction on how to use this section.
    groupInfo = '\nOne prompt = one response.  Select one group by number and press [ENTER].'
    groupInfo += '\nYou will be asked if you want to select additional groups.\n'
    print(groupInfo)

    # Go fetch me a group list.
    groupsAvailable = generateGroupList()
    groupsAvailable.append('Continue to Next Step')

    # Security groups selected by the user, stored as a list object.
    groupsSelected = []

    # This section of the script will run until all groups are selected or
    # the user selects the 'Continue to Next Step' step.
    while len(groupsSelected) < len(groupsAvailable):
        selectedGroup = menuGroups(groupsAvailable)
        if 'Continue to Next Step' not in selectedGroup:
            if selectedGroup in groupsSelected:
                print('\n\tNaughty, naughty!  You have already selected \'' + selectedGroup + '\' from the list.\n')
                continue
            if selectedGroup not in groupsSelected:
                groupsSelected.append(selectedGroup)
        elif 'Continue to Next Step' in selectedGroup:
            return groupsSelected
