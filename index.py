import wx
import wx.html as html
import ctypes
from convert import *
import sys
import webbrowser
import re
import trim

class MDRenderWindow(wx.Frame):

    def __init__(self, defaultFile=None, *args, **kwargs):
        super(MDRenderWindow, self).__init__(*args, **kwargs)

        self.InitUI()
        if defaultFile:
            self.showMD(convert(open(defaultFile).read()))

    def InitUI(self):

        self.prepareMenu()
        self.prepareMainBody("")
        #
        self.SetIcon(wx.Icon('res/jojo.png', wx.BITMAP_TYPE_PNG))
        #
        myappid = 'krakenco.md.01' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # tbicon = wx.TaskBarIcon()
        # tbicon.setIcon(wx.Icon('res/jojo.png', wx.BITMAP_TYPE_PNG))


        toolbar = self.CreateToolBar()
        # self.toolbar.AddLabelTool(1, '', wx.Bitmap('res/texit.png'))
        zoomInTool = toolbar.AddTool(wx.ID_ANY, "Zoom In", wx.Bitmap("res/zoomin.png"))
        zoomOutTool = toolbar.AddTool(wx.ID_ANY, "Zoom In", wx.Bitmap("res/zoomout.png"))

        self.toolbar = toolbar
        self.toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.zoomIn, zoomInTool)
        self.Bind(wx.EVT_TOOL, self.zoomOut, zoomOutTool)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        self.SetSize((720, 480))
        self.SetMinSize((720, 480))
        self.SetTitle('Kraken MD')
        self.Centre()
        self.Show(True)

    def onNav(self, event):
        url = event.GetURL()
        webbrowser.open(url)

    def zoomOut(self, e):
        print ("Zooming out")

    def zoomIn(self, e):
        print ("Zooming in")


    def prepareMenu(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        viewMenu = wx.Menu()

        openItem = wx.MenuItem(fileMenu, wx.ID_OPEN, '&Open\tCtrl+O')
        fileMenu.Append(openItem)
        findItem = wx.MenuItem(fileMenu, wx.ID_ANY, '&Find\tCtrl+F')
        fileMenu.Append(findItem)

        fileMenu.AppendSeparator()
        imp = wx.Menu()
        imp.Append(wx.ID_ANY, 'Georgia')
        imp.Append(wx.ID_ANY, 'Segoe UI')
        imp.Append(wx.ID_ANY, 'Consolas')
        viewMenu.Append(wx.ID_ANY, 'Font', imp)
        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+C')
        fileMenu.Append(qmi)

        self.Bind(wx.EVT_MENU, self.open, openItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        self.Bind(wx.EVT_MENU, self.OnAboutBox, id=100)

        self.shst = viewMenu.Append(wx.ID_ANY, 'Show statubar',
            'Show Statusbar', kind=wx.ITEM_CHECK)
        self.shtl = viewMenu.Append(wx.ID_ANY, 'Show toolbar',
            'Show Toolbar', kind=wx.ITEM_CHECK)

        viewMenu.Check(self.shst.GetId(), True)
        viewMenu.Check(self.shtl.GetId(), True)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.shtl)
        self.Bind(wx.EVT_MENU, self.find, findItem)

        menubar.Append(fileMenu, '&File')
        menubar.Append(viewMenu, '&View')
        self.SetMenuBar(menubar)

    def OnAboutBox(self, e):
        description = "Render Markdown code with ease."

        licence = """Kraken MD is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version. Kraken MD is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with Kraken MD; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA """

        info = wx.adv.AboutDialogInfo()

        info.SetIcon(wx.Icon('res/jojo.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Kraken MD')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2016 - 2018 Kraken CO.')
        info.SetWebSite('http://krakenco.com')
        info.SetLicence(licence)
        info.AddDeveloper('Jacob Schneider')
        info.AddDocWriter('Jacob Schneider')
        info.AddArtist('Kraken CO.')
        info.AddTranslator('Jacob Schneider')

        wx.AboutBox(info)

    def ToggleStatusBar(self, e):

        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, e):

        if self.shtl.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()

    def open(self, e):
        with wx.FileDialog(self, "Open Markdown File", wildcard="Markdown File (*.md)|*.md",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.showMD(convert(file.read()))

            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)
                wx.MessageBox('An Error Occured', 'Error', wx.OK | wx.ICON_ERROR)

    def find(self, e):
        dlg = wx.TextEntryDialog(self, 'Enter text to be found','Find')
        if dlg.ShowModal() == wx.ID_OK:
            val = dlg.GetValue()
            # print (str(len(re.findall(val, self.pageContent))) + " matches")
            self.showMDFind(wrapMatches(self.code, val))

    def OnQuit(self, e):
        self.Close()

    def prepareMainBody(self, code):
        # print (code)

        self.panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.htmlwin = html.HtmlWindow(self.panel, -1, style=wx.NO_BORDER)
        self.htmlwin.SetBackgroundColour(wx.WHITE)
        self.htmlwin.SetStandardFonts()
        self.htmlwin.SetPage("<html>Open a file to begin.<!--<br><br<br><img src=\"res/jojo_white.png\" width=\"300\" height=\"300\">--></html>")

        vbox.Add((-1, 10), 0)
        vbox.Add(self.htmlwin, 1, wx.EXPAND)

        self.panel.SetSizer(vbox)

    def showMD(self, code):
        self.pageContent = trim.trimHTML(code)
        self.code = code
        self.htmlwin.SetPage(code)
    def showMDFind(self, code):
        self.htmlwin.SetPage(code)

def main(filePath=None):

    ex = wx.App()
    MDRenderWindow(filePath, None)
    ex.MainLoop()

if __name__ == '__main__':
    main(join(sys.argv[1:]))
