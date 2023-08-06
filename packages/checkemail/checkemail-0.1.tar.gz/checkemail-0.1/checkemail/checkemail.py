import re

def checkDomain(domain, email):
    def getDomain(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        isEmail = re.match(pattern, email)
        if isEmail:
            domain = email.split('@')[1]
            return True, domain
        else:
            return False, 'Invaild Email'
    
    def is_vaild_domain(domain):
        pattern = r"^(?=.{1,253}\.)[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.([a-zA-Z]{2,})$"
        return bool(re.match(pattern, domain))

    if type(domain) is str:
        if is_vaild_domain(domain=domain) == False:
            return False, 'Please Check Domain'
        result = getDomain(email=email)
        if result[0]:
            if result[1] == domain:
                return True, 'Vaild Domain'
            else:
                return False, 'Invaild Domain'
        else:
            return False, 'Invaild Email'
        
    elif type(domain) is list:
        for i in domain:
            if is_vaild_domain(i) == False:
                return False, 'Please Check Domain'
        result = getDomain(email=email)
        if result[0]:
            if result[1] in domain:
                return True, 'Vaild Domain'
            else:
                return False, 'Invaild Domain'
        else:
            return False, 'Invaild Email'
    else:
        return False, 'Default Domain Type / Only List or String'