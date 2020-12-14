#the script finds the prices of the current link and print
from urllib.request import Request, urlopen
import Parce_CSV as Csv
import bs4 as bs
import re
import time
import random
from Sent_Email import SentEmailNotification
global text
text = None
class PriceTracker():
    def __init__(self,link,carname,model,email_receiver):
        self.link = link
        self.carname = carname
        self.model=model
        self.email_receiver=email_receiver
        self.Prices = []
        self.CarLinks = []
        self.nextPageNum = 2
        req = Request(self.link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        self.soup = bs.BeautifulSoup(webpage, 'lxml')


    def FindNewCars(self):
        pass

    def FindCarPrices(self):
        # print(self.soup.find_all('h2'))
        # if class=='row-normal-price' or class==''
        # print(self.soup.find_all("span", {'class': "row-normal-price"}, itemprop=re.compile("price")))
        for value, paragraph in enumerate(self.soup.find_all("span", itemprop=re.compile("price"))):
            # print (value, '-->', paragraph.text)
            if "row-normal-price" in paragraph["class"]:  # skip elements having emptyItem class
                print('double Price value found in the tracking Link ')
                continue
            digits = re.findall(r"\d", paragraph.text)
            # print(value+1,digits)
            digits = int("".join(digits))
            self.Prices.append(digits)
            # print(self.soup.prettify())
        #print(*self.Prices, sep="\n")

    def FindCarsWithSpecificPrice(self,price):
        self.Prices.clear()
        self.CarLinks.clear()
        self.FindCarPrices()
        self.FindCarLinks()
        while self.soup.find('a', class_= "next"): #επαναάμβάνει τον έλεγχο για όλες τις σελιδες
            nextlink = self.link + f'&pg={self.nextPageNum}'
            req = Request(nextlink, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            self.soup = bs.BeautifulSoup(webpage, 'lxml')
            self.FindCarPrices()
            self.FindCarLinks()
            self.nextPageNum += 1
            time.sleep(1)
        self.nextPageNum = 1
        print(f'################# {self.carname} Results Number:{len(self.Prices)} #################')
        print(f' Prices Len: {len(self.Prices)} Carlink len: {len(self.CarLinks)}')
        emailMessage=[]
        limitedPrices=[]
        limitedCarlinks=[]
        for i, value in enumerate(self.Prices):
            if value <= price:
                try:
                    result = f'Price: {value} --> {self.CarLinks[i]}'
                    emailMessage.append(result)
                    print(result)
                    limitedPrices.append(value)
                    limitedCarlinks.append(self.CarLinks[i])
                except :
                    print('Exception Capturted CarLink length <= Price Length')
        print('##################################################')
        Csv.writeResults('DataLogs\ResultLogs.csv', self.carname,self.model,limitedPrices,limitedCarlinks,self.email_receiver)
        if not self.Prices:
            pass
            #SentEmailNotification(emailMessage,str(self.email_receiver))
        else:
            print("No car with specific cryteria was found")
        emailMessage.clear()

    def FindCarLinks(self):
        for value,a in enumerate(self.soup.find_all('a', class_= "vehicle list-group-item clsfd_list_row")):
            #print(f"{value} URL:", a['href'])
            self.CarLinks.append('car.gr'+a['href'])
            #print(CarLinks[value])

    def PrintAllPage(self):
        for price, link in zip(self.Prices, self.CarLinks):
            print(price, "-->", link)

'''########################## END OF CLASS #############################'''

startFlag = False
objectsList = []

def AddRandomTime(frequency):
    frequency = int(frequency)
    randomSum = random.expovariate(1 / 2) + random.uniform(1, 1)
    randomTime = round(randomSum,3)
    return frequency+randomTime

def Start_Tracking():
    global objectsList
    global startFlag

    print('Objects Creating...')
    linkList,nameList,modelList,frequencyList, maxPriceList,emailReceiverList = Csv.readData('DataLogs/trackingList.csv')
    for i, j in enumerate(linkList):
        object = PriceTracker(linkList[i], nameList[i],modelList[i],emailReceiverList[i])
        object.FindCarsWithSpecificPrice(int(maxPriceList[i]))
        timeDelay = AddRandomTime(frequencyList[i])
        print(f'Delay until next Tracking Search --{timeDelay}-- Seconds')
        time.sleep(timeDelay)
    Start_Tracking()

'''######################Functions info###########################'''
'''def FindNewCars(self): (future implementation)
        # save values into a text only the first time the program starts
        # In every scan check the results compared to the text
        #create text with carname as name
        #save there the logs (price , link)
        #ckeck if web scan results doesnt existn in text the return the new car

#def FindCarPrices(self): 
#βρίσκει τις τιμές των οχημάτων από την εκάστοτε σελίδα
def AddRandomTime(frequency):Αυξανει το χρόνο της καθυστέρησης που εχει επιλεξει ο 
χρήστης κατα έενα τυχάιο χρονικό διάστημα'''


"""Diaforoi kwdikes:
#obj1=PriceTracker('https://www.car.gr/classifieds/cars/?fs=1&make=251&model=828&price-from=%3E500&price-to=%\
# 3C20000&registration-from=%3E2010&engine_size-from=%3E1800&engine_size-to=%3C2000' , 'p')
#obj1.FindCarsWithSpecificPrice(40000)
#p1 = threading.Thread(target=search1.FindCarsWithSpecificPrice, args=[32000])
#p1.start()
#p1.join()
#link1 = 'https://www.car.gr/used-cars/opel/gt.html?sort=pra'  # opel Gt
#search1 = PriceTracker(link1, 'opelgt')"""