import smtplib, ssl
from socket import gaierror
import os
import csv

global dataBuffer
dataBuffer=''
def SentEmailNotification(data,receiver_email):
    SaveData(data)
    return
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    # sender_email = "gigiriva2oz@gmail.com"
    # password = 'ddimitrakopoulos314159'
    sender_email,password = ReadEmailSenderCredentials()

    message = f"""\
    Subject: Found something new

    From: {sender_email}

    {data}
    This message is sent from Gigiriva Automation System.
    """

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print(f'Email was sent to {receiver_email}')
    except (gaierror, ConnectionRefusedError):
        print('Failed to connect to the server. Bad connection settings?')
    except smtplib.SMTPServerDisconnected:
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))

def SaveData(data):
    global dataBuffer
    with open('DataLogs/SentedEmailData.txt','a') as f:
        for line in data:
        #print(line)
            f.write(str(line[0])+','+str(line[1])+','+str(line[2])+','+str(line[3])+','+str(line[4])+','+str(line[5])+'\n')
        f.write('#################################################################################\n')

    with open('DataLogs/SentedEmailData.txt','r') as f:
        dataBuffer=f.read()


def WriteEmailSenderCredentials(senderEmail,password):
    fileName="dataLogs/EmailSenderCredentials.csv"
    if os.path.isfile(fileName):
        with open(fileName, 'w') as csv_file:  # create and write a new file
            fieldnames = ['SenderEmail', 'Password']
            dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
            dict_writer.writeheader()
            csv_writer = csv.writer(csv_file, lineterminator='\n')
            data=[senderEmail,password]
            csv_writer.writerow(data)


def ReadEmailSenderCredentials():
    fileName = "dataLogs/EmailSenderCredentials.csv"
    if os.path.isfile(fileName):
        with open(fileName, 'r') as csv_file:  # append to existed file
            csv_reader = csv.reader(csv_file, lineterminator='\n')
            for row in csv_reader:
                try:
                    senderEmail = row[0]
                    password = row[1]
                except Exception as e :
                    print(e)
                    return None,None
            return senderEmail, password