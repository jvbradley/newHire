def checkNameFormat(nameFull):
    # This module ensures that the provided name only includes letters, hypen,
    # and/or a single apostrophe per surname.  O'Brien-O'Byrne works.
    for nameCheck in nameFull:                                  # Iterate each name.
        for thisCharacter in nameCheck:                         # Iterate each character in the name.
            if thisCharacter == '\'' or thisCharacter == '-':   # Ignore apostrophes and hypens.
                continue
            try:
                thisCharacter = int(thisCharacter)              # Try to convert this character to an integer.
            except ValueError:
                # This means that it was not possible to convert this
                # particular character into a numerical equivalent.  This is
                # good.
                continue
            return False
        # All tests concluded successfully.
    return True

def getName():
    # This module prompts for a first, middle, and last name.  It is able to
    # accommodate hyphenated surnames and single apostrophes.
    import pyinputplus as pyip
    import re

    # Define a regular expression that accommodates names with apostrophes and
    # a hypenated surname.

    # Regex reads as at least one letter, one apostrophe, and then multiple letters.
    # The pipe indicates 'or' - first option, or just surname entirely of letters.
    nameRegex = re.compile(r'\w{1}\'{1}\w*|\w+')

    # Prompt the user for the new account's names.
    nameFirst = pyip.inputStr('Enter the new employee\'s first (or preferred) name: ', blank = False)
    nameMiddle = pyip.inputStr('IF AVAILABLE, enter the new employee\'s middle name/initial: ', blank = True)
    nameLast = pyip.inputStr('Enter the new employee\'s surname: ', blank = False)

    # Compare the input to matches: it will only find letters, hyphens, and apostrophes.
    fnOutput = nameRegex.search(nameFirst)
    mnOutput = nameRegex.search(nameMiddle)
    lnOutput = nameRegex.findall(nameLast)

    # Hypenate the surname if there is more than one provided.
    if len(lnOutput) == 1:
        lnOutput = str(lnOutput[0].title())
    elif len(lnOutput) == 2:
        lnOutput = str(lnOutput[0].title()) + '-' + str(lnOutput[1]).title()

    # Create a list variable named 'nameFull'.
    try:
        nameFull = [fnOutput.group().title(), mnOutput.group().title(), lnOutput.title()]
        # Allow for a period after the middle initial.
        if len(nameFull[1]) == 1:
            nameFull[1] = nameFull[1] + '.'
    except AttributeError:
        # It means that no middle name as provided.
        nameFull = [fnOutput.group().title(), lnOutput.title()]
    # Toss variable 'nameFull' over to the 'checkNameFormat' function to validate a lack of integers.
    if checkNameFormat(nameFull) == True:
        # No numbers!  Sending information back to the requesting function.
        return nameFull
    elif checkNameFormat(nameFull) == False:
        # Whoops: I found a number.  Unless you are the artist formerly known as Prince,
        # names shouldn't have numbers.  Let's try again, shall we?
        print('\n\tError: This script encountered an invalidly formatted name.  Try again.\n')
        getName()
