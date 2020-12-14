from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog
import Price_Tracker
import threading
import Parce_CSV as Csv
import ctypes
from tkinter import scrolledtext
from Activator import checkLicence
import tkinter.simpledialog
global processStatus
processStatus='Stopped'    #Values :Stopped or Running
import Sent_Email

def WriteToConsole(*message, end = "\n", sep = " "):
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    #Console.insert(INSERT, text)

def Clear_Entries():
    carName_entry.delete(0, END)
    model_entry.delete(0, END)
    link_entry.delete(0, END)
    frequency_entry.delete(0, END)
    price_entry.delete(0, END)
    emailReceiver_entry.delete(0, END)

def StartTracking():
    global processStatus
    global thread1
    if processStatus == 'Stopped':
        progress_bar.start()
        progress_bar.step(10)
        thread1=PriceTrackingThread()
        thread1.start()

        processStatus = "Running"
    else:
        messagebox.showinfo('Please Note', 'One Process has already started!!')

def StopTracking():
    global processStatus
    progress_bar.stop()
    screen.update()
    if processStatus == "Running":
         processStatus = 'Stopped'
         thread1.raise_exception()
         thread1.join()


#################################thread#####################################
class PriceTrackingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        Price_Tracker.Start_Tracking()
        Clear_Entries()

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

PriceTrackingThread.daemon=True #Otherwise you will have issues closing your program

##################################################################################

def add_info_to_text():
    carName = carName_entry.get()
    model = model_entry.get()
    link = link_entry.get()
    frequency = frequency_entry.get()
    maxPrice=price_entry.get()
    emailReceiver=emailReceiver_entry.get()

    if carName =='' or model =='' or link ==''  or frequency==0 :
        messagebox.showinfo('Please Note','One or more values are NULL')
        print('one or more values are NULL')
        return
    print(carName, model, link, frequency,maxPrice,emailReceiver)
    fileName = 'DataLogs/trackingList.csv'
    Csv.addData(fileName,carName,model,link,frequency,maxPrice,emailReceiver)
    Clear_Entries()

def remove_info_from_text():
    fileName = 'DataLogs/trackingList.csv'
    Csv.previewFile(fileName)

def open_result_file():
    if processStatus=='Stopped':
        Csv.previewFile('DataLogs\ResultLogs.csv')
    else:
        messagebox.showinfo('Please Note', 'One Process is running. You have to stop tracking and then open the result file.')



#####################################Tkinder Start#################################################
###################################################################################################
class MyDialog(simpledialog.Dialog):
    def body(self, master):

        Label(master, text="First:").grid(row=0)
        Label(master, text="Second:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        senderEmail = self.e1.get()
        password = self.e2.get()
        print(senderEmail,password)
        Sent_Email.WriteEmailSenderCredentials(senderEmail,password)


screen = Tk()
screen.geometry("1180x660")
screen.title("Car Price Tracking System")
heading = Label(text="Add the required information below", bg="cyan4", fg="black", width="500", height="3",font=14)
heading.pack()

frame_top = Frame(screen, width=500, height=380, bg="gray40")
frame_top.place(x=0, y=60)
frame_bottom= Frame(screen, width=500, height=280, bg="gray28")
frame_bottom.place(x=0, y=430)
carName_text = Label(text="Car name * ",font=12,bg='gray72' )
model_text = Label(text="Model* ",font=12 ,bg='gray72' )
link_text = Label(text="LINK to track* ", font=12 ,bg='gray72')
frequency_text = Label(text="Frequency of tracking in (sec) * ",font=12 ,bg='gray72' )
price_text = Label(text="Maximum price to track * ", font=12 ,bg='gray72')
emailReceiver_text = Label(text="Email Receiver * ", font=12 ,bg='gray72')

#Text above Entries
carName_text.place(x=15, y=70)
model_text.place(x=15, y=130)
link_text.place(x=15, y=190)
frequency_text.place(x=15, y=250)
price_text.place(x=15, y=310)
emailReceiver_text.place(x=15, y=370)

carName = StringVar()
model = StringVar()
link = StringVar()
frequency = IntVar()
price = IntVar()
emailReceiver = StringVar()


#Entries
carName_entry = Entry(textvariable=carName, width="30" ,bg='floral white')
model_entry = Entry(textvariable=model, width="30",bg='floral white')
link_entry = Entry(textvariable=link, width="75",bg='floral white')
frequency_entry = Entry(textvariable=frequency, width="15",bg='floral white')
price_entry = Entry(textvariable=price, width="15",bg='floral white')
emailReceiver_entry = Entry(textvariable=emailReceiver, width="35",bg='floral white')

#Console
'''Console = Text(screen, width=70,height=33)
Console.place(x=480,y = 60)'''
#Console.insert(END,f"{str(Price_Tracker.WriteToConsole())}")

carName_entry.place(x=15, y=100)
model_entry.place(x=15, y=160)
link_entry.place(x=15, y=220)
frequency_entry.place(x=15, y=280)
price_entry.place(x=15, y=340)
emailReceiver_entry.place(x=15, y=400)

#Buttons
AddBtn = Button(screen, text="Add data to Tracking File", width="30", height="2", command=add_info_to_text, bg="green")
AddBtn.place(x=15, y=440)
RemoveBtn = Button(screen, text="Edit Tracking File", width="30", height="2", command=remove_info_from_text, bg="DarkOrange3")
RemoveBtn.place(x=250, y=440)
StartBtn = Button(screen, text="Start Tracking", width="30", height="2", command=StartTracking, bg="cyan")
StartBtn.place(x=15, y=500)
StopBtn = Button(screen, text="Stop Tracking", width="30", height="2", command=StopTracking, bg="indian red")
StopBtn.place(x=250, y=500)
ShowResultsBtn = Button(screen, text="Show Car Results", width="30", height="2", command=lambda: open_result_file()  , bg="DarkOrange3")
ShowResultsBtn.place(x=120, y=560)
#rewrite the print function
#you just have to call write() instead of print()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        screen.destroy()

#screen.after(1000, RunTracking)
screen.protocol("WM_DELETE_WINDOW", on_closing)

####################################################
#screen.title("Email Data")

# Title Label
ttk.Label(screen,text="Search Results",font=("Times New Roman", 15),background='green',
          foreground="white").place(x=500, y=80)

# Creating scrolled text
# area widget
global text_area
text_area = scrolledtext.ScrolledText(screen,wrap=WORD,width=92,height=34,font=("Arial",10))
results=""
text_area.place(x=500, y=100)
text_area.insert('insert',results)


DataBuffer=''
localBuffer=''
firstRun=True
def PrintDataToGuiConsole():
    # global firstRun
    # global localBuffer
    # if firstRun: #1st time reads file
    #     file = open('DataLogs/SentedEmailData.txt', 'r')
    #     data = file.read()
    #     text_area.insert('insert',data+'\n')
    #     file.close()
    #     firstRun=False
    #     localBuffer=data
    #
    # else:   #next times reads buffer
    #     data= Sent_Email.dataBuffer
    #     if localBuffer != data: #data  changed
    #         #data.replace(localBuffer,'')
    #         text_area.delete('1.0',END)
    #         text_area.insert('insert', data+'\n')
    #         localBuffer = data
    file = open('DataLogs/SentedEmailData.txt', 'r')
    global DataBuffer
    data=file.read()

    if DataBuffer==data:
        pass
    elif DataBuffer=='':
        DataBuffer=data
        text_area.delete('1.0',END)
        text_area.insert('insert',data+'\n')
    else:
        data.replace(DataBuffer,'')
        text_area.delete('1.0',END)
        text_area.insert('insert', data+'\n')
        DataBuffer = data

    file.close()
    screen.after(10000, PrintDataToGuiConsole)

PrintDataToGuiConsole()
######################################################

def Activate():
    ActivationLabel = Label(screen, text="Pending...")
    ActivationLabel.place(x=80, y=620)
    file = open("DataLogs/ActivationKey.txt", "r+")  # r+ for read and write
    message,flag=checkLicence(file.read())
    if flag==False: #licence is valid
        ActivationLabel['text']=message
        print(file.read())
        file.close()
    else:
        USER_INP = simpledialog.askstring(title="Activation",prompt="Please enter the activation key:")

        file = open("DataLogs/ActivationKey.txt", "r+")
        file.truncate(0)
        try:
            file.write(USER_INP)
        except:
           pass
        message, flag = checkLicence(file.read())
        if flag==True: #licence is not valid
            ActivationLabel['text'] = message
            screen.after(4000, screen.destroy)
        file.close()

Activate()

def CheckEmailCredentials():
    email,password=Sent_Email.ReadEmailSenderCredentials()
    if email==None or password==None:
        messagebox.showinfo('Please Note', 'Your Email and Password Entries are empty, messages will not be sent')
        EmailCredentialsPopUp()
def EmailCredentialsPopUp():
   d = MyDialog(screen)

CheckEmailCredentials()
#################Menu Bar##########################
menubar = Menu(screen)
screen.config(menu=menubar)

# fileMenu = Menu(menubar)
# fileMenu.add_cascade(label="Exit", command=quit)
menubar.add_cascade(label="Activation", command=Activate)
menubar.add_cascade(label="Email-Credentials", command=EmailCredentialsPopUp)
####################################################

#progress Bar
progress_bar = ttk.Progressbar(screen, orient="horizontal",mode="determinate", maximum=100, value=0)
label_1 = Label(screen, text="Process Status")
label_1.place(x=15, y=560)
progress_bar.place(x=15, y=580)
progress_bar['value'] = 0


screen.update()
screen.configure(background='gray72')
screen.mainloop()

