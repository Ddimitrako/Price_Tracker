from datetime import date,datetime
import time

def checkLicence(codeString):
    #x=codeString.isnumeric()
    day=codeString[2:4]
    month=codeString[6:8]
    year=codeString[10:12]
    try:
        expiredate=day+'/'+month+'/20'+year
        today = date.today()
        # format== dd/mm/YY
        d1 = today.strftime("%d/%m/%Y")
        expireDate = time.strptime(str(expiredate), "%d/%m/%Y")
        now = time.strptime(str(d1), "%d/%m/%Y")
        if expireDate<=now or codeString==None:
            message="Your Licence has expired please renew it"
            print(message)
            return message,True
        else:
            message=f"System Activated!!! Your Licence will expire on {expiredate}"
            print(message)
            return message,False
    except:
        message="Not a valid licence. Program will terminate"
        return message,True
#Ana 2 psifia exei hmerominia to codeString
# 47 day=25 38 month=11 93 year=21 50835983
# codeString="47123808932150835983"
# checkLicence(codeString)