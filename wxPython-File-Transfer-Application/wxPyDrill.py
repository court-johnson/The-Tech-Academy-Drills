import wx
import shutil
from datetime import timedelta, datetime
from os import path
import os

#File locations
folders = {'Folder A':{'path':'C:\Users\court\Desktop\Folder A'},
           'Folder B':{'path':'C:\Users\court\Desktop\Folder B'}}

#Setting the time now to the deadline time of 24 hours
now = datetime.now()
deadline = now + timedelta(hours=-24)

#-----------------------------------------------------------------------

#creating GUI
class fileWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,200))
        #creating panel with text and buttons
        panel = wx.Panel(self)
        originText = wx.StaticText(panel, -1, "Origin Location",(55,30))
        destinationText = wx.StaticText(panel, -1, "Destination Location",(235,30))

        self.origin = wx.ComboBox(panel, choices=folders.keys(),
                             style=wx.CB_DROPDOWN, pos=(60,50))
        self.destination = wx.ComboBox(panel, choices=folders.keys(),
                             style=wx.CB_DROPDOWN, pos=(250,50))
        transferButton = wx.Button(panel, wx.ID_ANY, label='Transfer',
                                   pos=(150,100))
        
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
        popupComplete.Destroy()
        self.Destroy()
        
#---------------------------------------------------------------------------
      
if __name__ == '__main__':
    app = wx.App(False)
    frame = fileWindow(None, 'Transfer Files')
    
    app.MainLoop()
    




        
