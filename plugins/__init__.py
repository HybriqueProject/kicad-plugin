import pcbnew
import os
import re
import datetime

from Tkinter import *
from ttk import *


class Hybrique( pcbnew.ActionPlugin ):
    def __init__(self):
        super(Hybrique, self).__init__()
        self.name = "Hybrique"
        self.category = "Read PCB"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "logo.png")
        self.description = "Search for parts online"

    def defaults( self ):
        self.name = "Hybrique"
        self.category = "Read PCB"
        self.description = "Search for parts online"




    def tab_issues(self,tab_issues):
        label = Label(tab_issues, text="Issues generally occur because of missing primary filters!")
        label.place(x=0,y=0)

        btn_ignore=Button(tab_issues,text="Ignore")
        btn_resolve=Button(tab_issues,text="Resolve")
        btn_ignore.place(x=330, y=0)
        btn_resolve.place(x=415, y=0)

    def part_details_fun(self,part_Details):
        label = Label(part_Details, text="Hey")
        label.place(x=0,y=0)

    
    def manafactures_fun(self, manafacturers_):
        label = Label(manafacturers_, text="Ranking")
        label.place(x=0,y=0)

    def distributors_fun(self,distributors_):
        label = Label(distributors_, text="Ranking")
        label.place(x=0,y=0)


    def tab2(self, tab2):
 
        #labelFrame2 = Frame(tab2, text = "Second Tab")
        #labelFrame2.grid(column = 0, row = 0, padx = 8, pady = 4)
        """label = Label(labelFrame2, text="Enter Your Name:")
        label.grid(column=0, row=0, sticky='W')
        textEdit = Entry(labelFrame2, width=20)
        textEdit.grid(column=1, row=0)
        label2 = Label(labelFrame2, text="Enter Your Password:")
        label2.grid(column=0, row=1)
        textEdit = Entry(labelFrame2, width=20)
        textEdit.grid(column=1, row=1)"""


        label_count = Label(tab2, text="BOM has 7 unique parts out of 8 total parts in design")
        label_count.place(x=30,y=4)

        btn_filters=Button(tab2,text="Filters")
        btn_help=Button(tab2,text="Help")

        btn_filters.place(x=600,y=5)
        btn_help.place(x=690,y=5)

        
        combo=Combobox(tab2,height=10)
        combo["values"]=(1,2,3,4,5,"Hi")
        combo.current(2)
        combo.place(x=30, y=30)

        spin=Spinbox(tab2,from_=0, to=100, width=10)
        spin.place(x=440, y=30)

        bt_load=Button(tab2,text="LOAD BOM", width=10)
        bt_load.place(x=520, y=30)

        tree = Treeview(tab2, selectmode='browse')
        tree.place(x=30, y=65)

        vsb = Scrollbar(tab2, orient="vertical", command=tree.yview)
        vsb.place(x=30+550+2, y=65, height=200+20)
        #vsb.grid(row=30+200+2, column=95, height=200+20)

        tree.configure(yscrollcommand=vsb.set)

        tree["columns"] = ("1", "2","3","4","5","6","7","8")
        tree['show'] = 'headings'
        tree.column("1", width=50, anchor='c')
        tree.column("2", width=70, anchor='c')
        tree.column("3", width=70, anchor='c')
        tree.column("4", width=100, anchor='c')
        tree.column("5", width=50, anchor='c')
        tree.column("6", width=70, anchor='c')
        tree.column("7", width=70, anchor='c')
        tree.column("8", width=70, anchor='c')
        tree.heading("1", text="Idx")
        tree.heading("2", text="Value")
        tree.heading("3", text="Package")
        tree.heading("4", text="Description")
        tree.heading("5", text="Qty")
        tree.heading("6", text="Price")
        tree.heading("7", text="Manafacturer")
        tree.heading("8", text="Distributor")


        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))

        bt_debug=Button(tab2,text="DEBUG",width = 90)
        bt_debug.place(x=30, y=298)

        childtabControl = Notebook(tab2)
        tab_issues = Frame(childtabControl,width=500,height=200)
        childtabControl.add(tab_issues, text = "ISSUES")
        self.tab_issues(tab_issues)

        tab_warnings = Frame(childtabControl)
        childtabControl.add(tab_warnings, text = "WARNINGS")

        tab_suggestions = Frame(childtabControl)
        childtabControl.add(tab_suggestions, text = "SUGGESTIONS")


        childtabControl.place(x=30,y=325)

        #label_partDetails = Label(tab2, text="Part Details")
        #label_partDetails.place(x=600,y=35)

        PartDetails = Notebook(tab2)
        PartDetails.place(x=600,y=45)
        part_Details = Frame(PartDetails,width=300,height=130)
        PartDetails.add(part_Details, text = "Part Details")
        self.part_details_fun(part_Details)

        #label_manafacturers = Label(tab2, text="Manafacturers for slected part")
        #label_manafacturers.place(x=600,y=215)

        manafacturers = Notebook(tab2)
        manafacturers.place(x=600,y=205)
        manafacturers_ = Frame(manafacturers,width=300,height=120)
        manafacturers.add(manafacturers_, text = "Manafacturers for slected part")
        self.manafactures_fun(manafacturers_)


        distributors = Notebook(tab2)
        distributors.place(x=600,y=355)
        distributors_ = Frame(distributors,width=300,height=120)
        distributors.add(distributors_, text = "Distributors for selected Manafacturers")
        self.distributors_fun(distributors_)

        bt_update_man=Button(tab2,text="Update Manafacture and Distributor",width = 50)
        bt_update_man.place(x=600, y=505)

        bt_set_preference=Button(tab2,text="Set preference",width = 50)
        bt_set_preference.place(x=600, y=530)


    def tab1(self, tab1):
        text_search = Entry(tab1,width=50)
        text_search.insert(0, "Default Text")
        text_search.place(x=450,y=10)

        bt_search=Button(tab1,text="Search")
        bt_search.place(x=780, y=10)

        bt_search=Button(tab1,text="Sync")
        bt_search.place(x=860, y=10)


        tab1_right_top = Notebook(tab1)
        tab1_right_top.place(x=450,y=35)
        tab1_id = Frame(tab1_right_top,width=480,height=200)
        tab1_right_top.add(tab1_id, text = "ID")
        
        tab1_name = Frame(tab1_right_top,width=300,height=130)
        tab1_right_top.add(tab1_name, text = "NAME")

        tab1_created = Frame(tab1_right_top,width=300,height=130)
        tab1_right_top.add(tab1_created, text = "CREATED")

        tab1_tag = Frame(tab1_right_top,width=300,height=130)
        tab1_right_top.add(tab1_tag, text = "TAG")


        tab1_right_bottom=Frame(tab1 , width=480,height=180)
        tab1_right_bottom.place(x=450,y=270)
        random_text=Label(tab1_right_bottom,text="random text")
        random_text.place(x=0,y=0)


        btn_loadexistingbom=Button(tab1,text="LOAD EXISTING BOM",width=78)
        btn_loadexistingbom.place(x=450,y=500)

        btn_createnewbom=Button(tab1,text="CREATE NEW BOM",width=78)
        btn_createnewbom.place(x=450,y=530)



    def tab4(self,tab4):
        btn_showprivacypolicy=Button(tab4,text="Show Privacy Policy")
        btn_showprivacypolicy.place(x=700,y=10)

        btn_createnewbom=Button(tab4,text="Help")
        btn_createnewbom.place(x=840,y=10)

        label_heading=Label(tab4,text="Hybrique AI Part Recommender and BOM Management Plugin",font=("Arial Bold",15))
        label_heading.place(x=200,y=50)

        label_version=Label(tab4,text="Version : 1.0",font=("Arial Bold",10))
        label_version.place(x=450,y=85)

    def Run ( self ):
        #root = Tk()
        #root.geometry("600x350")
        #root.attributes('-topmost', True)

        #l1=Label(root, text= "Hello2! ", font=('Helvetica bold', 15))
        #l1.grid(column=0,row=0)
        #win = Tk()
        #win.minsize(width=600, height=500)
        #win.attributes('-topmost', True)
        #win.resizable(width=0, height=0)
        

        win = Tk()
        win.geometry("960x650")
        win.attributes('-topmost', True)

        
        #l1=Label(win, text= "Hello2! ", font=('Helvetica bold', 15))
        #l1.grid(column=0,row=0)
        #win.resizable(width=0, height=0)

        label_heading = Label(win, text="Hybrique")
        label_heading.place(x=10,y=10)

        label_greet = Label(win, text="Welcome User")
        label_greet.place(x=700,y=10)

        btn_logout=Button(win, text="Logout")
        btn_logout.place(x=850,y=10)

        tabControl = Notebook(win)
        tab1 = Frame(tabControl)
        tabControl.add(tab1, text = "Home")
        self.tab1(tab1)


        tab2 = Frame(tabControl, width=950,height=600)
        tabControl.add(tab2, text = "Load BOM")
        self.tab2(tab2)

        tab3 = Frame(tabControl)
        tabControl.add(tab3, text = "Part Supplier Summery")

        tab4 = Frame(tabControl)
        tabControl.add(tab4, text = "About")
        self.tab4(tab4)
        #tabControl.pack(expand = 1, fill = "both")
        
        tabControl.place(x=10,y=40)

        


        """combo=Combobox(win)
        combo["values"]=(1,2,3,4,5,"Hi")
        combo.current(3)
        combo.place(x=30, y=70)

        spin=Spinbox(win,from_=0, to=100, width=10)
        spin.place(x=440, y=70)

        bt=Button(win,text="LOAD BOM")
        bt.place(x=520, y=65)

        tree = Treeview(win, selectmode='browse')
        tree.place(x=30, y=95)

        vsb = Scrollbar(win, orient="vertical", command=tree.yview)
        vsb.place(x=30+550+2, y=95, height=200+20)
        #vsb.grid(row=30+200+2, column=95, height=200+20)

        tree.configure(yscrollcommand=vsb.set)

        tree["columns"] = ("1", "2","3","4","5","6","7","8")
        tree['show'] = 'headings'
        tree.column("1", width=50, anchor='c')
        tree.column("2", width=70, anchor='c')
        tree.column("3", width=70, anchor='c')
        tree.column("4", width=100, anchor='c')
        tree.column("5", width=50, anchor='c')
        tree.column("6", width=70, anchor='c')
        tree.column("7", width=70, anchor='c')
        tree.column("8", width=70, anchor='c')
        tree.heading("1", text="Idx")
        tree.heading("2", text="Value")
        tree.heading("3", text="Package")
        tree.heading("4", text="Description")
        tree.heading("5", text="Qty")
        tree.heading("6", text="Price")
        tree.heading("7", text="Manafacturer")
        tree.heading("8", text="Distributor")


        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        tree.insert("",'end',text="L1",values=("1","10R","R0603","RESISTOR, American symbol","1","0.1","Multicomp","Newark"))
        """

        win.mainloop()


        pcb = pcbnew.GetBoard()


Hybrique().register()