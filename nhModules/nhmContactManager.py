def setAddress():
    # This function structures the CompanyName corporate address and returns it
    # as a list value to the contactManager() function.
    addressStreet1 = '1 Main Street'
    addressStreet2 = 'Suite 100'
    addressCity = 'Anytown'
    addressState = 'NY'
    addressZip = '55100-5500'

    addressInformation = [addressStreet1, addressStreet2, addressCity, addressState, addressZip]
    return addressInformation

def requestPhoneNumber():
    # This function prompts for a telephone number and returns it.
    import pyinputplus as pyip
    phoneNumber = pyip.inputStr(prompt = '\nTelephone number: ')
    return phoneNumber

def setPhoneNumber():
    # Module Information
    pnInfo = '\n\tEnter a ten digit telephone number for the new employee.  You may use '
    pnInfo += '\n\tparentheses, periods, and/or hypens; please avoid using spaces.  Blank '
    pnInfo += '\n\tresponses will be rejected.'
    print(pnInfo)

    # Import modules for regular expression and input verification.
    import re
    import pyinputplus as pyip

    # Build regular expression for telephone numbers.  Prompt for and search.
    phoneNumberRegex = re.compile('(\(?)(\d{3})(.?|-?)(\s?)(\d{3})(.?|-?)(\d{4})')

    # Variable creation, empty string value to old the formatted telephone number.
    pnFormatted = str()

    # Request a telephone number and ensure that it fits the expected format.
    # pnRegexSearch will search the returned value.  This function will call the
    # requestPhoneNumber() function until it is provided with a telephone number
    # that fits its format.
    phoneNumber = requestPhoneNumber()
    pnRegexSearch = phoneNumberRegex.findall(phoneNumber)
    if len(pnRegexSearch) == 0:
        print('\n\tUnexpectedly formatted response: try again.')
        requestPhoneNumber()

    # This part of the function will look at each group returned and attempt
    # to convert that data from string to integer.  If it fails, it indicates
    # that it is an appropriate spot for a hyphen.
    for pnSection in pnRegexSearch:
        for strObject in pnSection:
            try:
                intObject = int(strObject)
                pnFormatted += str(intObject) + '-'
            except ValueError:
                continue

    # This drops the first and last characters from the string data.  They are
    # unnecessary hypens.  This is a string variable.
    pnFormatted = pnFormatted[0:-1]

    # Prompt for extension and require a three-digit numeric response.
    extYN = pyip.inputYesNo('Does this employee have an extension assigned? ', blank = False)

    # If the new employee has an extension associated with the office telephone
    # number, the user will be prompted and required to provide a three-digit
    # extension number.
    if extYN == 'yes':
        pnExtension = pyip.inputInt('Enter the three digit extension: ', blank = False, allowRegexes = [r'\d{3}'])
        pnFormatted += ', ext. ' + str(pnExtension)

    return pnFormatted

def contactManager():
    # This module receives a request from the main newEmployee.py script.  It
    # runs two functions in this module to return a list value of the address
    # and the telephone number.

    addressInformation = setAddress()
    phoneInformation = setPhoneNumber()
    return addressInformation, phoneInformation
