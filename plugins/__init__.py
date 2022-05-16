import pcbnew
import os
import sys
import platform
import json
import xml.etree.ElementTree as ET
import subprocess

class Hybrique(pcbnew.ActionPlugin):
    def __init__(self):
        super(Hybrique, self).__init__()
        self.name = "Hybrique"
        self.category = "Read PCB"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(
            os.path.dirname(__file__), "icon.png")
        self.description = "Search for parts online"

    def defaults(self):
        self.name = "Hybrique"
        self.category = "Read PCB"
        self.description = "Search for parts online"

    def Run(self):

        board = pcbnew.GetBoard()
        pcb_file_name = board.GetFileName()
        try:
            modules = board.GetFootprints()
        except:
            modules = board.GetModules()

        SYSTEM_PLATFORM = platform.system()

        fileName = pcb_file_name.split('/')[-1]

        if SYSTEM_PLATFORM == 'Windows':
            fileName = fileName.split('\\')[-1]
        
        idx = 0
        index = 0
        dictInfo = []

        '''
        modules = [
            {
                "GetReference":"r1",
                "GetDescription":"abc",
                "GetValue":"1"
            },
            {
                "GetReference":"r2",
                "GetDescription":"abc",
                "GetValue":"1"
            },
            {
                "GetReference":"r3",
                "GetDescription":"abcd",
                "GetValue":"2"
            }
        ]
        '''

        for module in modules:
            index += 1
            x = module.GetReference()
            #x = module["GetReference"]
            y = module.GetDescription()
            #y = module["GetDescription"]
            z = module.GetValue()
            #z = module["GetValue"]
            groupId = -1
            for i in dictInfo:
                if(i["PackageDescription"] == y and i["Value"] == z):
                    groupId = i["GroupID"]
                    break
            if(groupId == -1):
                idx += 1
                groupId = idx

            data = {
                "Name": x,
                "Index": str(index),
                "Value": z,
                "PackageDescription": y,
                "PackageName": "",
                "PackageHeadline": "",
                "DeviceDesctiption": "",
                "GroupID": str(groupId)
            }
            dictInfo.append(data)

        dataSend = {
            "filename": fileName,
            "source": "Kicad",

        }
        dataOrder = [
                    [
                        "Name",
                        "Index",
                        "Value",
                        "PackageDescription",
                        "PackageName",
                        "PackageHeadline",
                        "DeviceDesctiption",
                        "GroupID"
                    ]
        ]

        for i in dictInfo:
            data = []
            data.append(i["Name"])
            data.append(i["Index"])
            data.append(i["Value"])
            data.append(i["PackageDescription"])
            data.append(i["PackageName"])
            data.append(i["PackageHeadline"])
            data.append(i["DeviceDesctiption"])
            data.append(i["GroupID"])
            dataOrder.append(data)

        dataSend["data"] = dataOrder

        if SYSTEM_PLATFORM == 'Windows':
            HYBRIQUE_DIR_PATH = os.path.join(os.path.expanduser('~\AppData\Local'), 'Hybrique')
        elif SYSTEM_PLATFORM == "Linux":
            HYBRIQUE_DIR_PATH = os.path.expanduser('~/.hybrique')
        elif SYSTEM_PLATFORM == "Darwin":
            HYBRIQUE_DIR_PATH = os.path.expanduser('~/.hybrique')

        # Create Hybrique dir if do not exist
        
        if not os.path.isdir(HYBRIQUE_DIR_PATH):
            os.makedirs(HYBRIQUE_DIR_PATH)

        with open(os.path.join(HYBRIQUE_DIR_PATH, '_temp.json'), 'w') as f:
            json.dump(dataSend, f)

        PLUGINS_XML_PATH = os.path.join(HYBRIQUE_DIR_PATH, 'plugins.xml')
        try:
            tree = ET.parse(PLUGINS_XML_PATH)
            root = tree.getroot()
            app_tag = root.find("meta").find("app")
            exePath = app_tag.attrib["path"]
            
            # Launching the application
            if SYSTEM_PLATFORM == 'Windows':
                runCmd = '"'+str(exePath)+'"' + " -p"
                CREATE_NO_WINDOW = 0x08000000
                subprocess.call(runCmd, creationflags=CREATE_NO_WINDOW)
            elif SYSTEM_PLATFORM == "Linux":
                runCmd = "hybrique -p"
                os.system(runCmd)
            elif SYSTEM_PLATFORM == "Darwin":
                runCmd = "hybrique -p"        
                os.system(runCmd)

        except:
            # Create plugin.xml file inside hybrique dir
            if not os.path.isfile(PLUGINS_XML_PATH):
                with open(PLUGINS_XML_PATH, 'w') as f:
                    f.write('<?xml version="1.0"?><root><plugins><kicad/></plugins></root>')

            # Show popup to download plugin
            HYBRIQUE_PRODUCT_PAGE = "https://www.hybrique.com/product"
            
            import webbrowser
            if SYSTEM_PLATFORM == 'Windows':
                import ctypes
                STYLE_YESNO = 0x04
                ICON_EXLAIM=0x30
                result = ctypes.windll.user32.MessageBoxW(0, "Please download and install the standalone plugin!\nDo you want to proceed to the webpage ?", "App not found!", STYLE_YESNO | ICON_EXLAIM)
                if (result == 6):
                    webbrowser.open_new_tab(HYBRIQUE_PRODUCT_PAGE)
                elif (result == 7):
                    pass
            elif SYSTEM_PLATFORM == "Darwin":
                import wx
                wixApp = wx.App()
                dlg = wx.MessageDialog(parent=None, message='Please download and install the standalone plugin!\nDo you want to proceed to the webpage ?', caption='App not found!', style=wx.YES | wx.NO | wx.CENTRE | wx.ICON_EXCLAMATION)
                result = dlg.ShowModal()
                if (result == wx.ID_YES):
                    webbrowser.open_new_tab(HYBRIQUE_PRODUCT_PAGE)
                elif (result == wx.ID_NO):
                    pass
                dlg.Destroy()
                wixApp.Destroy()
            elif SYSTEM_PLATFORM == "Linux":
                if sys.version_info[0] == 3:
                    from tkinter import Tk, messagebox
                    root = Tk()
                    result = messagebox.askyesno(title='App not found!', message='Please download and install the standalone plugin!\nDo you want to proceed to the webpage ?')
                    if (result == True):
                        webbrowser.open_new_tab(HYBRIQUE_PRODUCT_PAGE)
                    else:
                        pass
                    root.mainloop()
                elif sys.version_info[0] == 2:
                    import Tkinter
                    import tkMessageBox
                    master = Tkinter.Tk()
                    master.withdraw()
                    res = tkMessageBox.askokcancel(
                        'App not found!', 'Please download and install the plugin!')
                    if res == True:
                        # Open web browser
                        import webbrowser
                        webbrowser.open_new_tab("https://www.hybrique.com/product")
            

Hybrique().register()
