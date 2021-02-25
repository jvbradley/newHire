def newEmployee():
    # Import modules.
    import pyinputplus as pyip
    import os
    from nhModules import nhmGetName
    from nhModules import nhmDepartmentTitle
    from nhModules import nhmContactManager
    from nhModules import nhmUserChecker
    from nhModules import nhmGroupManager
    from nhModules import nhmCreateAccounts

    # Welcome text.
    bannerText = 'Company Name: New Employee Script'
    introText = '\n\tThis script was created to facilitate the creation of new '
    introText += '\n\tusers on the domain example.com.  You will be '
    introText += '\n\tprompted to confirm the details that you enter before the '
    introText += '\n\taccount is created.  This script creates the account in '
    introText += '\n\tActive Directory and populates it with most of the minimum '
    introText += '\n\tdata. Passwords are set to Welcome123! (exclamation point '
    introText += '\n\tincluded).\n'
    print('\n' + bannerText.center(80))
    print(introText)

    # List value: first name, middle name, surname
    nameFull = nhmGetName.getName()

    # Set a display name for Active Directory.
    if len(nameFull) == 3:
        nameDisplay = nameFull[2] + ', ' + nameFull[0] + ' ' + nameFull[1][0] + '.'
    elif len(nameFull) == 2:
        nameDisplay = nameFull[1] + ', ' + nameFull[0]

    # Set phone number and address.
    addressInformation, phoneInformation = nhmContactManager.contactManager()

    # Set department, department SharePoint site, and job title; value returned as a list.
    workHorse = nhmDepartmentTitle.workHorse()

    # Verify availability of the username; value return as a string.
    username = nhmUserChecker.userChecker(nameFull)

    # Set the e-mail address based on the returned available username.
    email = username + '@example.com'

    # Let's select a few groups.  This returns a list object by calling the
    # groupManager() function in the nhmGroupManager module.
    groupsSecurity = nhmGroupManager.groupManager()

    # Format the data to pass it to subsequent functions as a single variable.
    # Create a dictionary variable, populate it, and then review/confirm the
    # accuracy of the information.  An answer in the negative clears the data
    # and restarts this script.
    print('\n')
    detailsNewUser = {}
    detailsNewUser['displayName'] = nameDisplay
    detailsNewUser['samAccountName'] = username
    detailsNewUser['email'] = email
    detailsNewUser['telephone'] = phoneInformation
    detailsNewUser['title'] = workHorse[2]
    detailsNewUser['department'] = workHorse[0]
    detailsNewUser['homePage'] = workHorse[1]
    detailsNewUser['groupsMembership'] = groupsSecurity
    detailsNewUser['nameFull'] = nameFull
    detailsNewUser['address'] = addressInformation
    for k, v in detailsNewUser.items():
        print(k.ljust(20) + '\t' + str(v))

    print('\nAre the details correct as listed above?')
    correctYN = pyip.inputYesNo('You can change information by answering \'no\' to restart the script: ', blank = False)
    if correctYN == 'no':
        del detailsNewUser
        os.system('cls')
        print('Cleared data.  Restarted script.')
        newEmployee()
    elif correctYN == 'yes':
        # Information validated by user.  Moving to create accounts.
        nhmCreateAccounts.createAccounts(detailsNewUser)

newEmployee()
