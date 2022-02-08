from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from HomeDepotData import *
from GurobiAllocationEngine import AllocationModel
from GurobiOutput import *


class UI:

    ##Function to initialize and set all variables used within the UI
    def __init__(self, master):
        
        self.root = master
        
        self.POfn = StringVar()
        self.CSfn = StringVar()
        self.CRfn = StringVar()
        self.RGfn = StringVar()
        self.MQCfn = StringVar()
        self.OAfn = StringVar()
        self.TPSens = StringVar()
        self.CarrierRemoved = StringVar()
        self.OriginRemoved = StringVar()
        self.DestRemoved = StringVar()
        self.Carrier2Cap = StringVar()
        self.Origin2Cap = StringVar()
        self.Dest2Cap = StringVar()
        self.CarrierCap = StringVar()
        self.contractWK = StringVar()
        self.costOnOff = StringVar()
        self.var = IntVar()
        
        
        self.POfn.set('...')
        self.CSfn.set('...')
        self.CRfn.set('...')
        self.RGfn.set('...')
        self.MQCfn.set('...')
        self.OAfn.set('...')
        self.TPSens.set('high')
        self.CarrierRemoved.set('Carrier')
        self.OriginRemoved.set('Origin')
        self.DestRemoved.set('Destination')
        self.Carrier2Cap.set('Carrier')
        self.CarrierCap.set('Upper Bound')
        self.Origin2Cap.set('Origin')
        self.Dest2Cap.set('Destination')
        self.contractWK.set("Week Number")
        self.costOnOff.set('On')

        self.originsList = ['Please choose a carrier first']
        self.destinationList = ['Please choose a carrier first']
        self.originsCapList = ['Please choose a carrier first']
        self.destinationCapList = ['Please choose a carrier first']
        self.LanesRemoved = set()
        self.alreadyAssigned = dict()

        
        self.InputFiles()

############################################################################################################################################################
##Functions create each window that is shown in the UI

    def InputFiles(self):

        self.Close()
        
        self.aWin = Toplevel()
        self.aWin.rowconfigure(0, weight=1)
        self.aWin.columnconfigure(0, weight=1)
        self.aWin.title("Input Files")

        self.fr=Frame(self.aWin)
        self.fr.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.PO = Label(self.fr, text="Purchase Orders: ", anchor="w")
        self.PO.grid(row=0, column=0)

        self.CS = Label(self.fr, text="Carrier Schedule: ", anchor="w")
        self.CS.grid(row=1, column=0)

        self.CR = Label(self.fr, text="Carrier Rates: ", anchor="w")
        self.CR.grid(row=2, column=0, sticky=W)

        self.RG = Label(self.fr, text="Routing Guide: ", anchor="w")
        self.RG.grid(row=3, column=0, sticky=W)

        self.MQC = Label(self.fr, text="MQC Report: ", anchor="w")
        self.MQC.grid(row=4, column=0, sticky=W)

        self.PObutt = Button(self.fr, text="Choose File...", command=self.openPO)
        self.PObutt.grid(row=0, column=1, padx=10)

        self.CSbutt = Button(self.fr, text="Choose File...", command=self.openSchedule)
        self.CSbutt.grid(row=1, column=1, padx=10)

        self.CRbutt = Button(self.fr, text="Choose File...", command=self.openRates)
        self.CRbutt.grid(row=2, column=1, padx=10)

        self.RGbutt = Button(self.fr, text="Choose File...", command=self.openRouting)
        self.RGbutt.grid(row=3, column=1, padx=10)

        self.MQCbutt = Button(self.fr, text="Choose File...", command=self.openMQCReport)
        self.MQCbutt.grid(row=4, column=1, padx=10)
        
        self.e1 = Entry(self.fr, state = 'readonly', textvar = self.POfn, width = 50)
        self.e1.grid(row = 0, column = 2, sticky=E)
        
        self.e2 = Entry(self.fr, state = 'readonly', textvar = self.CSfn, width = 50)
        self.e2.grid(row = 1, column = 2, sticky=E)

        self.e3 = Entry(self.fr, state = 'readonly', textvar = self.CRfn, width = 50)
        self.e3.grid(row = 2, column = 2, sticky=E)

        self.e4 = Entry(self.fr, state = 'readonly', textvar = self.RGfn, width = 50)
        self.e4.grid(row = 3, column = 2, sticky=E)
        
        self.MQCe = Entry(self.fr, state = 'readonly', textvar = self.MQCfn, width = 50)
        self.MQCe.grid(row = 4, column = 2, sticky=E)

        self.cf3 = Button(self.fr, width = 30)
        self.cf3["text"] = "Next"
        self.cf3["command"] = self.checkFilesMissing
        self.cf3.grid(row=6, column=0, sticky=EW, pady = 5, columnspan=3)

        ##This segment centers the window
        self.aWin.update_idletasks()
        width = self.aWin.winfo_width()
        height = self.aWin.winfo_height()
        x = (self.aWin.winfo_screenwidth()//2) - (width//2)
        y = (self.aWin.winfo_screenheight()//2) - (height//2)
        self.aWin.geometry("{}x{}+{}+{}".format(width, height, x, y))


    def allocation_status(self):
        
        self.Close()
    
        self.bWin = Toplevel()
        self.bWin.rowconfigure(0, weight=1)
        self.bWin.columnconfigure(0, weight=1)
        self.bWin.title("Allocation Status")
        
        self.f2=Frame(self.bWin)
        self.f2.grid(row = 0, column = 0, columnspan =3, padx = 10, pady = 10)

        self.weekLabel = Label(self.f2, text="Which contract week number is this allocation for?")
        self.weekLabel.grid(row=0, column=0, sticky=W)

        self.contractNum = Entry(self.f2, textvar=self.contractWK, width=15)
        self.contractNum.grid(row=1, column=0, sticky=W)

        self.question = Label(self.f2, text="Is this an original allocation or reallocation?")
        self.question.grid(row=3,column=0, sticky=W, pady=10)
        
        self.orig = Radiobutton(self.f2, text="Original Allocation",  height=2, variable=self.var, value=0)
        self.orig.grid(row=4, column=0, sticky=W)
        
        self.reop = Radiobutton(self.f2, text="Re-Allocation", height=3, variable=self.var, value=1)
        self.reop.grid(row=5, column=0, sticky=W)

        self.miniframe = Frame(self.bWin)
        self.miniframe.grid(row=6, column=0, columnspan=3, pady = 5, padx = 5)
        
        self.backbutt = Button(self.miniframe, text='Back', width=15, command=self.InputFiles)
        self.backbutt.grid(row=0, column=0, sticky=W)

        self.nextbutt = Button(self.miniframe, text='Next', width=15, command=self.assignNext)
        self.nextbutt.grid(row=0, column=1, sticky=E)

        self.bWin.update_idletasks()
        width = self.bWin.winfo_width()
        height = self.bWin.winfo_height()
        x = (self.bWin.winfo_screenwidth()//2) - (width//2)
        y = (self.bWin.winfo_screenheight()//2) - (height//2)
        self.bWin.geometry("{}x{}+{}+{}".format(width, height, x, y))


    def uploadOriginal(self):
        
        self.Close()

        self.cWin = Toplevel()
        self.cWin.rowconfigure(0, weight=1)
        self.cWin.columnconfigure(0, weight=1)
        self.cWin.title("Upload Original Allocation: ")

        self.f3 = Frame(self.cWin)
        self.f3.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.label1 = Label(self.f3, text="Original Allocation")
        self.label1.grid(row=0, column=0, sticky=W)

        self.ch5 = Button(self.f3, text= "Choose File...", command=self.openOriginal)
        self.ch5.grid(row=0, column=1, padx=10)

        self.e5 = Entry(self.f3, state = 'readonly', textvar = self.OAfn, width = 50)
        self.e5.grid(row = 0, column = 2, sticky=E)

        self.miniframe1 = Frame(self.cWin)
        self.miniframe1.grid(row=1, column=0, columnspan=3, pady = 5, padx = 5)

        self.nextbutt1 = Button(self.miniframe1, text="Next", width=20, command=self.manipulateAlreadyAllocated)
        self.nextbutt1.grid(row=0, column=1, sticky=E)

        self.backbutt1 = Button(self.miniframe1, text="Back", width=20, command=self.allocation_status)
        self.backbutt1.grid(row=0, column=0, sticky=W)

        self.cWin.update_idletasks()
        width = self.cWin.winfo_width()
        height = self.cWin.winfo_height()
        x = (self.cWin.winfo_screenwidth()//2) - (width//2)
        y = (self.cWin.winfo_screenheight()//2) - (height//2)
        self.cWin.geometry("{}x{}+{}+{}".format(width, height, x, y))


    def lanePreferences(self):
        
        self.Close()
        
        self.dWin = Toplevel()
        self.dWin.rowconfigure(0, weight=1)
        self.dWin.columnconfigure(0, weight=1)
        self.dWin.title("Lane Preferences")

        self.f4 = Frame(self.dWin)
        self.f4.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.label3 = Label(self.f4, text="Remove Carrier Lane: ")
        self.label3.grid(row=0, column=0, sticky=W)

        self.label4 = Label(self.f4, text="Carrier Capacity Restrictions (FEU): ")
        self.label4.grid(row=2, column=0, sticky=W)

        self.removecarrier = OptionMenu(self.f4, self.CarrierRemoved, 'CSCL', 'CMDU', 'EGLV', 'HJSC', 'HLCU', 'MAEU', 'MOLU', 'NYKS', 'OOLU', command=self.setOD)
        self.removecarrier.grid(row=0, column=1, sticky=E+W)

        self.carriercap = OptionMenu(self.f4, self.Carrier2Cap, 'CSCL', 'CMDU', 'EGLV', 'HJSC', 'HLCU', 'MAEU', 'MOLU', 'NYKS', 'OOLU', command=self.setCapOD)
        self.carriercap.grid(row=2, column=1, sticky=E+W)

        self.removeorigin = OptionMenu(self.f4, self.OriginRemoved, *self.originsList)
        self.removeorigin.grid(row=0, column=2, sticky=E+W)

        self.removedestination = OptionMenu(self.f4, self.DestRemoved, *self.destinationList)
        self.removedestination.grid(row=0, column=3, sticky=E+W)

        self.removeButt = Button(self.f4, text='Remove Lane', command=self.removeLanes)
        self.removeButt.grid(row=1, column=1, sticky=E+W, pady=(5,15), padx=2)

        self.addButt = Button(self.f4, text='Add Back Lane', command=self.addBackLanes)
        self.addButt.grid(row=1, column=2, sticky=E+W, pady=(5,15), padx=2)

        self.CapOrigin = OptionMenu(self.f4, self.Origin2Cap, *self.originsCapList)
        self.CapOrigin.grid(row=2, column=2, sticky=E+W)

        self.CapDestination = OptionMenu(self.f4, self.Dest2Cap, *self.destinationCapList)
        self.CapDestination.grid(row=2, column=3, sticky=E+W)

        self.carrCapEntry = Entry(self.f4, text=self.CarrierCap)
        self.carrCapEntry.grid(row=3, column=1, sticky=W, padx=2)

        self.addCapButt = Button(self.f4, text='Add Capacity', command=self.addCarrierCap)
        self.addCapButt.grid(row=3, column=2, sticky=E+W, pady=(5,10), padx=2)

        self.addCapButt = Button(self.f4, text='Remove Capacity', command=self.removeCarrierCap)
        self.addCapButt.grid(row=3, column=3, sticky=E+W, pady=(5,10), padx=2)

        self.miniframe2 = Frame(self.dWin)
        self.miniframe2.grid(row=4, column=0, columnspan=3, pady = 5, padx = 5)

        self.nextbutt3 = Button(self.miniframe2, text="Next", width=20, command=self.allocationPreferences)
        self.nextbutt3.grid(row=0, column=1, sticky=E)

        self.backbutt2 = Button(self.miniframe2, text="Back", width=20, command=self.allocation_status)
        self.backbutt2.grid(row=0, column=0, sticky=W)

        self.dWin.update_idletasks()
        width = self.dWin.winfo_width()+75
        height = self.dWin.winfo_height()
        x = (self.dWin.winfo_screenwidth()//2) - (width//2)
        y = (self.dWin.winfo_screenheight()//2) - (height//2)
        self.dWin.geometry("{}x{}+{}+{}".format(width, height, x, y))


    def allocationPreferences(self):
        
        self.Close()
        
        self.eWin = Toplevel()
        self.eWin.rowconfigure(0, weight=1)
        self.eWin.columnconfigure(0, weight=1)
        self.eWin.title("Allocation Preferences")

        self.f5 = Frame(self.eWin)
        self.f5.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        self.label2 = Label(self.f5, text="Target Percentage Penalty: ")
        self.label2.grid(row=0, column=0, sticky=W, pady=(6,0))

        self.label3 = Label(self.f5, text="MQC Penalty: ")
        self.label3.grid(row=1, column=0, sticky=W)

        self.label4 = Label(self.f5, text="Cost Optimization On/Off: ")
        self.label4.grid(row=2, column=0, sticky=W)
                   
        self.tarpercentage = Scale(self.f5, from_=0, to=1000, orient=HORIZONTAL, resolution=50, length=200) ##Change resolution here to alter how specific of a penalty you can have
        self.tarpercentage.set(500)
        self.tarpercentage.grid(row=0, column=1, sticky=E+W, pady=(0,10))

        self.MQCPenalty = Scale(self.f5, from_=0, to=1000, orient=HORIZONTAL, resolution=50, length=200) ##Change resolution here to alter how specific of a penalty you can have
        self.MQCPenalty.set(500)
        self.MQCPenalty.grid(row=1, column=1, sticky=E+W, pady=(0,10))

        self.costOpt = OptionMenu(self.f5, self.costOnOff, '', 'On', 'Off')
        self.costOpt.grid(row=2, column=1, sticky=E+W)

        self.miniframe3 = Frame(self.eWin)
        self.miniframe3.grid(row=3, column=0, columnspan=3, pady = 5, padx = 5)

        self.runbutt = Button(self.miniframe3, text="Run Allocation", width=20, command=self.RunAllocation)
        self.runbutt.grid(row=0, column=1, sticky=E)

        self.backbutt3 = Button(self.miniframe3, text="Back", width=20, command=self.lanePreferences)
        self.backbutt3.grid(row=0, column=0, sticky=W)

        self.eWin.update_idletasks()
        width = self.eWin.winfo_width()+75
        height = self.eWin.winfo_height()
        x = (self.eWin.winfo_screenwidth()//2) - (width//2)
        y = (self.eWin.winfo_screenheight()//2) - (height//2)
        self.eWin.geometry("{}x{}+{}+{}".format(width, height, x, y))
        
############################################################################################################################################################
##Functions to call on the HomeDepotData and Model files to create the data structures and run the model
        
    def ManipulateData(self):
        self.data = HomeDepotData(self.POfn.get(), self.CSfn.get(), self.CRfn.get(), self.RGfn.get(), self.MQCfn.get(), int(self.contractWK.get()))
        self.lanePreferences()

    def manipulateAlreadyAllocated(self):
        if len(self.OAfn.get()) <= 3:
            return messagebox.showwarning("Warning","The original allocation file is missing")
        self.data = HomeDepotData(self.POfn.get(), self.CSfn.get(), self.CRfn.get(), self.RGfn.get(), self.MQCfn.get(), int(self.contractWK.get()))
        self.data.getOriginalAllocation(self.OAfn.get())
        self.lanePreferences()

    def RunAllocation(self):
        if self.costOnOff.get() == 'On':
            costOnOff=True
        elif self.costOnOff.get() == 'Off':
            costOnOff=False
        tarPercentagePen = self.tarpercentage.get()
        MQCPenalty = self.MQCPenalty.get()
        self.data.removeStrings(self.LanesRemoved)
        model = AllocationModel(self.data, costOn=costOnOff, allocationPen=tarPercentagePen, MQCPen=MQCPenalty)
        outputModelResults(model)
        print("\nThe allocation process is complete and the output file has been saved to your current folder.")
        self.Close()

############################################################################################################################################################
##Functions to create drop-down menus, a list of lanes to remove, and set capacity restrictions for carrier/lane pairs
        
    def setOD(self, value):
        C = self.data.carrierO
        D = self.data.carrierOD
        self.originsList = ['Origin']
        self.destinationList = ['Destination']
        for i in C[self.CarrierRemoved.get()]:
            self.originsList.append(i)
        for x in D[self.CarrierRemoved.get()]:
            self.destinationList.append(x)
            
        self.removeorigin = OptionMenu(self.f4, self.OriginRemoved, *self.originsList)
        self.removeorigin.grid(row=0, column=2, sticky=E+W)

        self.removedestination = OptionMenu(self.f4, self.DestRemoved, *self.destinationList)
        self.removedestination.grid(row=0, column=3, sticky=E+W)

    def setCapOD(self, value):
        O = self.data.carrierO
        Dest = self.data.carrierOD
        self.originsCapList = ['Origin']
        self.destinationCapList = ['Destination']
        for i in O[self.Carrier2Cap.get()]:
            self.originsCapList.append(i)
        for x in Dest[self.Carrier2Cap.get()]:
            self.destinationCapList.append(x)
            
        self.removeCapOrigin = OptionMenu(self.f4, self.Origin2Cap, *self.originsCapList)
        self.removeCapOrigin.grid(row=2, column=2, sticky=E+W)

        self.removeCapDestination = OptionMenu(self.f4, self.Dest2Cap, *self.destinationCapList)
        self.removeCapDestination.grid(row=2, column=3, sticky=E+W)


    def removeLanes(self):
        lane = (self.CarrierRemoved.get(), self.OriginRemoved.get(), self.DestRemoved.get())
        self.LanesRemoved.add(lane)
        print('These are the lanes you will remove: ', self.LanesRemoved)

    def addBackLanes(self):
        lane = (self.CarrierRemoved.get(), self.OriginRemoved.get(), self.DestRemoved.get())
        self.LanesRemoved.remove(lane)
        print('These are the lanes you will remove: ', self.LanesRemoved)


    def addCarrierCap(self):
        lane = (self.Origin2Cap.get(), self.Dest2Cap.get())
        carrier = self.Carrier2Cap.get()
        capacity = int(self.CarrierCap.get())
        self.data.addCapacity(carrier, lane, capacity)


    def removeCarrierCap(self):
        lane = (self.Origin2Cap.get(), self.Dest2Cap.get())
        carrier = self.Carrier2Cap.get()
        capacity = int(self.CarrierCap.get())
        self.data.removeCapacity(carrier, lane, capacity)

############################################################################################################################################################
##Functions to display error messages if a contract week is entered incorrectly or input file directories are missing
##Function also brings you to the correct screen dependent on it being original or a re-allocation

    def assignNext(self):
        try:
            num = int(self.contractWK.get())
            if num in range(1,53):
                if self.var.get() == 0:
                    self.ManipulateData()
                elif self.var.get() == 1:
                    self.uploadOriginal()
            else:
                return messagebox.showwarning("Warning","Please input an appropriate contract week number.")
        except:
            return messagebox.showwarning("Warning","Please input an appropriate contract week number.")
        
            
    def checkFilesMissing(self):
        if (len(self.POfn.get()) <= 3) or (len(self.CSfn.get())<=3) or (len(self.CRfn.get())<=3) or (len(self.RGfn.get())<=3) or (len(self.MQCfn.get())<=3):
            return messagebox.showwarning("Warning","Some files are missing")
        self.allocation_status()
        

############################################################################################################################################################
##Functions to open each file and set its respective variable to the proper file directory
        
    def openPO(self):
        self.poFile = filedialog.askopenfilename()
        self.POfn.set(self.poFile)
    
    def openSchedule(self):
        self.scheduleFile = filedialog.askopenfilename()
        self.CSfn.set(self.scheduleFile)
    
    def openRates(self):
        self.rateFile = filedialog.askopenfilename()
        self.CRfn.set(self.rateFile)

    def openRouting(self):
        self.routingFile = filedialog.askopenfilename()
        self.RGfn.set(self.routingFile)

    def openOriginal(self):
        self.OAFile = filedialog.askopenfilename()
        self.OAfn.set(self.OAFile)

    def openMQCReport(self):
        self.MQCFile = filedialog.askopenfilename()
        self.MQCfn.set(self.MQCFile)
        

############################################################################################################################################################
##Functions to close each window before a new window is opened
        
    def Close(self):
        try:
            self.aWin.withdraw()
        except:
            pass
        try:
            self.bWin.withdraw()
        except:
            pass
        try:
            self.cWin.withdraw()
        except:
            pass
        try:
            self.dWin.withdraw()
        except:
            pass
        try:
            self.eWin.withdraw()
        except:
            pass



##Root initialization of the TKinter GUI module
root=Tk()
root.withdraw()
root.title("THD Ocean Frieght Allocation")
app = UI(root)
root.mainloop()
