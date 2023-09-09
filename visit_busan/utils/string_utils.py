
def check_passwd_rule(passwd):
    if (len(passwd) < 8):
        return False
    
    check_alpha = False
    check_num = False
    
    for p in passwd:
        if check_alpha and check_num:
            return True
        
        if p.isdigit():
            check_num = True
        elif p.isalpha():
            check_alpha = True
        else:
            if p not in ['!@#$%^&*']:
                return False
    if check_alpha and check_num:
        return True