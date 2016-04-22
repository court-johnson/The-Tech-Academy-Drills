import wx
import shutil
import time
import sqlite3
from datetime import timedelta, datetime
from os import path
import os

#File locations
folders = {'Folder A':{'path':'C:\Users\court\Desktop\Folder A'},
           'Folder B':{'path':'C:\Users\court\Desktop\Folder B'}}

#Setting the time now to the deadline time of 24 hours
now = datetime.now()
deadline = now + timedelta(hours=-24)

#connecting to the already created database and table
conn = sqlite3.connect('dbDrill.db')
c = conn.cursor()

#Table already exists currently
#c.execute("DROP TABLE IF EXISTS fileCheck")
#c.execute("CREATE TABLE fileCheck(ID INTEGER PRIMARY KEY AUTOINCREMENT, DATE TEXT, TIME TEXT)")

#collecting data from when the last transfer was completed
c.execute("SELECT DATE, TIME FROM fileCheck WHERE ID =(SELECT MAX(ID) FROM fileCheck)")
lastTransferPerformed = c.fetchone()
lastTransferStamp = [str(i) for i in (lastTransferPerformed)]
print lastTransferStamp

#-----------------------------------------------------------------------

#creating GUI
class fileWindow(wx.Frame):
    

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,250))
        #creating panel with text and buttons
        panel = wx.Panel(self)


        #origin text and dropdown
        originText = wx.StaticText(panel, -1, "Origin Location:",(60,20))
        self.origin = wx.ComboBox(panel, choices=folders.keys(),
                             style=wx.CB_DROPDOWN, pos=(60,40))
        
        #destination text and dropdown
        destinationText = wx.StaticText(panel, -1, "Destination Location:",(240,20))
        self.destination = wx.ComboBox(panel, choices=folders.keys(),
                             style=wx.CB_DROPDOWN, pos=(240,40))
        

        #print the last transfer date and time
        self.lastEntryText = wx.StaticText(panel, -1, "Last Transfer Performed:",(90,75))
        self.lastEntryBox = wx.TextCtrl(panel, value = str(lastTransferStamp), pos=(90,95), size=(200,-1))


        #transfer button
        transferButton = wx.Button(panel, wx.ID_ANY, label='Transfer', pos=(150,150))
        
        #initial pop up box
        popupQuestion = wx.MessageDialog(None, 'Would you like to check for a file \
modification within the last 24 hours?', 'Transfer', wx.YES_NO)
        popupAnswer = popupQuestion.ShowModal()
        popupQuestion.Destroy()
        
        if popupAnswer == wx.ID_NO:
            self.Close()

        #referencing event for transfer
        self.Bind(wx.EVT_BUTTON, self.fileTransfer, transferButton)
        
        #showing panel/frame
        self.Center()
        self.Show(True)

        
#---------------------------------------------------------------------------

    #transfering the selected modified files 
    def fileTransfer(self, event):
        originSelection = self.origin.GetStringSelection()
        destinationSelection = self.destination.GetStringSelection()
        origin_path = folders[originSelection]['path']
        dest_path = folders[destinationSelection]['path']

        #generating the file names from Origin 
        try:
            for root, dir, files in os.walk(origin_path):
                #looping through each file to retrieve the time stamp and pathname
                for file in files:
                    pathname = os.path.join(root, file)
                    modified_time = datetime.fromtimestamp(os.path.getmtime(pathname))
                    #comparing modification time from deadline and moving if appropriate
                    if now >= modified_time >= deadline:
                         print 'modified within 24 hours: ' + pathname
                         shutil.move(pathname, dest_path)
        except Exception as e:
            print e
        #printing 'completed' once all files are transferred
        else:
            self.transferButtonClicked()
            

#---------------------------------------------------------------------------

        #event defined for transfer
    def transferButtonClicked(self):
        popupComplete = wx.MessageDialog(None, 'Transfer Completed!', 'Transfer', wx.OK)
        popupDone = popupComplete.ShowModal()
        self.button_clicked_time = time.time()
        self.dataInsert()
        popupComplete.Destroy()
        self.Destroy()

#--------------------------------------------------------------------------
        
    def dataInsert(self):        
        #setting parameters to retrieve the date and the time of when the transfer button is clicked
        p = datetime.now()
        clicked_date = p.strftime("%Y-%m-%d")
        clicked_time = p.strftime("%H:%M")

        #inserting retrieved time and date of when the transfer button was clicked
        c.execute("INSERT INTO fileCheck (DATE, TIME) VALUES (?,?)", (clicked_date, clicked_time))
        conn.commit()

        #disconnecting from database        
        c.close()
        conn.close()

        
#---------------------------------------------------------------------------
      
if __name__ == '__main__':
    app = wx.App(False)
    frame = fileWindow(None, 'Transfer Files')
    
    app.MainLoop()

   
