import csv
import os
from datetime import datetime
from Sent_Email import SentEmailNotification
global sendData
sendData=[]
global datatoConsole
datatoConsole=[]

#add data to trackingLists.csv
def addData(fileName,carName, model, link, frequency,maxPrice,emailReceiver):

    if os.path.isfile(fileName):
        with open (fileName, 'a') as csv_file:
                csv_writer = csv.writer(csv_file,lineterminator = '\n')
                data=[carName,model,link,frequency,maxPrice,emailReceiver]
                csv_writer.writerow(data)
    else:
        with open (fileName, 'w') as csv_file:
            fieldnames = ['Car_Name','Model','link','frequency','maxPrice','emailReceiver']
            dict_writer=csv.DictWriter(csv_file, fieldnames=fieldnames,lineterminator = '\n')
            dict_writer.writeheader()
            csv_writer = csv.writer(csv_file, lineterminator='\n')
            data=[carName,model,link,frequency,maxPrice,emailReceiver]
            csv_writer.writerow(data)

#read data from trackingLists.csv
def readData(fileName):
    linkList = []
    nameList = []
    modelList = []
    frequencyList = []
    maxPriceList = []
    emailReceiverList = []
    if os.path.isfile(fileName):
        with open (fileName, 'r') as csv_file:
            csv_reader = csv.reader(csv_file,lineterminator = '\n')
            next(csv_reader)
            for row in csv_reader:
                nameList.append(row[0])
                modelList.append(row[1])
                linkList.append(row[2])
                frequencyList.append(row[3])
                maxPriceList.append(row[4])
                emailReceiverList.append(row[5])
        return linkList,nameList,modelList,frequencyList, maxPriceList,emailReceiverList

def writeResults(fileName,carname,model,prices,carLinks,emailReceiver):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    if os.path.isfile(fileName):
        with open(fileName, 'r') as csv_file: #append to existed file
            csv_reader=csv.reader(csv_file,lineterminator='\n')
            for row in csv_reader:
                for i,(price,carlink) in enumerate(zip(prices,carLinks)):
                    if row[3] == carlink:
                        carLinks.remove(carlink)
                        prices.remove(price)
                        #print("car already exists in result logs file")


        with open(fileName, 'a') as csv_file:  # append to existed file
            csv_writer = csv.writer(csv_file, lineterminator='\n')
            global sendData
            sendData=[]
            for i in range(len(prices)):
                data = [carname,model,prices[i],carLinks[i],emailReceiver,dt_string]
                csv_writer.writerow(data)
                sendData.append(data)
            if not len(prices)==0:
                SentEmailNotification(sendData, emailReceiver)
                print(sendData)
                csv_writer.writerow('###########################')
                datatoConsole=sendData
                sendData.clear()

    else:
        with open(fileName, 'w') as csv_file: #create and write a new file
            fieldnames = ['Car_Name', 'Model', 'Price', 'Link', 'emailReceiver',"Date-Time"]
            dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
            dict_writer.writeheader()
            csv_writer = csv.writer(csv_file, lineterminator='\n')

            sendData = []
            for i in range(len(prices)):
                data = [carname,model,prices[i], carLinks[i],emailReceiver,dt_string]
                csv_writer.writerow(data)
                sendData.append(data)
            if not len(prices)==0:
                SentEmailNotification(sendData, emailReceiver)
                print(sendData)
                csv_writer.writerow('###########################')
                datatoConsole = sendData
                sendData.clear()

def previewFile(fileName):
    if os.path.isfile(fileName):
        print(fileName, 'exists')
        print( 'Opening ', fileName)
        os.startfile(fileName)

    else:
        print(fileName, 'doesnt exists')
        #write(fn, ' doesnt exists')



def getsendData():
    return datatoConsole
#backup codika gia eggrafh toυ pinaka sto file results
'''with open(fileName, 'a') as csv_file:  # append to existed file

    csv_writer = csv.writer(csv_file, lineterminator='\n')
    csv_writer.writerow('###########################')
    for i in range(len(prices)):
        data = [carname, model, prices[i], carLinks[i]]
        csv_writer.writerow(data)'''



#def addData: Προσθέτει δεδομένα εντός του csv αρχείου
#def readData: διαβάζει το αρχειο και επιστρέφει τα δεδομένα ανα στήλη σε πίνακες
#def writeResults
#def previewFile: ανοίγει το αρχείο με τα windows
