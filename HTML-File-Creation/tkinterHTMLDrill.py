from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import webbrowser
import sqlite3
import os.path
#------------------------------------------------------------------------------------------
#html script to be created 
script = """<html>
<body>
%s
</body>
</html>"""

#------------------------------------------------------------------------------------------

#connecting to the already created database and table
conn = sqlite3.connect('htmlDrill.db')
c = conn.cursor()

#Table already exists currently
#c.execute("DROP TABLE IF EXISTS entriesHTML")
#c.execute("CREATE TABLE entriesHTML(ID INTEGER PRIMARY KEY AUTOINCREMENT, ENTRY TEXT)")

#collecting data from when the last body text was created/saved 
c.execute("SELECT ENTRY FROM entriesHTML")#WHERE ID =(SELECT MAX(ID) FROM entriesHTML)")
previousEntries = c.fetchall()

#------------------------------------------------------------------------------------------

class Feedback():

    def __init__(self, master):
   
        master.title('Create HTML Document')
        master.resizable(False, False)

        #styling of the label, frame, button
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#85adad')
        self.style.configure('TButton', background = '#527a7a')
        self.style.configure('TLabel', background = '#85adad', font = ('Arial', 11))
        
        #creating the frame of the window
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        #label indicating to use the text box to enter in what should be entered into the html script
        ttk.Label(self.frame_content, text = "Please enter the text to be inserted:", style = 'TLabel').grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.enteredText = Text(self.frame_content, width = 30, height = 10, borderwidth = 3)
        self.enteredText.grid(row=1,column=0, padx = 10, sticky = 'w')
        
        #button that binds to the create html file function
        self.createFile = ttk.Button(self.frame_content, text='Create to Web Browser', style='TButton')
        self.createFile.grid(row = 3, column = 0, padx = 7, pady = 10, sticky = 'e')
        self.createFile.bind("<Button-1>", self.createButtonClicked)
        
        #button that allows the user to browser previous entries to reuse
        self.pickOldEntry = ttk.Button(self.frame_content, text='View Previous Entries', style = 'TButton')
        self.pickOldEntry.grid(row = 2, column = 0, padx = 7, pady = 10, sticky = 'e')
        self.pickOldEntry.bind("<Button-1>", self.pickOptionClicked)

#------------------------------------------------------------------------------------------
        
    def createButtonClicked(self, event):
        #indicating to create a file under a particular name
        file = open("test.html", 'w')
        
        #writing the file with the text entered in from the text box by the user
        file.write(script % self.enteredText.get('1.0', END))
        file.close()

        #opening the file to the default web browser automatically
        webbrowser.open(os.path.abspath("test.html"))
        self.dataInsert()
        file.close()
        
#------------------------------------------------------------------------------------------

    def pickOptionClicked(self, event):
        #creating new popup window to browser previously used body texts
        self.popupBox = Toplevel()
        self.popupBox.config(background = '#85adad')
 
        self.pickEntrySelection = ttk.Label(self.popupBox, text = "Select a previous saved entry:", style = 'TLabel')
        self.pickEntrySelection.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')   

        #box that produces previous used body text entries generated from the database
        self.oldEntries = Listbox(self.popupBox, width = 35, height = 10, borderwidth = 3)
        self.oldEntries.grid(row=1,column=0, padx = 10, sticky = 'w')

        #referencing each individual entry in the database and remove the brackets from the data
        for i in previousEntries:
            self.oldEntries.insert(END, i[0])

        #enters old entry selection into text box on initial window to be saved to the html file
        self.submit = ttk.Button(self.popupBox, text='Submit', style = 'TButton')
        self.submit.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.submit.bind('<Button-1>', self.oldEntryPicked)

        #closing the popup window
        self.cancel = ttk.Button(self.popupBox, text='Cancel', style = 'TButton')
        self.cancel.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'e')
        self.cancel.bind('<Button-1>', self.cancelClose)
        
#------------------------------------------------------------------------------------------
    #event from the submit button being clicked, inserts selected text to the original text box
    def oldEntryPicked(self, event):
        pickedEntry = self.oldEntries.selection_get()
        self.enteredText.insert(END, pickedEntry)
        self.popupBox.destroy()
        
    #closes pop up window   
    def cancelClose(self, event):
        self.popupBox.destroy()

#------------------------------------------------------------------------------------------

    #function for adding the entered text from the user into the database for later use or reference
    def dataInsert(self):        
        #inserting retrieved time and date of when the transfer button was clicked
        c.execute("INSERT INTO entriesHTML (ENTRY) VALUES (?)", (self.enteredText.get('1.0', END),))
        conn.commit()

        #disconnecting from database
        c.close()
        conn.close()
        
#------------------------------------------------------------------------------------------

def main():
    root = Tk()
    feedback = Feedback(root)
    root.mainloop()

if __name__ == '__main__':
    main()

