import re

class emailInfo():
    def __init__(self, domain, email):
        self.domain = domain
        self.email = email

    def checkDomain(self):
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
        
        if type(self.domain) is str:
            if is_vaild_domain(domain=self.domain) == False:
                return False, 'Please Check Domain'
            result = getDomain(email=self.email)
            if result[0]:
                if result[1] == self.domain:
                    return True, 'Vaild Domain'
                else:
                    return False, 'Invaild Domain'
            else:
                return False, 'Invaild Email'
            
        elif type(self.domain) is list:
            for i in self.domain:
                if is_vaild_domain(i) == False:
                    return False, 'Please Check Domain'
            result = getDomain(email=self.email)
            if result[0]:
                if result[1] in self.domain:
                    return True, 'Vaild Domain'
                else:
                    return False, 'Invaild Domain'
            else:
                return False, 'Invaild Email'
        else:
            return False, 'Default Domain Type / Only List or String'