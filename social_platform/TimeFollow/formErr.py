
def RegisterFormErrMessages(formErrors) -> list[str]:
    errList = []
    unknownErr = False
    for err in formErrors:  # Checks for specific errors in form input
        match err:
            case 'username':
                errMessage = formErrors[err][0].messages[0]
                errList += [errMessage]
            case 'phone_num':
                errList += ['Please enter a valid phone number e.g. "0123456789".']
            case 'password2':
                errMessage = formErrors[err][0].messages[0]
                errList += [errMessage]
            case _:
                unknownErr = True
    
    if unknownErr:
        errList += ['Some other input is not valid.']

    return errList