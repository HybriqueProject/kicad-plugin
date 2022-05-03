import re
import datetime
import sys
import io
import json
import requests
import pcbnew
import json
import os
import xml.etree.ElementTree as ET

# from urllib import urlencode
# import urllib2

# def http_post(url, data):
#     post = urlencode(data)
#     req = urllib2.Request(url, post)
#     response = urllib2.urlopen(req)
#     return response.read()


class Hybrique(pcbnew.ActionPlugin):
    def __init__(self):
        super(Hybrique, self).__init__()
        self.name = "Hybrique"
        self.category = "Read PCB"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(
            os.path.dirname(__file__), "logo.png")
        self.description = "Search for parts online"

    def defaults(self):
        self.name = "Hybrique"
        self.category = "Read PCB"
        self.description = "Search for parts online"

    # Function for issues in tab2

    def Run(self):

        board = pcbnew.GetBoard()
        pcb_file_name = board.GetFileName()
        modules = board.GetModules()

        fileName = ""
        for i in range(len(pcb_file_name)-1, -1, -1):
            if(pcb_file_name[i] == '/'):
                break
            else:
                fileName = pcb_file_name[i] + fileName

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

        # Create Hybrique dir if do not exist
        hybriqueDirPath = os.path.join(
            os.path.expanduser('~\AppData\Local'), 'Hybrique')
        if not os.path.isdir(hybriqueDirPath):
            os.makedirs(hybriqueDirPath)

        with open(os.path.join(os.path.expanduser('~\AppData\Local'), 'Hybrique', '_temp.json'), 'w') as f:
            json.dump(dataSend, f)

        path = os.path.join(os.path.expanduser(
            '~\AppData\Local\Hybrique'), 'plugins.xml')
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            app_tag = root.find("meta").find("app")
            exePath = app_tag.attrib["path"]

            # Launching the application
            os.system('"'+str(exePath)+'"' + " -p")
        except:
            # Create plugin.xml file inside hybrique dir
            PLUGINS_XML_PATH = os.path.join(hybriqueDirPath, 'plugins.xml')
            if not os.path.isfile(PLUGINS_XML_PATH):
                with open(PLUGINS_XML_PATH, 'w') as f:
                    f.write(
                        '<?xml version="1.0"?><root><plugins><kicad/></plugins></root>')

            # Show popup to download plugin
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
