import wx

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(450,250))
        self.Center()
        panel=wx.Panel(self)
        button = wx.Button(panel, label="Exit", size=(100,40), pos=(175,125))
        button.Bind(wx.EVT_BUTTON, self.exit)
        
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        self.SetMenuBar(menuBar)
        menuBar.Append(fileMenu, "File")
        menuBar.Append(editMenu, "Edit")
        fileMenu.Append(wx.NewId(), "New File", "Create a new file")
        fileMenu.Append(wx.NewId(), "Open", "Open an existing file")
        fileMenu.Append(wx.NewId(), "Exit", "Exit window")

        self.CreateStatusBar()

    def exit(self, event):
        self.Destroy()
        

app = wx.App()
frame = Frame("Python Gui")
frame.Show()
app.MainLoop()
