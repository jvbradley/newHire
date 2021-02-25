def selectDepartment():
    return listDepartments.sort()

def selectTitle():
    return listTitles.sort()

def workHorse():
    lenCenterD = len('Menu: Department Selection')
    lenCenterJ = len('Menu: Job Title Selection')
    import pyinputplus as pyip

    listDepartments = ['Customer Service', 'Technical Support', 'Accounting',
    'Sales']
    listTitles = ['Administrative Assistant', 'Network Administrator',
    'Systems Administrator', 'Developer', 'C.S. Agent', 'Lead', 'Manager',
    'Supervisor', 'Manager (Assistant)', 'Director', 'President']

    print('\n')
    print('Menu: Department Selection'.center(lenCenterD))
    selectedDepartment = pyip.inputMenu(listDepartments, numbered = True, lettered = False, blank = False)

    urlSharePoint = 'https://example.sharepoint.com/sites/'
    urlCS = 'CustomerService/'
    urlTS = 'TechnicalSupport/'
    urlAccounting = 'Accounting/'
    urlSales = 'Sales/'

    if 'Service Desk' in selectedDepartment:
        urlSharePoint = urlSharePoint + urlCS
    elif 'Centralized Services' in selectedDepartment:
        urlSharePoint = urlSharePoint + urlTS
    elif 'Operations' in selectedDepartment:
        urlSharePoint = urlSharePoint + urlAccounting
    elif 'Technical Account Management' in selectedDepartment:
        urlSharePoint = urlSharePoint + urlSales

    print('\n')
    print('Menu: Job Title Selection'.center(lenCenterJ))
    selectedTitle = pyip.inputMenu(listTitles, numbered = True, lettered = False, blank = False)
    return [selectedDepartment, urlSharePoint, selectedTitle]
