

import customtkinter
import os, sys,string, math, time
#import ouplib, dialogs, tools, reports, nodes, auxiliaries, distmatrixtype, Pmw
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog
import tkinter as Tkinter
from tkinter import filedialog as tkFileDialog
from random import randint

class App(customtkinter.CTk):
    def __init__(self):  # a special method (constructor) that gets called when an instance of the App class is created.
        super().__init__() # To set up the basic properties of the window (such as size and title)
        self.geometry("1000x800") # WINDWOW size,1000x800 pixels 
        self.title("CTk example")

        # add widgets to app
        self.button = customtkinter.CTkButton(self, command=self.button_click)
        self.button.grid(row=0, column=0, padx=20, pady=10)

    # add methods to app
    def button_click(self): # This method is associated with the button widget
        print("button click")



try:
    import psyco
    psyco.profile()
except ImportError:
    pass

#########################################################################################################
class GUI:
    def __init__(self, root, trigger=None):
        self.root = root
        self.trigger = trigger
        self.selected_item = ""
        self.balloon = None
        if self.root:
            self.balloon = Pmw.Balloon(self.root)
            self.menuBar = Pmw.MainMenuBar(self.root, balloon=self.balloon)
            self.root.config(menu=self.menuBar)
        
        # FLAGS
        self.flg_has_changed = 0
        
    def buildMenu(self):
        pass
        
    def do(self, ArgList):
        if self.trigger:
            return self.trigger(ArgList)
        
    def buildWindow(self):
        # Frame Set
        frame_buttonBar = Tkinter.Frame(self.root)
        frame_buttonBar.pack(anchor='nw')

        self.frame_mainWindow = Tkinter.Frame(self.root)
        self.frame_mainWindow.pack(anchor='w', expand=1, fill=Tkinter.Y)
        # Event Handlers
        self.frame_mainWindow.bind("<Destroy>", self.exit)

        self.frame_statusBar = Tkinter.Frame(self.root)
        self.frame_statusBar.pack(anchor='sw', expand=1, fill=Tkinter.X)
        
        self.frame_left = Tkinter.Frame(self.frame_mainWindow, bd=2, relief=Tkinter.SUNKEN)
        self.frame_left.pack(side=Tkinter.LEFT, anchor="w", expand=1, fill=Tkinter.Y)
        
        # Scrolled frame_list
        self.frame_commands = Tkinter.Frame(self.frame_left, bd=2, relief=Tkinter.SUNKEN)
        self.frame_commands.pack(side=Tkinter.TOP, expand=0, fill=Tkinter.X)

        self.frame_title = Tkinter.Frame(self.frame_left)
        self.frame_title.pack(side=Tkinter.TOP, expand=0, fill=Tkinter.X)

        self.frame_buttons = Tkinter.Frame(self.frame_title)
        self.frame_buttons.pack(side=Tkinter.RIGHT, expand=0, fill=None)
        
        frame_list = Tkinter.Frame(self.frame_left, bd=2, relief=Tkinter.SUNKEN)
        frame_list.pack(side=Tkinter.BOTTOM, expand=1, fill=Tkinter.BOTH)
        
        f1 = Tkinter.Frame(frame_list)
        f1.pack(side=Tkinter.TOP, expand=1, fill=Tkinter.BOTH)

        f2 = Tkinter.Frame(frame_list)
        f2.pack(side=Tkinter.TOP, expand=1, fill=Tkinter.X)
        
        self.yscrollbar = Tkinter.Scrollbar(f1, orient=Tkinter.VERTICAL)
        self.xscrollbar = Tkinter.Scrollbar(f2, orient=Tkinter.HORIZONTAL)
        self.listbox = Tkinter.Listbox(f1,
                                       height=30,
                                       width=50,
                                       exportselection=0,
                                       yscrollcommand=self.yscrollbar.set,
                                       xscrollcommand=self.xscrollbar.set)
        self.listbox.bind("<Button-1>", self.listboxOnClick)
        self.listbox.bind("<Double-Button-1>", self.listboxOnDoubleClick)
        self.listbox.bind("<Button-2>", self.listboxOnRightClick)
        self.listbox.bind("<Button-3>", self.listboxOnRightClick)
        self.listbox.bind("<Control-Button-1>", self.listboxOnControlClick)
        self.listbox.bind("<Shift-Button-1>", self.listboxOnShiftClick)
        self.listbox.bind("<Control-KeyPress-A>", self.selectall_onclick)
        self.setlistbox()
        self.yscrollbar.config(command=self.listbox.yview)
        self.xscrollbar.config(command=self.listbox.xview)

        self.listbox.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=1)
        self.yscrollbar.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
        self.xscrollbar.pack(side=Tkinter.TOP, fill=Tkinter.X)

        self.listbox.select_set(0)
        self.listbox.see(0)
        
        self.oStatus = StatusBar(self.frame_statusBar, self.do)
        self.balloon.configure(statuscommand=self.oStatus._messagebar.helpmessage, state='status')

        self.list_title = Tkinter.Label(self.frame_title, text="")
        self.list_title.pack(side=Tkinter.LEFT)
        
        self.frame_right = None
        self.command_buttons = None
    
    # Notebook
    # pages = ["name",...];
    def get_notebook(self, parent, pages, width=650):
        # Notebook
        notebook = Pmw.NoteBook(parent,
                                pagemargin=0,
                                borderwidth=2)
        notebook.pack(side=Tkinter.RIGHT, expand=1, fill=Tkinter.BOTH)
        for pagename in pages:
            notebook.add(pagename)
        notebook.component('hull')['width'] = width
        return notebook
    
    def currselection(self):
        return list(self.listbox.curselection())
        
    def open_option_from_list(self, option):
        pass
        
    def setlistbox(self):
        pass
        
    def setFileName(self, fname):
        self.oViewer.setFileName(fname)
        
    def getFileName(self):
        return self.oViewer.getFileName()
        
    def selectall_onclick(self, event=None):
        self.listbox.select_set(0, Tkinter.END)
        self.selected_item = ""
        
    def invert_onclick(self, event=None):
        selection = self.listbox.curselection()
        self.listbox.select_set(0, Tkinter.END)
        for i in selection:
            self.listbox.select_clear(i)
        self.selected_item = ""
        
    def deselect_onclick(self, event=None):
        self.listbox.select_clear(0, Tkinter.END)
        self.selected_item = ""
        
    def listboxOnClick(self, event):
        self.selected_item = self.listbox.nearest(event.y)
        
    def listboxOnDoubleClick(self, event):
        option = self.listbox.nearest(event.y)
        self.open_option_from_list(self.options[option])

    def listboxOnRightClick(self, event):
        pass
        
    def listboxOnControlClick(self, event):
        self.selected_item = self.listbox.nearest(event.y)
        self.listbox.select_set(self.selected_item)
        
    def listboxOnShiftClick(self, event):
        selected_item = self.listbox.nearest(event.y)
        if not self.selected_item:
            self.selected_item = selected_item
            self.listbox.select_set(self.selected_item)
        else:
            items = [self.selected_item, selected_item]
            items.sort()
            self.listbox.select_set(items[0], items[1])
            self.selected_item = selected_item
        
    def notebook_onselect(self, event):
        print(event)
        
    def setChanged(self, val=1):
        self.flg_has_changed = val
        
    def has_changed(self):
        return self.flg_has_changed
    
    # EVENTS
    def exit(self, event=None):
        pass

class MainWinInterface(GUI):
    def __init__(self, root, cdr):
        super().__init__(root)
        
        # General settings
        self.curDir = ""
        self.maindir = sys.path[0]
        if "library.zip" in self.maindir:
            self.maindir = self.maindir[:-11]
        self.cdr = cdr
        self.temporary_database_folder = os.path.join(os.getcwd(), "lib", "tmp")
        self.pattern_type = "n"
        self.normalization = 1
        self.word_length = 4
        self.thresholds = [90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
        self.seqLengthLimitations = [600, 1200, 5000, 18500, 74000, 295000]
        self.buffer_size = 500
        
        self.getOptionsByDefault()
        # create a low level store to manage the database patterns
        self.store = Store(self.buffer_size, self.do)
        
        self.workspaces = {}
        self.Builder = WorkSpace(self.do)
        self.oDbEditor = None
        self.extensions = ['FNA', 'FAS', 'FST', 'FASTA', 'GB', 'GBK', 'GBFF']
        self.report_number = 0
        # current directory
        if not os.path.isdir(self.cdr):
            self.cdr = os.getcwd()
        self.objectlist = []
        
        self.active_file = None
        self.flg_subfoldermode = 0
        
        if self.root:
            self.root.title("SeqWord MetaLingvo 1.0")
            self.buildMenu()
            self.buildWindow()
            self.specifyUI()
            
            # TABS
            self.notebook = None
            self.tabs = {"Associations": None, "Report": None, "Colorpad": None}
        
            self.clean()
        
    # Trigger
    def do(self, option, ArgList=None):
        if option == "Process":
            self.process(ArgList)
        elif option == "Remove page":
            self.notebook.delete(ArgList)
            if self.notebook.getcurselection() is None:
                self.frame_right.destroy()
                self.frame_right = None
                self.notebook = None
        elif option == "Get sequence":
            fname = ArgList[0]
            seqnames = []
            if len(ArgList) > 1:
                seqnames.extend(ArgList[1])
            return self.Builder.getSequence(fname, seqnames)
        elif option == "Get pattern":
            return self.getPattern(ArgList)
        elif option == "Compare patterns":
            first, second, pattern_type = ArgList
            return self.comparePatterns(first, second, pattern_type)
        elif option == "Print report":
            self.print_report(ArgList)
        elif option == "Pickup report":
            # ArgList is a report object
            self.pickup_workspace(ArgList, "report")
        elif option == "Recalculate":
            id, info, elements = ArgList
            self.recalculate_watchtowers(id, info, elements)
        elif option == "Copy":
            elements, oInfo = ArgList
            self.copy_to_FASTA(elements, oInfo)
        elif option == "Get list of viewers":
            return list(self.treeviewers.keys())
        elif option == "Rename identification table":
            old_name, new_name = ArgList
            oIdentifier = auxiliaries.Identifier(self.root, self.do)
            oIdentifier.rename_table(old_name, new_name)
            del oIdentifier
        elif option == "Open database editor":
            self.openDbEditor(ArgList)
        elif option == "Remove database editor":
            self.oDbEditor = None
        elif option == "Warn sequence length":
            return self.warnSeqLength()
        elif option == "Parse pattern type":
            return self.parse_patternType(ArgList)
        elif option == "Update database":
            if self.oDbEditor:
                self.oDbEditor.exit()
                self.oDbEditor = DatabaseInterface(tkinter.Toplevel(self.root), self.do)
        elif option == "Save image":
            self.save_image(ArgList)
        elif option == "Help":
            if ArgList == "get":
                self.menu_Help_show()
            elif ArgList == "about":
                self.menu_Help_about()
            elif ArgList == "license":
                pass
            else:
                pass
        elif option == "Get current directory":
            return self.curDir
        elif option == "Get main directory":
            return self.maindir
        elif option == "Get temporary database folder":
            return self.temporary_database_folder
        elif option == "Get pattern type settings":
            return self.pattern_type, self.normalization, self.word_length
        elif option == "Get thresholds":
            thresholds = []
            thresholds.extend(self.thresholds)
            return thresholds
        elif option == "Get buffer size":
            return self.buffer_size
        elif option == "Store pattern":
            oPattern, key = ArgList
            self.store.add(oPattern, key)
        elif option == "Store distance":
            first, second, distance = ArgList
            self.store.setDistance(first, second, distance)
        else:
            return None

    def getOptionsByDefault(self):
        fname = os.path.join(os.getcwd(), "lib", "options")
        if not os.path.isfile(fname):
            return None
        try:
            options = tools.openDBFile(fname)[0]
        except:
            os.remove(fname)
            self.setOptionsByDefault()
            return
        self.cdr = options["source data"]
        self.pattern_type = options["pattern type"]
        self.normalization = options["normalization"]
        self.word_length = options["word length"]
        self.thresholds = options["thresholds"]
        self.buffer_size = options["buffer size"]

    def setOptionsByDefault(self, settings=None):
        fname = os.path.join(os.getcwd(), "lib", "options")
        options = {"source data": self.cdr,
                    "pattern type": self.pattern_type,
                    "normalization": self.normalization,
                    "word length": self.word_length,
                    "thresholds": self.thresholds,
                    "buffer size": self.buffer_size}
        if os.path.isfile(fname):
            try:
                options = tools.openDBFile(fname)[0]
            except:
                os.remove(fname)
        if settings:
            for key in settings.keys():
                if key in options:
                    options[key] = settings[key]
        else:
            options = {"source data": self.cdr,
                        "pattern type": self.pattern_type,
                        "normalization": self.normalization,
                        "word length": self.word_length,
                        "thresholds": self.thresholds,
                        "buffer size": self.buffer_size}
        tools.saveDBFile(options, fname)
# Menu
    def buildMenu(self):
        self.menuBar.addmenu('File', 'File')
        self.menuBar.addcascademenu('File', 'Open', 
            'Open files of different types', 
            traverseSpec = 'z', tearoff = 1)
        menuCommands = [["workspace", self.menu_file_openWorkSpace],
                        ["dataset", self.menu_file_openDataSet],
                        ["projection", self.menu_file_openProjection],
                        ["cluster tree", self.menu_file_openClusterTree],
                        ["report", self.menu_file_openReport]]
                        #["phylogenetic tree", self.menu_file_openPhylogeneticTree],
                        #["text file", self.menu_file_openTextFile]]
        for menuoption in menuCommands:
            self.menuBar.addmenuitem('Open', 'command', f"Open {menuoption[0]}",
            command = menuoption[1],
            label = menuoption[0])
        self.menuBar.addmenuitem('File', 'command', 'Convert to FASTA files',
            command = self.menu_file_convertToFASTA,
            label = 'Convert to FASTA...')
        self.menuBar.addmenuitem('File', 'separator') 
        self.menuBar.addmenuitem('File', 'command', 'Exit',
            command = self.menu_file_exit,
            label = 'Exit')

        self.menuBar.addmenu('Command', 'Main functions')
        self.menuBar.addmenuitem('Command', 'command', 'Process',
            command = self.menu_command_process,
            label = 'Process dataset')
        self.menuBar.addmenuitem('Command', 'command', 'Strait identification',
            command = self.menu_command_straitIdentification,
            label = 'Identify sequences')
        '''
        self.menuBar.addmenuitem('Command', 'command', 'Dataset identification',
            command = self.menu_command_advancedIdentification,
            label = 'Identify the dataset')
        '''
        
        self.menuBar.addmenu('Database', 'Arrange the database')
        self.menuBar.addmenuitem('Database', 'command', 'Edit',
            command = self.menu_database_edit,
            label = 'Edit...')
        self.menuBar.addmenuitem('Database', 'command', 'Add sequences',
            command = self.menu_database_addSequences,
            label = 'Add sequences...')

        self.menuBar.addmenu('Preferences', 'Options')
        self.menuBar.addmenuitem('Preferences', 'command', 'Show current set',
            command = self.menu_preferences_showCurrentOptionsByDefault,
            label = 'Show current set')
        self.menuBar.addmenuitem('Preferences', 'separator')
        self.menuBar.addmenuitem('Preferences', 'command', 'Set pattern type',
            command = self.menu_preferences_setPatternType,
            label = 'Pattern type')
        self.menuBar.addmenuitem('Preferences', 'command', 'Set start directory',
            command = self.menu_preferences_setStartDirectory,
            label = 'Start directory')
        self.menuBar.addmenuitem('Preferences', 'command', 'Set buffer size',
            command = self.menu_preferences_setBufferSize,
            label = 'Buffer size')
        self.menuBar.addmenuitem('Preferences', 'separator')
        self.menuBar.addmenuitem('Preferences', 'command', 'Set current settings by default',
            command = self.menu_preferences_saveCurrentSettings,
            label = 'Save current settings')
            
        self.menuBar.addmenu('Phylogeny', 'Options')
        self.menuBar.addmenuitem('Phylogeny', 'command', 'Distance matrix',
            command = self.menu_phylogeny_distanceMatrix,
            label = 'Distance matrix')
        '''
        self.menuBar.addmenuitem('Phylogeny', 'command', 'Neighbour joining phylogenetic tree',
            command = self.menu_phylogeny_neighbourJoining,
            label = 'Neighbour joining')
        self.menuBar.addmenuitem('Phylogeny', 'command', 'Fitch phylogenetic tree',
            command = self.menu_phylogeny_fitch,
            label = 'Fitch-Margoliash')
        self.menuBar.addmenuitem('Phylogeny', 'command', 'Kitch phylogenetic tree',
            command = self.menu_phylogeny_kitsch,
            label = 'Fitch-Margoliash with clock')
        '''
        
        self.menuBar.addmenu('?', 'Options')
        self.menuBar.addmenuitem('?', 'command', 'Help text',
            command = self.menu_Help_show,
            label = 'Help')
        self.menuBar.addmenuitem('?', 'command', 'About',
            command = self.menu_Help_about,
            label = 'About')
        '''
        self.menuBar.addmenuitem('?', 'command', 'License',
            command = self.menu_Help_license,
            label = 'License agreement')
        '''

    def specifyUI(self):
        # Add buttons
        btnProcess = tkinter.Button(self.frame_commands, text="Process ", command=self.btn_process_onclick)
        btnProcess.pack(side=tkinter.LEFT, padx=2)
        btnIdentify = tkinter.Button(self.frame_commands, text="Identify ", command=self.btn_identify_onclick)
        btnIdentify.pack(side=tkinter.LEFT, padx=2)
        #btnTest = tkinter.Button(self.frame_commands, text="Test", command=self.test)
        #btnTest.pack(side=tkinter.LEFT, padx=2)

        # Add image buttons
        imagepath = "images"
        try:
            self.img_open = tkinter.PhotoImage(file=os.path.join(imagepath, "open.gif"))
            self.img_uplevel = tkinter.PhotoImage(file=os.path.join(imagepath, "uplevel.gif"))
            self.img_single_selection = tkinter.PhotoImage(file=os.path.join(imagepath, "single_selection.gif"))
            self.img_multiple_selection = tkinter.PhotoImage(file=os.path.join(imagepath, "multiple_selection.gif"))
            self.img_select_all = tkinter.PhotoImage(file=os.path.join(imagepath, "select_all.gif"))
            self.img_invert_selection = tkinter.PhotoImage(file=os.path.join(imagepath, "invert_selection.gif"))
            self.img_deselect = tkinter.PhotoImage(file=os.path.join(imagepath, "deselect.gif"))
        except:
            imagepath = os.path.join("lib", "images")
            self.img_open = tkinter.PhotoImage(file=os.path.join(imagepath, "open.gif"))
            self.img_uplevel = tkinter.PhotoImage(file=os.path.join(imagepath, "uplevel.gif"))
            self.img_single_selection = tkinter.PhotoImage(file=os.path.join(imagepath, "single_selection.gif"))
            self.img_multiple_selection = tkinter.PhotoImage(file=os.path.join(imagepath, "multiple_selection.gif"))
            self.img_select_all = tkinter.PhotoImage(file=os.path.join(imagepath, "select_all.gif"))
            self.img_invert_selection = tkinter.PhotoImage(file=os.path.join(imagepath, "invert_selection.gif"))
            self.img_deselect = tkinter.PhotoImage(file=os.path.join(imagepath, "deselect.gif"))
        self.subfolder_mode = tkinter.Checkbutton(self.frame_buttons, text="Including subfolders", command=self.set_subfoldermode)
        self.subfolder_mode.pack(side=tkinter.LEFT)
        btn_open = tkinter.Button(self.frame_buttons, image=self.img_open, command=self.open_onclick)
        btn_open.pack(side=tkinter.LEFT)

# Methods

def process(self, filelist):
    # Set pattern options
    settings = self.choosePatternType()
    if not settings:
        return
    self.setPatternType(settings)
    elements = []
    seqnames = []
    for fname in filelist:
        elements.extend(filelist[fname])
        seqnames.append(fname)
    start = 0
    TOTAL = len(filelist)
    oTree = None
    # Create new workspace
    workspace_id = tools.randomizer("nnn_#nnnnn", self.workspaces.keys())
    self.workspaces[workspace_id] = WorkSpace(self.do, workspace_id, self.root, settings['name'])
    self.workspaces[workspace_id].setPatternType(self.pattern_type + str(self.normalization) +
                                                 "_" + str(self.word_length) + "mer")
    counter = 0
    while start < TOTAL:
        stop = start + 500
        if stop >= TOTAL:
            stop = None
        subset_of_files = {}
        for fname in seqnames[start:stop]:
            subset_of_files[fname] = filelist[fname]
        # Process sequences: calculate patterns and store them to the temporary files
        print("Processing of the source sequences...")
        self.workspaces[workspace_id].processSequences(subset_of_files)
        # Add patterns to a database and search for the most distant patterns
        print("\nSetting of watchtowers...")
        self.workspaces[workspace_id].append(elements, counter)
        start = stop
        counter += 1
        if start is None:
            break
    return [workspace_id, counter]

def recalculate_watchtowers(self, workspace_id, info, elements):
    if not elements:
        return
    new_workspace_id = tools.randomizer("nnn_#nnnnn", self.workspaces.keys())
    missed_seq = {}
    curr_files = {}
    if workspace_id:
        curr_files.update(self.workspaces[workspace_id].getSeqLocationInfo())
    flg_setting_changed = None
    settings = self.choosePatternType(workspace_id)
    if settings is None:
        return
    if settings:
        flg_setting_changed = self.setPatternType(settings)
    self.workspaces[new_workspace_id] = WorkSpace(self.do, new_workspace_id, self.root)
    self.workspaces[new_workspace_id].setPatternType(self.pattern_type + str(self.normalization) +
                                                     "_" + str(self.word_length) + "mer")
    for item in elements:
        if flg_setting_changed or item not in curr_files:
            if info[item]['path'] not in missed_seq:
                missed_seq[info[item]['path']] = [info[item]['seqname']]
            else:
                missed_seq[info[item]['path']].append(info[item]['seqname'])
        elif not flg_setting_changed and workspace_id:
            self.workspaces[workspace_id].copy(new_workspace_id)
            self.workspaces[new_workspace_id].setSeqLocationInfo(self.workspaces[workspace_id].getSeqLocationInfo())
        else:
            continue
    if missed_seq:
        # Process sequences: calculate patterns and store them to the temporary files
        print("Processing of missed sequences...")
        self.workspaces[new_workspace_id].processSequences(missed_seq, 1)
    oTree = self.workspaces[new_workspace_id].setWatchtowers(elements)
    self.workspaces[new_workspace_id].showTree(0, oTree)
    self.workspaces[new_workspace_id].setChanged()

def copy_to_FASTA(self, elements, info):
    folder = tkinter.filedialog.askdirectory()
    if not folder:
        return
    for element in elements:
        seqlist = self.Builder.getSequence(info[element]['path'])
        if not seqlist:
            continue
        fname = element + ".fst"
        path = os.path.join(folder, fname)
        with open(path, "w") as f:
            for seqname in seqlist:
                f.write(f">{element}\n{seqlist[seqname]}\n")

def convertToFASTA(self, source_filelist, seqnum, path):
    seq_counter = 0
    file_counter = 1
    output = ""
    for source_fname in source_filelist:
        seqlist = self.Builder.getSequence(source_fname, source_filelist[source_fname])
        if not seqlist:
            continue
        for seqname in seqlist:
            if seqnum == 1:
                fname = seqname
                for symbol in ("\\", "/", "|", "?", ":", "\"", "<", ">", "*"):
                    fname = fname.replace(symbol, "_")
                fname = os.path.join(path, fname + ".fst")
                with open(fname, "w") as f:
                    f.write(f">{seqname}\n{seqlist[seqname]}")
            else:
                if seq_counter == seqnum:
                    fname = path + "#" + str(file_counter) + ".fst"
                    with open(fname, "w") as f:
                        f.write(output[:-1])
                    file_counter += 1
                    output = ""
                else:
                    output += f">{seqname}\n{seqlist[seqname]}\n"
                    seq_counter += 1
    if output:
        fname = path + "#" + str(file_counter) + ".fst"
        with open(fname, "w") as f:
            f.write(output[:-1])

def getSeqFromFASTA(self, fname, names=[]):
    return self.Builder.getSeqFromFASTA(fname, names)

def strait_identification(self):
    filelist = self.getFileList()
    if not filelist:
        return
    result = self.warnSeqLength()
    if not result:
        return
    oIdentifier = auxiliaries.Identifier(self.root, self.do)
    report = oIdentifier.identify_sequences(filelist)
    if report:
        self.print_report(report)

def console_identification(self, fname, dbname):
    oIdentifier = auxiliaries.Identifier(self.root, self.do)
    report = oIdentifier.identify_sequences(fname, dbname)
    if report:
        return self.identificationReport2text(report['report'])
    else:
        return ""

def console_flatClustering(self, source, wlength, norm):
    # Set pattern type options
    settings = {'name': '', 'thresholds': [90, 80, 70, 60, 50, 40, 30, 20, 10, 0], 
                'normalization': norm, 'pattern type': 'n', 'word length': wlength}
    self.setPatternType(settings)
    # Create new workspace without GUI
    workspace_id = tools.randomizer("nnn_#nnnnn", self.workspaces.keys())
    self.workspaces[workspace_id] = WorkSpace(self.do, workspace_id, None, settings['name'])
    self.workspaces[workspace_id].setPatternType(self.pattern_type + str(self.normalization) +
                                                 "_" + str(self.word_length) + "mer")
    # Read and process the FASTA file 'source'
    self.workspaces[workspace_id].processSequences(source)
    # Create an object of the class nodes.Node
    oTree = self.workspaces[workspace_id].setWatchtowers()
    # Create an object of the class reports.TreeViewer
    oTreeViewer = reports.TreeViewer(None, self.workspaces[workspace_id].do)
    oTreeViewer.setTreeObject(oTree, self.workspaces[workspace_id].pattern_type)
    
    # Multidimensional projection
    # Set references
    references = oTree.getListOfOutermosts(oTreeViewer.getThreshold())
    size = len(oTree.getLeaves())
    
    while len(references) < 15 and len(references) != size:
        threshold = oTreeViewer.getThreshold() - 5
        if threshold < 0:
            threshold = 0
        oTreeViewer.setThreshold(threshold)
        references = oTree.getListOfOutermosts(oTreeViewer.getThreshold())
    # Create a projection - reports.TView object
    result = oTreeViewer.getProjection(self.workspaces[workspace_id].do, references)
    if not result:
        raise IOError("Error creating the projection!")
    oProjection, elements = result
    if not oProjection:
        raise IOError("Projection is empty!")
    oProjection.showProjection()
    # oProjection.container is a auxiliaries.Container object - collection of
    # clusters, leave elements and their coordinates in the multidimensional space
    
    # Check space resolution
    resolution = oProjection.resolution()
    while resolution < 0.75:
        dim = oProjection.dimension() + 1
        if dim > size - 1 or dim > 20:
            break
        oProjection.showProjection(dim)
        if resolution >= oProjection.resolution():
            oProjection.showProjection(dim - 1)
            break
        resolution = oProjection.resolution()
        # CLUSTER TREE
    def cluster_tree(self, oTree, size):
        branch_distribution = {}
        for i in range(1, len(self.thresholds)):
            branch_distribution[self.thresholds[i]] = oTree.getBranching(i)
        branch_distribution[0] = size

        oClusterTree = oProjection.generateTableObj("", [70, 50, 30, 20])
        oGroups = oClusterTree.getGroups()
        leaves = oGroups.get_leaf_elements()
        if not leaves:
            raise IOError("List of sequences is empty!")
        leaves.sort(key=tools.sortAlfabetically)
        report = ""
        for name, cluster in leaves:
            if not cluster:
                report += name + "\tNone\t"
            else:
                report += name + "\t" + cluster + "\t"
            path = oGroups.getSpeciesIndex(name)[1:]
            path.reverse()
            report += ".".join(path) + "\n"

        del self.workspaces[workspace_id]
        return report

    def add_patterns(self):
        filelist = self.getFileList()
        if not filelist:
            return
        oIdentifier = auxiliaries.Identifier(self.root, self.do)
        result = oIdentifier.select_tables("All")
        if not result:
            return
        tables, supplementary = result
        for names in tables:
            tbname, pattern_type = names.split(":")
            pattern_list = {}
            for fname in filelist:
                seqlist = self.Builder.getSequence(fname, filelist[fname])
                if not seqlist:
                    print("\tError processing the file " + tools.basename(fname))
                    continue
                for seqname in seqlist:
                    newseqname = self.Builder.check_seqname(seqname, [])
                    oPattern = self.getPattern([newseqname, pattern_type, fname, seqlist[seqname]])
                    if not oPattern:
                        continue
                    print("Adding pattern '" + newseqname + "'")
                    try:
                        result = oIdentifier.add_pattern(newseqname, oPattern, tbname, pattern_type, fname)
                    except Exception as e:
                        print("Error!\tPattern '" + newseqname + "' was not added to the database!")
                    if not result:
                        break
        self.openDbEditor(oIdentifier.getUpdatedTables())

    def warnSeqLength(self):
        question = ("Sequences must be at least:\n\t" +
                    str(self.seqLengthLimitations[0] / 1000.0) + " kbp for 2mer;\n\t" +
                    str(self.seqLengthLimitations[1] / 1000.0) + " kbp for 3mer;\n\t" +
                    str(self.seqLengthLimitations[2] / 1000.0) + " kbp for 4mer;\n\t" +
                    str(self.seqLengthLimitations[3] / 1000.0) + " kbp for 5mer;\n\t" +
                    str(self.seqLengthLimitations[4] / 1000.0) + " kbp for 6mer;\n\t" +
                    str(self.seqLengthLimitations[5] / 1000.0) + " kbp for 7mer;\nidentification. Do you want to continue?")
        if messagebox.askquestion("Warning!", question) == "no":
            return None
        else:
            return 1

    def setObjectlist(self):
        self.objectlist = []
        if self.active_file:
            self.objectlist = self.getSequences()
        else:
            l = os.listdir(self.cdr)
            for fname in l:
                if os.path.isdir(os.path.join(self.cdr, fname)):
                    self.objectlist.append("[" + fname + "]")
                    continue
                if self.checkExtension(fname):
                    self.objectlist.append(fname)
        if self.objectlist:
            self.objectlist.sort(key=self.sortFiles)
        self.objectlist.insert(0, "[..]")

    def checkExtension(self, fname):
        dot = fname.rfind(".")
        if dot > 0 and dot < len(fname) - 1 and fname[dot + 1:].upper() in self.extensions:
            return 1
        else:
            return 0

    def clean(self):
        tmpPath = os.path.join(os.curdir, self.temporary_database_folder)
        for dirname in os.listdir(tmpPath):
            if not dirname:
                continue
            if os.path.isdir(os.path.join(tmpPath, dirname)) and dirname not in self.workspaces:
                for fname in os.listdir(os.path.join(tmpPath, dirname)):
                    try:
                        os.remove(os.path.join(tmpPath, dirname, fname))
                    except:
                        pass
                try:
                    os.rmdir(os.path.join(tmpPath, dirname))
                except:
                    pass
            else:
                try:
                    os.rmdir(os.path.join(tmpPath, dirname))
                except:
                    pass

    def getSequences(self):
        return self.Builder.getSequence(os.path.join(self.cdr, self.active_file)).keys()

    def setlistbox(self):
        self.listbox.delete(0, Tkinter.END)
        self.setObjectlist()
        for item in self.objectlist:
            self.listbox.insert(Tkinter.END, item)

    def open_option_from_list(self, index=None):
        if index is None:
            curselection = self.listbox.curselection()
            if not curselection:
                return
            index = int(curselection[0])
        element = self.objectlist[index]
        if element == "[..]":
            self.uplevel_onclick()
            return
        elif self.active_file:
            return
        elif element[0] == "[" and element[-1] == "]":
            self.cdr = os.path.join(self.cdr, element[1:-1])
        else:
            self.active_file = element
            self.list_title["text"] = "List of sequences:"
            self.subfolder_mode["state"] = Tkinter.DISABLED
        self.setlistbox()

    def getFileList(self, selected_objects=None):
        filelist = {}
        if not selected_objects:
            selected_objects = self.listbox.curselection()
        if not selected_objects:
            return
        if self.active_file:
            fname = os.path.join(self.cdr, self.active_file)
            filelist[fname] = []
            for ind in selected_objects:
                ind = int(ind)
                if ind:
                    filelist[fname].append(self.objectlist[ind])
        else:
            for ind in selected_objects:
                ind = int(ind)
                if ind == 0:
                    continue
                objname = self.objectlist[int(ind)]
                if objname[0] == "[" and objname[-1] == "]":
                    for fname in self.getFilesFromFolder(os.path.join(self.cdr, objname[1:-1])):
                        filelist[fname] = []
                else:
                    filelist[os.path.join(self.cdr, objname)] = []
        return filelist

    def getFilesFromFolder(self, dirname):
        filelist = []
        for objname in os.listdir(dirname):
            if self.flg_subfoldermode and os.path.isdir(os.path.join(dirname, objname)):
                for fname in self.getFilesFromFolder(os.path.join(dirname, objname)):
                    filelist.append(fname)
            elif os.path.isfile(os.path.join(dirname, objname)):
                filelist.append(os.path.join(dirname, objname))
            else:
                pass
        return filelist

    def choosePatternType(self, workspace_id=None):
        if workspace_id:
            self.pattern_type, self.normalization, self.word_length = self.workspaces[workspace_id].parsePatternType()
        dialog = dialogs.SetPatternType(self.root, self.pattern_type, self.normalization, self.word_length, self.thresholds)
        dialog.showAppModal()
        return dialog.get()

def setPatternType(self, settings):
    flg_settings_changed = None
    if not settings:
        return flg_settings_changed
    if settings["pattern type"] and self.pattern_type != settings["pattern type"]:
        self.pattern_type = settings["pattern type"]
        flg_settings_changed = 1
    if settings["normalization"] is not None and self.normalization != settings["normalization"]:
        self.normalization = settings["normalization"]
        flg_settings_changed = 1
    if settings["word length"] and self.word_length != settings["word length"]:
        self.word_length = settings["word length"]
        flg_settings_changed = 1
    if settings["thresholds"]:
        settings["thresholds"].sort(reverse=True)
        if settings["thresholds"] and settings["thresholds"][-1] != 0:
            settings["thresholds"].append(0)
        if self.thresholds != settings["thresholds"]:
            self.thresholds = []
            self.thresholds.extend(settings["thresholds"])
            flg_settings_changed = 1
    return flg_settings_changed

def print_report(self, report=None):
    # Create right frame
    if not self.frame_right:
        self.buildRightPanel()
    self.report_number += 1
    pagename = f"Report #{self.report_number}"
    oReport = reports.ReportPanel(self.notebook.add(pagename), self.do, None, pagename)
    self.notebook.selectpage(pagename)
    self.notebook.setnaturalsize()
    oReport.print_report(report)

def print_text_report(self, report):
    strText = self.identificationReport2text(report)
    ouplib.TextEditor("Results of identification", strText)

def parse_report(self, report, tbname=""):
    result = []
    for cluster_name in report:
        if not report[cluster_name]:
            result.append(["0", "", cluster_name, tbname])
        else:
            for species in report[cluster_name]:
                if isinstance(report[cluster_name][species], list):
                    euclidian_distance, corrected_distance = report[cluster_name][species]
                    result.append([euclidian_distance, corrected_distance, species, cluster_name, tbname])
                else:
                    inter = self.parse_report(report[cluster_name][species]["result"],
                                              f"{species} [{tools.format_number(report[cluster_name][species]['stDev'], 3)}]")
                    result.extend(inter)
    return result

def identificationReport2text(self, report):
    strText = ""
    if report:
        DNA_reads = list(report.keys())
        DNA_reads.sort(key=tools.sortAlphabetically)
        for seqname in DNA_reads:
            strText += seqname + "\n"
            flg_identified = False
            for tbname in report[seqname]:
                if not report[seqname][tbname]["result"]:
                    continue
                result = []
                for item in self.parse_report(report[seqname][tbname]["result"]):
                    result.append(item)
                result.sort()
                flag = 0
                for item in result:
                    strText += (f"{item[4]}\t{item[2]}\t{tools.format_number(item[0], 2)}"
                                f"-{tools.format_number(item[1], 2)} [{tools.format_number(report[seqname][tbname]['stDev'], 2)}]:\n")
                    flag = 1
                flg_identified = True
            if not flg_identified:
                strText += "\tNot identified\n"
    return strText

def parse_patternType(self, pattern_type):
    settings = {"pattern type": pattern_type[0],
                "word length": int(pattern_type[3]),
                "normalization": int(pattern_type[1]),
                "thresholds": None}
    return settings

class MyClass:
    def openDbEditor(self, tablesToUpdate=None):
        if self.oDbEditor:
            self.oDbEditor.exit()
        if tablesToUpdate:
            self.oDbEditor = ChangedTablesInterface(Tkinter.Toplevel(self.root), tablesToUpdate, self.do)
        else:
            self.oDbEditor = DatabaseInterface(Tkinter.Toplevel(self.root), self.do)

    def open_workspace(self, fname="", dataset_type=""):
        workspace_id = tools.randomizer("nnn_#nnnnn", self.workspaces.keys())
        self.workspaces[workspace_id] = WorkSpace(self.do, workspace_id, self.root, fname)
        if dataset_type == "workspace":
            self.workspaces[workspace_id].openWorkspaceFile(fname)
            self.workspaces[workspace_id].setFileName(fname)
        elif dataset_type == "tree":
            self.workspaces[workspace_id].openTreeFile(fname)
            self.workspaces[workspace_id].showTree()
        elif dataset_type == "projection":
            self.workspaces[workspace_id].openProjectionFile(fname)
        elif dataset_type == "cluster":
            self.workspaces[workspace_id].openClusterTreeFile(fname)
        elif dataset_type == "report":
            self.workspaces[workspace_id].openReportFile(fname)
        else:
            WorkSpaceInterface(Tkinter.Toplevel(self.root), self.do, dataset_name, dataset_type, dataset)

    def pickup_workspace(self, oWS, dataset_type):
        workspace_id = tools.randomizer("nnn_#nnnnn", self.workspaces.keys())
        self.workspaces[workspace_id] = WorkSpace(self.do, workspace_id, self.root)
        if dataset_type == "report":
            self.workspaces[workspace_id].pickup_report(oWS)

    def getPattern(self, ArgList):
        options = ["", "", "", "", None]
        for i in range(len(ArgList)):
            options[i] = ArgList[i]
        seqname, pattern_type, fname, sequence, oPattern = options
        if not oPattern:
            oPattern = self.store.get(seqname)
        if oPattern:
            if oPattern.getPatternName() != pattern_type:
                oPattern = oPattern.convert(pattern_type[0], int(pattern_type[1]))
        if oPattern:
            self.store.add(oPattern, seqname)
            return oPattern
        if fname and not sequence:
            seqlist = self.Builder.getSequence(fname, [seqname, ])
            if not seqlist:
                return None
            sequence = seqlist[list(seqlist.keys())[0]]
        if sequence:
            oPattern = self.create_pattern(sequence, pattern_type)
        if not oPattern:
            db = auxiliaries.Identifier(self.root, self.do)

        if oPattern:
            self.store.add(oPattern, seqname)
            return oPattern

    def create_pattern(self, sequence, pattern_type):
        ptype = self.parse_patternType(pattern_type)
        oPattern = ouplib.Pattern(ptype["word length"])
        oPattern.setPattern(sequence, ptype["normalization"], ptype["pattern type"])
        return oPattern

    def comparePatterns(self, first, second, pattern_type):
        if isinstance(first, str):
            if self.store.hasDistance(first, second):
                return self.store.getDistance(first, second)
            else:
                patterns = []
                for pattern in (first, second):
                    if self.store.has(pattern):
                        patterns.append(self.store.get(pattern))
                    else:
                        patterns.append(self.getPattern([pattern, self.pattern_type]))
                dist = patterns[0] - patterns[1]
                if dist is not None:
                    self.store.setDistance(first, second, dist)
                return dist
        else:
            return first - second

    def save_image(self, cv):
        fname = tkFileDialog.asksaveasfilename(filetypes=[("PostScript file", "*.eps")])
        if fname:
            tmp = fname.split('.')
            if tmp[-1] != 'eps':
                ext = '.eps'
            else:
                ext = fname[-4:]
                fname = fname[:-4]
        else:
            return None

        mode = 'Whole image'
        hborders = cv.xview()
        lborder = hborders[0]
        rborder = hborders[1]
        img_width = rborder - lborder
        vborders = cv.yview()
        top = vborders[0]
        bottom = vborders[1]
        img_height = bottom - top

        if mode == 'Whole image' or mode == 'Banch of images':
            if lborder > 0 or rborder < 1:
                cvwidth = 1000.0 / float(img_width)
            else:
                cvwidth = 1000.0
            if top > 0 or bottom < 1:
                cvheight = 600.0 / float(img_height)
            else:
                cvheight = 600.0
            cv.xview('moveto', 0.0)
            cv.yview('moveto', 0.0)
        else:
            cvwidth = float(cv['width'])
            cvheight = float(cv['height'])

        banchsize = 1
        if mode == 'Banch of images':
            dialog = dialogs.WordLengthAndPatternType(self.root, 2, 1, 10,
                                                      "Select number of image files in the banch",
                                                      None, "Banch saving of image files")
            dialog.showAppModal()
            result = dialog.get()
            del dialog
            if result is None:
                return None
            else:
                banchsize = result["Word length"]
                cvwidth = cvwidth / banchsize
                step = 1.0 / float(banchsize)

        for i in range(banchsize):
            if banchsize == 1:
                currFile = fname + ext
            else:
                currFile = fname + '#' + str(i) + ext
                cv.xview('moveto', i * step)
            cv.postscript(colormode='color', colormap='RGB', width=cvwidth, height=cvheight, file=currFile)
# scroll canvas to the starting point
        if lborder != 0.0:
            cv.xview('moveto', lborder)
        if top != 0.0:
            cv.yview('moveto', top)

    def exit(self, event=None):
        for ws in self.workspaces:
            self.workspaces[ws].exit()
        self.workspaces = {}
        self.clean()
        self.root.destroy()

    def test(self):
        filelist = self.getFileList()
        if not filelist:
            return
        filelist = list(filelist.keys())
        filelist.sort()
         # Set pattern options
        settings = self.choosePatternType()
        if not settings:
            return
        self.setPatternType(settings)
        dirname = tkFileDialog.askdirectory()
        if not dirname:
            return
        for fname in filelist:
            print(fname)
            try:
                pos = fname.rfind(", complete")
                newname = fname[:pos]
                path = os.path.join(dirname, tools.basename(newname))
                workspace_id = tools.randomizer("nnn_#nnnnn", self.workspaces.keys())
                self.workspaces[workspace_id] = WorkSpace(self.do, workspace_id, self.root, fname)
                self.workspaces[workspace_id].processSequences({fname: [], })
                oTree = self.workspaces[workspace_id].setWatchtowers()
                oViewer = self.workspaces[workspace_id].showTree(0, oTree, 1)
                oViewer.show_projection()
                oViewer.setCutoff(0)
                oViewer.generate_clustertree()
                oViewer.export_genome_fragments(path)
            except:
                continue
            self.clean()
 # EVENTS
    def btn_process_onclick(self):
        result = self.process(self.getFileList())
        if not result:
            return
        workspace_id, counter = result
        self.workspaces[workspace_id].showTree(counter)
        self.workspaces[workspace_id].setChanged()

    def btn_identify_onclick(self):
        respond = ["Identify individual sequences"]
        if respond:
            if respond[0] == "Identify individual sequences":
                self.strait_identification()
            else:
                self.advanced_identification()

    def btnSelectionModeOnClick(self):
        if self.listbox['selectmode'] == 'browse':
            self.listbox['selectmode'] = 'multiple'
            self.btn_selection_mode["image"] = self.img_multiple_selection
        else:
            self.listbox['selectmode'] = 'browse'
            self.btn_selection_mode["image"] = self.img_single_selection

    def set_subfoldermode(self):
        self.flg_subfoldermode = not self.flg_subfoldermode

    def open_onclick(self):
        self.open_option_from_list()

    def uplevel_onclick(self):
        if self.active_file:
            self.active_file = None
            self.list_title["text"] = "List of files:"
            self.subfolder_mode["state"] = Tkinter.NORMAL
            self.setlistbox()
        else:
            self.cdr = os.path.split(self.cdr)[0]
            self.setlistbox()

    def listboxOnClick(self, event):
        self.listbox.select_clear(0, 0)
        self.selected_item = self.listbox.nearest(event.y)

    def listboxOnDoubleClick(self, event):
        self.open_option_from_list(self.listbox.nearest(event.y))

    def menu_file_openWorkSpace(self):
        fname = tkFileDialog.askopenfilename(filetypes=[("Workspace files", "*.wsp")])
        if fname:
            self.open_workspace(fname, "workspace")

    def menu_file_openDataSet(self):
        fname = tkFileDialog.askopenfilename(filetypes=[("Dataset files", "*.wtw")])
        if fname:
            self.open_workspace(fname, "tree")

    def menu_file_openProjection(self):
        fname = tkFileDialog.askopenfilename(filetypes=[("Projection files", "*.dvw")])
        if fname:
            self.open_workspace(fname, "projection")

def menu_file_openClusterTree(self):
    fname = tkFileDialog.askopenfilename(filetypes=[("Cluster tree files", "*.clu")])
    if fname:
        self.open_workspace(fname, "cluster")

def menu_file_openReport(self):
    fname = tkFileDialog.askopenfilename(filetypes=[("Identification report files", "*.rep")])
    if fname:
        self.open_workspace(fname, "report")

def menu_file_openPhylogeneticTree(self):
    pass

def menu_file_openTextFile(self):
    fname = tkFileDialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

def menu_file_convertToFASTA(self):
    source_filelist = self.getFileList()
    if not source_filelist:
        return
    while True:
        dialog = dialogs.CustomEntry(self.root, "Number of sequences per file", [["Number:", 1]])
        dialog.showGlobalModal()
        result = dialog.get()
        if not result:
            return
        try:
            seqnum = int(result)
            if seqnum <= 0:
                tools.alert("Enter a positive integer value")
                continue
            else:
                break
        except:
            tools.alert("Enter a positive integer value")
            continue
    if seqnum == 1:
        fname = tkFileDialog.askdirectory()
    else:
        fname = tkFileDialog.asksaveasfilename()
    if not fname:
        return
    self.convertToFASTA(source_filelist, seqnum, fname)

def menu_file_exit(self):
    self.exit()

def menu_command_process(self):
    workspace_id, counter = self.process(self.getFileList())
    # Show tree
    self.workspaces[workspace_id].showTree(counter)
    self.workspaces[workspace_id].setChanged()

def menu_command_straitIdentification(self):
    self.strait_identification()

def menu_command_advancedIdentification(self):
    self.advanced_identification()

def menu_database_edit(self):
    self.openDbEditor()

def menu_database_addSequences(self):
    self.add_patterns()

def menu_database_organize(self):
    self.organize()

def menu_preferences_showCurrentOptionsByDefault(self):
    strText = (f"Pattern type:\t{self.pattern_type}\n"
               f"Thresholds:\t{self.thresholds}\n"
               f"Start folder:\t{tools.basename(self.cdr)}\n"
               f"Buffer size:\t{self.buffer_size}")
    tools.message("Current set of the options by default", strText)

def menu_preferences_setPatternType(self):
    # Set pattern options
    settings = self.choosePatternType()
    if not settings:
        return
    self.setPatternType(settings)
    self.setOptionsByDefault(settings)

def menu_preferences_setStartDirectory(self):
    dirname = tkFileDialog.askdirectory()
    if not dirname:
        return
    self.cdr = dirname
    self.setlistbox()
    settings = {"source data": self.cdr}
    self.setOptionsByDefault(settings)

def menu_preferences_setBufferSize(self):
    while True:
        dialog = dialogs.CustomEntry(self.root, "Buffer size", [["Enter buffer size:", self.buffer_size]])
        dialog.showGlobalModal()
        result = dialog.get()
        if not result:
            return
        try:
            value = int(result)
            if value <= 0:
                tools.alert("Enter a positive integer")
                continue
            else:
                self.buffer_size = value
                settings = {"buffer size": value}
                self.setOptionsByDefault(settings)
                return
        except:
            tools.alert("Enter a positive integer")
            continue
    def menu_preferences_saveCurrentSettings(self):
        self.setOptionsByDefault()

    def menu_phylogeny_distanceMatrix(self):
        workspace_id, counter = self.process(self.getFileList())
        # Show distance table
        dmatrix = self.workspaces[workspace_id].getDistanceMatrix(counter)
        self.workspaces[workspace_id].showDistanceMatrix(dmatrix)

    def menu_phylogeny_neighbourJoining(self, distmatrix=None):
        workspace_id, counter = self.process(self.getFileList())
        # Show tree
        self.workspaces[workspace_id].showPhylogeneticTree("neighbour", counter)

    def menu_phylogeny_fitch(self, distmatrix=None):
        workspace_id, counter = self.process(self.getFileList())
        # Show tree
        self.workspaces[workspace_id].showPhylogeneticTree("fitch", counter)

    def menu_phylogeny_kitsch(self, distmatrix=None):
        workspace_id, counter = self.process(self.getFileList())
        # Show tree
        self.workspaces[workspace_id].showPhylogeneticTree("kitsch", counter)

    def menu_Help_show(self):
        fname = os.path.join(os.getcwd(), "lib", "doc", "index.html")
        if os.path.isfile(fname):
            os.startfile(fname)  # This works on Windows. For cross-platform, use webbrowser.open

    def menu_Help_about(self):
        tools.message("About", "MetaLingvo 1.0\n2009.07.19\n\nContact:\nDr. Oleg Reva\noleg.reva@up.ac.za")

    def menu_Help_license(self):
        pass

    def sortFiles(self, a, b):
        a_str = str(a).upper()
        b_str = str(b).upper()
        if a_str > b_str:
            return 1
        elif a_str < b_str:
            return -1
        else:
            return 0

#########################################################################################################
class WorkSpaceInterface(GUI):
    def __init__(self, parent, trigger, name="", mode="top", dataset=None):
        super().__init__(parent, trigger)  # Use super() for better readability
        self.name = name
        self.key = ""
        # GUI
        self.oViewer = None
        # data and collections
        self.oTree = None
        self.projections = {}
        self.cluster_trees = {}
        self.reports = {}
        self.comments = ""
        self.wsp_fname = None
        # modes in ("top","tree","projection","cluster","report","pattern","comments")
        self.mode = mode
        self.menuList = []
        self.options = []
        self.selected_item = ""
        self.auxiliary_elements = None

        self.statOptionsByDefault = ["Length", "PS"]
        self.cutoff = 3.14

        # FLAGS
        self.flg_showPatterns = 0
        self.flg_showProjections = 0
        self.flg_showTables = 0
        self.flg_showReports = 0

        if dataset:
            if self.mode == "tree":
                self.oTree = dataset
            elif self.mode == "projection":
                self.key = f"projection #{len(self.projections) + 1}"
                self.projections[self.key] = dataset
            elif self.mode == "cluster":
                self.key = f"projection #{len(self.cluster_trees) + 1}"
                self.cluster_trees[self.key] = dataset
            else:
                pass

        if self.root:
            self.root.title(f"Workspace {name}")
            self.buildWindow()
            self.specifyUI()
            self.reconfigure_window()
            
    def buildMenu(self):
        if self.menuList:
            if "Export clusters to" in self.menuList:
                self.menuBar.deletemenu("Export clusters to")
            for menuName in self.menuList:
                if menuName == "Export clusters to":
                    continue
                self.menuBar.deletemenu(menuName)
        
        self.menuList.clear()  # More explicit clearing of the list

        if self.mode == "top":
            self.menuBar.addmenu('File', 'File')
            self.menuList.append('File')
            self.menuBar.addmenuitem('File', 'command', 'Save workspace',
                command=self.menu_file_saveWorkspace,
                label='Save workspace...')
            self.menuBar.addmenuitem('File', 'command', 'Save new workspace',
                command=self.menu_file_saveWorkspaceAs,
                label='Save workspace as...')
            self.menuBar.addmenuitem('File', 'separator')
            self.menuBar.addmenuitem('File', 'command', 'Exit',
                command=self.menu_file_exit,
                label='Exit')

        elif self.mode == "tree":
            self.menuBar.addmenu('File', 'Working with database files')
            self.menuList.append('File')
            self.menuBar.addmenuitem('File', 'command', 'Merge files',
                command=self.menu_tree_file_merge,
                label='Merge files...')
            self.menuBar.addmenuitem('File', 'command', 'Copy files to folder',
                command=self.menu_tree_file_copy,
                label='Copy source files...')
            self.menuBar.addmenuitem('File', 'separator')
            self.menuBar.addmenuitem('File', 'command', 'Save workspace',
                command=self.menu_file_saveWorkspace,
                label='Save workspace...')
            self.menuBar.addmenuitem('File', 'command', 'Save new workspace',
                command=self.menu_file_saveWorkspaceAs,
                label='Save workspace as...')
            self.menuBar.addmenuitem('File', 'command', 'Save tree',
                command=self.menu_tree_file_saveAs,
                label='Save dataset...')
            self.menuBar.addmenuitem('File', 'command', 'Save EPS picture',
                command=self.menu_file_savePicture,
                label='Save picture...')
            self.menuBar.addmenuitem('File', 'separator')
            self.menuBar.addmenuitem('File', 'command', 'Exit the application',
                command=self.menu_file_exit,
                label='Exit')

            self.menuBar.addmenu('Command', 'Edit the tree')
            self.menuList.append('Command')
            self.menuBar.addmenuitem('Command', 'command', 'Recalculation',
                command=self.menu_tree_command_recalculate,
                label='Recalculate...')
            self.menuBar.addmenuitem('Command', 'command', 'Show multidimensional projection',
                command=self.menu_tree_command_projection,
                label='Multidimensional projection...')
            self.menuBar.addmenuitem('Command', 'command', 'Identify sequences',
                command=self.menu_tree_command_identify,
                label='Identify sequences...')

            self.menuBar.addmenu('View', 'View elements and statistics')
            self.menuList.append('View')
            self.menuBar.addmenuitem('View', 'command', 'Show outermost nodes',
                command=self.menu_tree_view_showOutermosts,
                label='Outermost elements...')
            self.menuBar.addmenuitem('View', 'command', 'Select elements by color',
                command=self.menu_tree_view_select,
                label='Select...')

            self.menuBar.addmenu('Phylogeny', 'Phylogeny')
            self.menuList.append('Phylogeny')
            self.menuBar.addmenuitem('Phylogeny', 'command', 'Distance matrix',
                command=self.menu_phylogeny_distanceMatrix,
                label='Distance matrix')

        elif self.mode == "dataset":
            self.menuBar.addmenu('File', 'Working with database files')
            self.menuList.append('File')
            self.menuBar.addmenuitem('File', 'command', 'Save workspace',
                command=self.menu_file_saveWorkspace,
                label='Save workspace...')
            self.menuBar.addmenuitem('File', 'command', 'Save new workspace',
                command=self.menu_file_saveWorkspaceAs,
                label='Save workspace as...')
            self.menuBar.addmenuitem('File', 'command', 'Save EPS picture',
                command=self.menu_file_savePicture,
                label='Save picture...')
            self.menuBar.addmenuitem('File', 'separator')
            self.menuBar.addmenuitem('File', 'command', 'Exit the application',
                command=self.menu_file_exit,
                label='Exit')
            
        elif self.mode == "projection":
            self.menuBar.addmenu('File', 'Working with database files')
            self.menuList.append('File')
            self.menuBar.addmenuitem('File', 'command', 'Save workspace',
                command=self.menu_file_saveWorkspace,
                label='Save workspace...')
            self.menuBar.addmenuitem('File', 'command', 'Save new workspace',
                command=self.menu_file_saveWorkspaceAs,
                label='Save workspace as...')
            self.menuBar.addmenuitem('File', 'command', 'Save multidimensional space',
                command=self.menu_projection_file_saveAs,
                label='Save projection...')
            self.menuBar.addmenuitem('File', 'command', 'Save EPS picture',
                command=self.menu_file_savePicture,
                label='Save picture...')
            self.menuBar.addmenuitem('File', 'separator')
            self.menuBar.addmenuitem('File', 'command', 'Exit the application',
                command=self.menu_file_exit,
                label='Exit')
            
            self.menuBar.addmenu('Command', 'Working with database files')
            self.menuList.append('Command')
            self.menuBar.addmenuitem('Command', 'command', 'Recalculate workspace',
                command=self.menu_projection_command_recalculate,
                label='Recalculate...')
            self.menuBar.addmenuitem('Command', 'command', 'Identify sequences',
                command=self.menu_projection_command_identify,
                label='Identify sequences...')
            self.menuBar.addmenuitem('Command', 'command', 'Export tree',
                command=self.menu_projection_command_exportTree,
                label='Generate cluster tree...')

            self.menuBar.addmenu('Edit', 'Change multidimensional space')
            self.menuList.append('Edit')
            self.menuBar.addmenuitem('Edit', 'command', 'Set number of dimensions',
                command=self.menu_projection_edit_setDimensions,
                label='Set dimensions...')
            self.menuBar.addmenuitem('Edit', 'command', 'Patterns set',
                command=self.menu_projection_edit_setOutgroups,
                label='Set outgroups...')
            self.menuBar.addmenuitem('Edit', 'command', 'Set of geometry attributes',
                command=self.menu_projection_edit_setGeometry,
                label='Set geometry...')
            self.menuBar.addmenuitem('Edit', 'command', 'Set reference patterns',
                command=self.menu_projection_edit_setReferences,
                label='Set references...')
            self.menuBar.addmenuitem('Edit', 'separator')
            self.menuBar.addmenuitem('Edit', 'command', 'Delete patterns',
                command=self.menu_projection_edit_deletePatterns,
                label='Delete patterns...')

            self.menuBar.addmenu('View', 'Control windows to change Multi-D view or export data')
            self.menuList.append('View')
            self.menuBar.addmenuitem('View', 'command', 'Select elements',
                command=self.menu_projection_view_select,
                label='Select...')
            self.menuBar.addmenuitem('View', 'command', 'Unselect elements',
                command=self.menu_projection_view_unselect,
                label='Unselect all')
            self.menuBar.addmenuitem('View', 'separator')
            self.menuBar.addmenuitem('View', 'command', 'Export table as a text',
                command=self.menu_projection_view_exportTable,
                label='Export table...')
            self.menuBar.addmenuitem('View', 'command', 'Export coordinates as a text',
                command=self.menu_projection_view_exportCoordinates,
                label='Export coordinates...')

            self.menuBar.addmenu('Phylogeny', 'Phylogeny')
            self.menuList.append('Phylogeny')
            self.menuBar.addmenuitem('Phylogeny', 'command', 'Distance matrix',
                command=self.menu_phylogeny_distanceMatrix,
                label='Distance matrix')
            
        elif self.mode == "cluster":
            self.menuBar.addmenu('File', 'Working with database files')
            self.menuList.append('File')
            self.menuBar.addmenuitem('File', 'command', 'Save workspace',
                command=self.menu_file_saveWorkspace,
                label='Save workspace...')
            self.menuBar.addmenuitem('File', 'command', 'Save new workspace',
                command=self.menu_file_saveWorkspaceAs,
                label='Save workspace as...')
            self.menuBar.addmenuitem('File', 'command', 'Save binary file',
                command=self.menu_cluster_file_saveAs,
                label='Save cluster tree...')
            self.menuBar.addmenuitem('File', 'command', 'Save EPS picture',
                command=self.menu_file_savePicture,
                label='Save picture...')
            self.menuBar.addmenuitem('File', 'separator')
            self.menuBar.addcascademenu('File', 'Export clusters to', 
                'Export cluster sequences', 
                traverseSpec='z', tearoff=1)
            menuCommands = [["FASTA", self.menu_cluster_file_exportToFASTA],
                            ["GBK", self.menu_cluster_file_exportToGBK],
                            ["Gbff", self.menu_cluster_file_exportToGbff],
                            ]
            for menuoption in menuCommands:
                self.menuBar.addmenuitem('Export clusters to', 'command', 'Export clusters to ' + menuoption[0],
                command=menuoption[1],
                label=menuoption[0])
            self.menuList.append('Export clusters to')
            self.menuBar.addmenuitem('File', 'command', 'Show list of endnode elements',
                command=self.menu_cluster_file_showLeafList,
                label='Show end-node elements...')
            self.menuBar.addmenuitem('File', 'command', 'Convert to text',
                command=self.menu_cluster_file_toString,
                label='Convert to text...')
            self.menuBar.addmenuitem('File', 'separator')
            self.menuBar.addmenuitem('File', 'command', 'Exit the application',
                command=self.menu_file_exit,
                label='Exit')

            self.menuBar.addmenu('Command', 'Edit functions')
            self.menuList.append('Command')    
            self.menuBar.addmenuitem('Command', 'command', 'Recalculate',
                command = self.menu_cluster_command_recalculate,
                label = 'Recalculate...')
            self.menuBar.addmenuitem('Command', 'command', 'Identify sequences',
                command = self.menu_cluster_command_identify,
                label = 'Identify sequences...')
            self.menuBar.addmenuitem('Command', 'command', 'Identify clusters',
                command = self.menu_cluster_command_identify_clusters,
                label = 'Identify clusters...')
                
            self.menuBar.addmenu('Edit', 'Edit tables')
            self.menuList.append('Edit')    
            self.menuBar.addmenuitem('Edit', 'command', 'Hide and delete reference patterns',
                command = self.menu_cluster_edit_setReferences,
                label = 'Set references...')
            self.menuBar.addmenuitem('Edit', 'command', 'Edit table',
                command = self.menu_cluster_edit_hide_rename,
                label = 'Hide/Rename...')
            self.menuBar.addmenuitem('Edit', 'separator')
            self.menuBar.addmenuitem('Edit', 'command', 'Rearrange the clusters',
                command = self.menu_cluster_edit_rearrange,
                label = 'Rearrange nodes...')
     
            self.menuBar.addmenuitem('Edit', 'command', 'Delete',
                command = self.menu_cluster_edit_delete,
                label = 'Delete clusters or nodes...')

            self.menuBar.addmenu('View', 'Different helpful statistics')
            self.menuList.append('View')    
            self.menuBar.addmenuitem('View', 'command', 'Hide outliers',
                command = self.menu_cluster_view_hideOutliers,
                label = 'Hide outliers')
            self.menuBar.addmenuitem('View', 'command', 'Restore hidden outliers',
                command = self.menu_cluster_view_showOutliers,
                label = 'Show outliers')
            self.menuBar.addmenuitem('View', 'command', 'Restore and show all elements',
                command = self.menu_cluster_view_showAll,
                label = 'Show all')
            self.menuBar.addmenuitem('View', 'separator')
            self.menuBar.addmenuitem('View', 'command', 'Select elements',
                command = self.menu_cluster_view_select,
                label = 'Select...')
            self.menuBar.addmenuitem('View', 'command', 'Unselect elements',
                command = self.menu_cluster_view_unselect,
                label = 'Unselect all')

            self.menuBar.addmenu('Phylogeny', 'Phylogeny')
            self.menuList.append('Phylogeny')
            self.menuBar.addmenuitem('Phylogeny', 'command', 'Distance matrix',
                command = self.menu_phylogeny_distanceMatrix,
                label = 'Pattern distance matrix')
            self.menuBar.addmenuitem('Phylogeny', 'command', 'Distance matrix',
                command = self.menu_cluster_phylogeny_clusterDistanceMatrix,
                label = 'Cluster distance matrix')
            
        elif self.mode == "pattern":
            self.menuBar.addmenu('File', 'File')
            self.menuList.append('File')
            self.menuBar.addmenuitem('File', 'command', 'Save workspace',
                command = self.menu_file_saveWorkspace,
                label = 'Save workspace...')
            self.menuBar.addmenuitem('File', 'command', 'Save new workspace',
                command = self.menu_file_saveWorkspaceAs,
                label = 'Save workspace as...')
            self.menuBar.addmenuitem('File', 'command', 'Save EPS picture',
                command = self.menu_file_savePicture,
                label = 'Save picture...')
            self.menuBar.addmenuitem('File', 'command', 'Export pattern as text',
                command = self.menu_pattern_file_export,
                label = 'Export...')
            self.menuBar.addmenuitem('File', 'separator') 
            self.menuBar.addmenuitem('File', 'command', 'Exit',
                command = self.menu_file_exit,
                label = 'Exit')
            
        elif self.mode == "report":
            self.menuBar.addmenu('File', 'File')
            self.menuList.append('File')
            self.menuBar.addmenuitem('File', 'command', 'Save workspace',
                command = self.menu_file_saveWorkspace,
                label = 'Save workspace...')
            self.menuBar.addmenuitem('File', 'command', 'Save new workspace',
                command = self.menu_file_saveWorkspaceAs,
                label = 'Save workspace as...')
            self.menuBar.addmenuitem('File', 'command', 'Save report',
                command = self.menu_report_file_saveReport,
                label = 'Save report...')
            self.menuBar.addmenuitem('File', 'command', 'Export report to text',
                command = self.menu_report_file_export,
                label = 'Export text...')
            self.menuBar.addmenuitem('File', 'separator') 
            self.menuBar.addmenuitem('File', 'command', 'Exit',
                command = self.menu_file_exit,
                label = 'Exit')
        else:
            pass
        
        # Add database menu
        self.menuBar.addmenu('Database', 'Identification of patterns')
        self.menuList.append('Database')
        self.menuBar.addmenuitem('Database', 'command', 'Edit identification table',
            command = self.menu_database_editTable,
            label = 'Edit database...')
        if self.mode =="cluster":
            self.menuBar.addmenuitem('Database', 'command', 'Add new identification table',
                command = self.menu_cluster_database_new,
                label = 'Import to database...')
            self.menuBar.addmenuitem('Database', 'command', 'Add clusters to the identification tables',
                command = self.menu_cluster_database_addClusters,
                label = 'Add clusters...')
        if self.mode not in ("top","dataset","report"):
            self.menuBar.addmenuitem('Database', 'command', 'Add sequences to the identification tables',
                command = self.menu_database_addPatterns,
                label = 'Add sequences...')

        # Add help menu
        self.menuBar.addmenu('?', 'Help')
        self.menuList.append('?')
        self.menuBar.addmenuitem('?', 'command', 'Help',
            command = self.menu_help_get,
            label = 'Help...')
        self.menuBar.addmenuitem('?', 'command', 'Help',
            command = self.menu_help_about,
            label = 'About...')
        self.menuBar.addmenuitem('?', 'command', 'Help',
            command = self.menu_help_license,
            label = 'License agreement...')

            
    def specifyUI(self):
        self.balloon_x = Pmw.Balloon(self.root)
        # Add buttons
        imagepath = "images"
        try:
            self.img_open = Tkinter.PhotoImage(file=os.path.join(imagepath,"open.gif"))
            self.img_delete = Tkinter.PhotoImage(file=os.path.join(imagepath,"delete.gif"))
            self.img_edit = Tkinter.PhotoImage(file=os.path.join(imagepath,"edit.gif"))
            self.img_save = Tkinter.PhotoImage(file=os.path.join(imagepath,"save.gif"))
        except:
            imagepath = os.path.join("lib","images")
            self.img_open = Tkinter.PhotoImage(file=os.path.join(imagepath,"open.gif"))
            self.img_delete = Tkinter.PhotoImage(file=os.path.join(imagepath,"delete.gif"))
            self.img_edit = Tkinter.PhotoImage(file=os.path.join(imagepath,"edit.gif"))
            self.img_save = Tkinter.PhotoImage(file=os.path.join(imagepath,"save.gif"))
        # button 'Open'
        btn_open = Tkinter.Button(self.frame_buttons, image=self.img_open, command=self.btn_open_onclick)
        btn_open.pack(side=Tkinter.LEFT)
        self.balloon_x.bind(btn_open,"Open")
        # button 'Edit'
        self.btn_edit = Tkinter.Button(self.frame_buttons, image=self.img_edit, command=self.btn_rename_onclick)
        self.btn_edit.pack(side=Tkinter.LEFT)
        self.balloon_x.bind(self.btn_edit,"Rename")
        # button 'Delete'
        self.btn_delete = Tkinter.Button(self.frame_buttons, image=self.img_delete, command=self.btn_delete_onclick)
        self.btn_delete.pack(side=Tkinter.LEFT)
        self.balloon_x.bind(self.btn_delete,"Delete")
        # button 'Save'
        btn_save = Tkinter.Button(self.frame_buttons, image=self.img_save, command=self.btn_saveworkspace_onclick)
        btn_save.pack(side=Tkinter.LEFT)
        self.balloon_x.bind(btn_save,"Save")
        
        #self.listbox['width'] = 50
        self.listbox['selectmode'] = 'single'
        
    def reconfigure_window(self):
        if not self.root:
            self.buildRightPanel()
            return
        self.buildMenu()
        result = self.buildRightPanel()
        if not result:
            return
        if self.command_buttons:
            self.command_buttons.destroy()
        if self.mode in ("top","tree"):
            #self.btn_upLevel['state'] = Tkinter.DISABLED
            self.list_title['text'] = "Items to show:"
        else:
            pass
            #self.btn_upLevel['state'] = Tkinter.ACTIVE
        # Add command buttons
        self.command_buttons = Tkinter.Frame(self.frame_commands)
        self.command_buttons.pack(side=Tkinter.TOP,expand=0,fill=Tkinter.X)
        if self.mode == "top":
            btn1 = Tkinter.Button(self.command_buttons,text="Save workspace",command=self.btn_saveworkspace_onclick)
            btn1.pack(side=Tkinter.LEFT, padx=2)
        if self.mode == "tree":
            '''
            btn1 = Tkinter.Button(self.command_buttons,text="Recalculate",command=self.btn_tree_recalculate_onclick)
            btn1.pack(side=Tkinter.LEFT, padx=2)
            '''
            btn2 = Tkinter.Button(self.command_buttons,text="Multi-D",command=self.btn_tree_projection_onclick)
            btn2.pack(side=Tkinter.LEFT, padx=2)
            viewerType = Pmw.RadioSelect(self.command_buttons,
                        buttontype = 'radiobutton',
                        orient = 'horizontal',
                        labelpos = 'w',
                        command = self.viewertype_onselect,
                        label_text = 'Viewer:',
                        hull_borderwidth = 0,
                        hull_relief = None,
                        selectmode = 'single',
                )
            viewerType.pack(side=Tkinter.LEFT, padx=2)
            # Add some buttons to the RadioSelect.
            for text in ("Tree","Stat"):
                viewerType.add(text)
            viewerType.setvalue("Tree")
        elif self.mode == "dataset":
            btn1 = Tkinter.Button(self.command_buttons,text="Save picture",command=self.btn_savepicture_onclick)
            btn1.pack(side=Tkinter.LEFT, padx=2)
            viewerType = Pmw.RadioSelect(self.command_buttons,
                        buttontype = 'radiobutton',
                        orient = 'horizontal',
                        labelpos = 'w',
                        command = self.viewertype_onselect,
                        label_text = 'Viewer:',
                        hull_borderwidth = 0,
                        hull_relief = None,
                        selectmode = 'single',
                )
            viewerType.pack(side=Tkinter.LEFT, padx=2)
            # Add some buttons to the RadioSelect.
            for text in ("Tree","Stat"):
                viewerType.add(text)
            viewerType.setvalue("Stat")
        elif self.mode == "projection":
            btn1 = Tkinter.Button(self.command_buttons,text="Generate cluster tree",command=self.btn_projection_generatetree_onclick)
            btn1.pack(side=Tkinter.LEFT, padx=2)
        elif self.mode == "cluster":
            btn1 = Tkinter.Button(self.command_buttons,text="Import to database",command=self.btn_importTable_onclick)
            btn1.pack(side=Tkinter.LEFT, padx=2)
            btn2 = Tkinter.Button(self.command_buttons,text="Identify clusters",command=self.btn_identify_clusters_onclick)
            btn2.pack(side=Tkinter.LEFT, padx=2)
        elif self.mode == "report":
            pass
        elif self.mode == "pattern":
            btn1 = Tkinter.Button(self.command_buttons,text="Export",command=self.btn_export_pattern_onclick)
            btn1.pack(side=Tkinter.LEFT, padx=2)
        else:
            pass
        self.setlistbox()
        
    def buildRightPanel(self):
        if self.root:
            if self.frame_right:
                self.frame_right.destroy()
            self.frame_right = Tkinter.Frame(self.frame_mainWindow,bd=2,relief=Tkinter.SUNKEN)
            self.frame_right.pack(side=Tkinter.RIGHT, expand=1, fill=Tkinter.BOTH)
        else:
            self.frame_right = None
        if self.mode == "tree" and self.oTree:
            self.oViewer = reports.TreeViewer(self.frame_right,self.do)
            self.oViewer.setTreeObject(self.oTree,self.trigger("Get pattern type"))
            if self.root:
                self.oViewer.showTree()
        elif self.mode == "dataset" and self.oTree:
            oInfo = self.trigger("Get sequence location info")
            self.oViewer = reports.StatViewer(self.frame_right,self.do,oInfo,self.balloon)
            self.oViewer.setComboBoxs(self.statOptionsByDefault)
            self.oViewer.draw()
        elif self.mode == "projection":
            if type(self.projections[self.key]) == type({}):
                oProjection = reports.TView()
                oProjection.setRoot(self.frame_right,self.do,self.balloon)
                oProjection.set_data(self.projections[self.key])
                self.projections[self.key] = oProjection
            else:
                self.projections[self.key].setRoot(self.frame_right,self.do,self.balloon)
            dNum = self.projections[self.key].getDimNumber()
            if dNum == 1:
                dNum = 0
            self.oViewer = self.projections[self.key].showProjection(dNum)
            if self.auxiliary_elements:
                for pattern in self.auxiliary_elements:
                    oPattern = self.trigger("Get pattern",[pattern])
                    self.projections[self.key].addPattern(pattern,oPattern)
                self.auxiliary_elements = None
        elif self.mode == "cluster" and self.cluster_trees[self.key]:
            self.oViewer = reports.ClusterViewer(self.frame_right,str(self.key),self.do,self.balloon)
            self.oViewer.setGroups(self.cluster_trees[self.key].getGroups())
            self.oViewer.showTree(self.cluster_trees[self.key])
        elif self.mode == "report" and self.reports[self.key]:
            self.oViewer = reports.ReportPanel(self.frame_right,self.do,self.balloon,self.key)
            self.oViewer.print_report(self.reports[self.key])
        elif self.mode == "pattern" and self.oTree:
            self.oViewer = reports.ColorPad(self.frame_right,self.do,self.balloon,self.key)
            self.oViewer.plotData(self.trigger('Get pattern',[self.key]))
        else:
            pass
        return 1
            
    def reset(self):
        self.oViewer = None
        self.key = ""
        self.mode = "top"
        
    def setlistbox(self):
        if not self.root:
            return
        self.listbox.delete(0,Tkinter.END)
        self.options = []
        if self.oTree:
            self.listbox.insert(Tkinter.END,"Dataset")
            self.options.append("Dataset")
        if self.projections:
            self.listbox.insert(Tkinter.END,"MULTI-D PROJECTIONS")
            self.options.append("MULTI-D PROJECTIONS")
            if self.flg_showProjections:
                for item in self.projections:
                    item = " ..." + item
                    self.listbox.insert(Tkinter.END,item)
                    self.options.append(item)
        if self.cluster_trees:
            self.listbox.insert(Tkinter.END,"CLUSTERS")
            self.options.append("CLUSTER TREES")
            if self.flg_showTables:
                for item in self.cluster_trees:
                    item = " ..." + item
                    self.listbox.insert(Tkinter.END,item)
                    self.options.append(item)
        if self.reports:
            self.listbox.insert(Tkinter.END,"REPORTS")
            self.options.append("REPORTS")
            if self.flg_showReports:
                for item in self.reports:
                    item = " ..." + item
                    self.listbox.insert(Tkinter.END,item)
                    self.options.append(item)
        if self.oTree:
            self.listbox.insert(Tkinter.END,"PATTERNS")
            self.options.append("PATTERNS")
            if self.flg_showPatterns:
                for item in self.oTree.getLeaves():
                    item = " ..." + item
                    self.listbox.insert(Tkinter.END,item)
                    self.options.append(item)
        
    # METHODS
    
    def do(self,option,ArgList=None):
        if option == "Update pages":
            if self.oViewer.getActivePage() == ArgList:
                print ("OK")
                return
        elif option == "Rename patterns":
            self.rename_patterns(ArgList)
        elif option == "Remove page":
            self.reset()
            self.reconfigure_window()
        elif option == "Set stat options":
            self.statOptionsByDefault = []
            self.statOptionsByDefault.extend(ArgList)
        elif option == "Print report":
            self.print_report(ArgList)
        elif option == "Reconfigure window":
            self.reconfigure_window()
        elif option == "Update window":
            self.reconfigure_window()
            self.setChanged()
        elif option == "Set changed":
            self.setChanged(ArgList)
        elif option == "Set cutoff" and self.key in self.cluster_trees:
            self.cluster_trees[self.key].setCutoff(ArgList)
        elif option == "Delete nodes":
            for node in ArgList:
                self.rearrange_node(node)
        elif option == "Rearange nodes":
            self.rearrange_nodes(ArgList)
        elif option == "Get available patterns":
            if self.oTree:
                return self.oTree.getLeaves()
            return 
        elif option == "Update report":
            for key in ArgList:
                self.reports[self.key][key] = ArgList[key]
            self.setChanged()
        else:
            return self.trigger(option,ArgList)
        
    def set_data(self,oTree):
        self.oTree = oTree
        self.mode = "tree"
        self.reconfigure_window()
        
    def open_option_from_list(self,option):
        if option == "Dataset" and self.mode != "tree":
            self.mode = "tree"
            self.reconfigure_window()
        elif option == "PATTERNS":
            self.flg_showPatterns = abs(self.flg_showPatterns-1)
        elif option == "MULTI-D PROJECTIONS":
            self.flg_showProjections = abs(self.flg_showProjections-1)
        elif option == "CLUSTER TREES":
            self.flg_showTables = abs(self.flg_showTables-1)
        elif option == "REPORTS":
            self.flg_showReports = abs(self.flg_showReports-1)
        elif option[:4] == " ...":
            self.open_second_level_option(option)
        else:
            pass
        self.setlistbox()
        self.select(option)
        
    def open_second_level_option(self,option):
        opt_ind = self.options.index(option)
        self.set_mode(opt_ind)
        self.key = option[4:]
        self.reconfigure_window()
    
       # modes in ("top","tree","projection","cluster","report","pattern")
    def set_mode(self, ind):
        if "PATTERNS" in self.options and ind > self.options.index("PATTERNS"):
            self.mode = "pattern"
        elif "REPORTS" in self.options and ind > self.options.index("REPORTS"):
            self.mode = "report"
        elif "CLUSTER TREES" in self.options and ind > self.options.index("CLUSTER TREES"):
            self.mode = "cluster"
        elif "MULTI-D PROJECTIONS" in self.options and ind > self.options.index("MULTI-D PROJECTIONS"):
            self.mode = "projection"
        else:
            tools.alert("Error setting the dataset mode!")
            
    def set_selected_item(self,item):
        if not self.root:
            return
        if item in ("REPORTS","CLUSTER TREES","MULTI-D PROJECTIONS"):
            self.btn_delete['state'] = Tkinter.ACTIVE
            self.btn_edit['state'] = Tkinter.DISABLED
            self.selected_item = "top:" + item
            return
        if item in ("Dataset","PATTERNS"):
            self.btn_delete['state'] = Tkinter.DISABLED
            self.btn_edit['state'] = Tkinter.DISABLED
            self.selected_item = ""
            return
        if item not in self.options:
            item = " ..."+item
        if item not in self.options:
            tools.alert("Wrong item " + item)
            return
        ind = self.options.index(item)
        if "PATTERNS" in self.options and ind > self.options.index("PATTERNS"):
            self.btn_delete['state'] = Tkinter.DISABLED
            self.btn_edit['state'] = Tkinter.ACTIVE
            self.selected_item = "pattern:" + item[4:]
        elif "REPORTS" in self.options and ind > self.options.index("REPORTS"):
            self.btn_delete['state'] = Tkinter.ACTIVE
            self.btn_edit['state'] = Tkinter.ACTIVE
            self.selected_item = "report:" + item[4:]
        elif "CLUSTER TREES" in self.options and ind > self.options.index("CLUSTER TREES"):
            self.btn_delete['state'] = Tkinter.ACTIVE
            self.btn_edit['state'] = Tkinter.ACTIVE
            self.selected_item = "cluster:" + item[4:]
        elif "MULTI-D PROJECTIONS" in self.options and ind > self.options.index("MULTI-D PROJECTIONS"):
            self.btn_delete['state'] = Tkinter.ACTIVE
            self.btn_edit['state'] = Tkinter.ACTIVE
            self.selected_item = "projection:" + item[4:]
        else:
            pass

    def select(self,option):
        if not self.root:
            return
        self.listbox.selection_clear(0,Tkinter.END)
        if option == "KEY":
            self.listbox.select_set(self.options.index(" ..." + self.key))
        elif option in self.options:
            self.listbox.select_set(self.options.index(option))
        else:
            pass
            
    def select_patterns(self):
        return self.oViewer.getElements()
            
    def recalculate_dataset(self):
        if not self.oViewer:
            return
        elements = self.oViewer.getElements()
        if not elements:
            return
        self.trigger("Recalculate",elements)
        
    def show_projection(self):
        if not self.oViewer or not self.oTree:
            return
        references = self.oTree.getListOfOutermosts(self.oViewer.getThreshold())
        result = self.oViewer.getProjection(self.do,references)
        if not result:
            return
        oProjection,self.auxiliary_elements = result
        if not oProjection:
            return
        self.mode = "projection"
        self.key = "MDP #" + str(len(self.projections)+1)
        #self.projections[self.key] = oProjection.getDataSet()
        self.projections[self.key] = oProjection
        self.reconfigure_window()
        self.flg_showProjections = 0
        self.open_option_from_list("MULTI-D PROJECTIONS")
        self.select("KEY")
        self.set_selected_item(self.key)
        self.setChanged()
        
    def open_projection(self,DataSet):
        self.mode = "projection"
        self.key = "MDP #" + str(len(self.projections)+1)
        self.projections[self.key] = DataSet
        # Plot data
        self.reconfigure_window()
        self.flg_showProjections = 0
        self.open_option_from_list("MULTI-D PROJECTIONS")
        self.select("KEY")
        self.set_selected_item(self.key)
        
    def open_clusterTree(self,oTable):
        self.mode = "cluster"
        self.key = "CLT #" + str(len(self.cluster_trees)+1)
        self.cluster_trees[self.key] = oTable
        # Plot data
        self.reconfigure_window()
        self.flg_showTables = 0
        self.open_option_from_list("CLUSTER TREES")
        self.select("KEY")
        self.set_selected_item(self.key)
        
    def open_report(self,report):
        self.mode = "report"
        self.key = "Rep #" + str(len(self.reports)+1)
        self.reports[self.key] = report
        # Plot data
        self.reconfigure_window()
        self.flg_showReports = 0
        self.open_option_from_list("REPORTS")
        self.select("KEY")
        self.set_selected_item(self.key)
                
    def generate_clustertree(self):
        if not self.projections[self.key]:
            return
        if self.root:
            self.projections[self.key].selectTable('Generate tree')
            oClusterTree = self.projections[self.key].getClusterTree()
        else:
            ArgList = ["Hierarchical","",[60,50,30,40],"Generate tree"]
            oClusterTree = self.projections[self.key].generateTree(ArgList)
        
        if not oClusterTree:
            return
        tree_name = self.key + ": CLT #" + str(len(self.cluster_trees)+1)
        self.projections[self.key].addChildTree(tree_name)
        self.key = tree_name
        self.mode = "cluster"
        self.cluster_trees[self.key] = oClusterTree
        self.reconfigure_window()
        self.flg_showTables = 0
        self.open_option_from_list("CLUSTER TREES")
        self.select("KEY")
        self.set_selected_item(self.key)
        self.setChanged()
            
    def print_report(self,report,parent_element=""):
        if not report:
            return
        if parent_element:
            parent_element += ": "
        report_key = parent_element + "Rep #" + str(len(self.reports)+1)
        if self.mode == "cluster":
            self.cluster_trees[self.key].addChildReport(report_key)
        self.key = report_key
        self.reports[self.key] = report
        self.mode = "report"
        self.reconfigure_window()
        self.flg_showReports = 0
        self.open_option_from_list("REPORTS")
        self.select("KEY")
        self.set_selected_item(self.key)
        self.setChanged()
        
    def setWorkSpace(self,WSP,fname=""):
        # data and collections
        self.oTree = None
        self.projections = {}
        self.cluster_trees = {}
        self.reports = {}
        self.reports.update(WSP["reports"])
        self.comments = {}
        self.comments.update(WSP["comments"])
        self.projections.update(WSP["projections"])
        for key in WSP["cluster trees"]:
            self.cluster_trees[key] = nodes.MultidimensionalTable(WSP["cluster trees"][key]["Name"],self.do)
            self.cluster_trees[key].loadTable(WSP["cluster trees"][key])
        if WSP["dataset"]:
            oTree = nodes.Node(0,self.do)
            oTree.importTree(WSP["dataset"])
            self.set_data(oTree)
        self.wsp_fname = fname
        
    def save_workspace(self,fname):
        WSP = {"dataset":{},
                "projections":{},
                "cluster trees":{},
                "reports":{},
                "patterns":{},
                "info":self.trigger("Get sequence location info"),
                "pattern type":self.trigger("Get pattern type"),
                "comments":self.comments}
        WSP["dataset"].update(self.oTree.valueOf())
        for key in self.projections:
            if type(self.projections[key]) == type({}):
                WSP["projections"][key] = {}
                WSP["projections"][key].update(self.projections[key])
            else:
                WSP["projections"][key] = self.projections[key].getDataSet()
        #WSP["cluster trees"].update(self.cluster_trees)
        for key in self.cluster_trees:
            WSP["cluster trees"][key] = {}
            WSP["cluster trees"][key].update(self.cluster_trees[key].getTableDictionary())
        WSP["reports"].update(self.reports)
        if self.oTree:
            counter = 0
            for seqname in self.oTree.getLeaves():
                key = counter/500 + 1
                #seqname,pattern_type,fname,sequence,oPattern
                if key not in WSP["patterns"]:
                    WSP["patterns"][key] = {}
                WSP["patterns"][key][seqname] = self.trigger("Get pattern",[seqname,WSP["pattern type"],WSP["info"][seqname]["path"],"",None])
                WSP["info"][seqname]["index"] = key
                counter += 1
        tools.saveDBFile(WSP,fname)
        self.setChanged(0)
        self.wsp_fname = fname
        self.name = fname
        self.root.title("Workspace " + tools.basename(fname))
                
    def save_dataset(self,fname):
        self.oViewer.saveTable(fname)
        
    def save_projection(self,fname):
        self.projections[self.key].saveFile(fname,self.trigger("Get sequence location info"))
        self.oViewer.setFileName(fname)
        
    def save_clusterTree(self,fname):
        self.oViewer.setFileName(fname)
        SupplementaryMaterials = {"Info":self.trigger("Get sequence location info"),"Group":None}
        tools.saveDBFile(self.cluster_trees[self.key].getTableDictionary(),fname,SupplementaryMaterials)
        self.oViewer.setFileName(fname)
        
    def save_report(self,fname):
        tools.saveDBFile(self.reports[self.key],fname)
        
    def rename_patterns(self,patternsToRename):
        for item in patternsToRename:
            oldname,newname = item
            self.rename_pattern(oldname,newname,0)
        self.reconfigure_window()
            
    def rename_pattern(self,oldname,newname,flg_reconfigure=1):
        result = self.trigger("Rename pattern",[oldname,newname])
        if not result:
            return result
        if self.key == oldname:
            self.key = newname
        if self.oTree:
            self.oTree.rename_pattern(oldname,newname)
        if self.projections:
            for key in self.projections:
                try:
                    self.projections[key].rename_pattern(oldname,newname)
                except:
                    for itemname in ('Pattern list',
                            'Pattern type',
                            'Main patterns',
                            'Outermosts',
                            'Hidden patterns'):
                        if oldname in self.projections[key][itemname]:
                            i = self.projections[key][itemname].index(oldname)
                            self.projections[key][itemname][i] = newname
                    if oldname in self.projections[key]['References']:
                        self.projections[key]['References'][newname] = self.projections[key]['References'][oldname].copy()
                        del self.projections[key]['References'][oldname]
                    for item in self.projections[key]['Distance matrix']:
                        while oldname in item:
                            i = item.index(oldname)
                            item[i] = newname

        if self.cluster_trees:
            for key in self.cluster_trees:
                self.cluster_trees[key].rename_pattern("Leaf elements",oldname,newname)
        if self.reports:
            for key in self.reports:
                self.reports[key].rename_pattern(oldname,newname)
                
        self.setChanged()
        
        if flg_reconfigure:
            self.reconfigure_window()
            self.select(" ..."+newname)
    
    def rename_projection(self,oldname,newname):
        projections = self.projections.copy()
        del self.projections[oldname]
        self.projections[newname] = projections[oldname]
        del projections
        if self.key == oldname:
            self.key = newname
        try:
            child_trees = self.projections[newname].getChildTreeNames()
        except:
            child_trees = []
            child_trees.extend(self.projections[newname]['Child trees'])
        for i in range(len(child_trees)):
            pos = string.rfind(child_trees[i],":")
            new_childname = newname + ":" + child_trees[i][pos+1:]
            self.rename_clusterTree(child_trees[i],new_childname)
            if self.key == child_trees[i]:
                self.key = new_childname
            child_trees[i] = new_childname
        try:
            self.projections[newname].setChildTreeNames(child_trees)
        except:
            self.projections[newname]['Child trees'] = []
            self.projections[newname]['Child trees'].extend(child_trees)
        self.reconfigure_window()
        self.select(" ..."+newname)
        self.setChanged()
        
    def rename_clusterTree(self,oldname,newname):
        self.cluster_trees[newname] = self.cluster_trees[oldname].copy()
        del self.cluster_trees[oldname]
        child_reports = self.cluster_trees[newname].getChildReportNames()
        for i in range(len(child_reports)):
            pos = string.rfind(child_reports[i],":")
            new_childname = newname + ":" + child_reports[i][pos+1:]
            self.rename_report(child_reports[i],new_childname)
            if self.key == child_reports[i]:
                self.key = new_childname
            child_reports[i] = new_childname
        self.cluster_trees[newname].setChildReportNames(child_reports)
        self.setChanged()
        
    def rename_report(self,oldname,newname):
        self.reports[newname] = {}
        self.reports[newname].update(self.reports[oldname])
        del self.reports[oldname]
        self.setChanged()
        
    def identifyPatterns(self):
        result = self.trigger("Warn sequence length")
        if not result:
            return
        patterns = self.oViewer.getElements()
        if not patterns:
            return
        oIdentifier = auxiliaries.Identifier(self.root,self.do)
        report = oIdentifier.identify_patterns(patterns)
        if report:
            self.print_report(report)
        self.setChanged()
        
    def identifyClusters(self):
        report = self.oViewer.identifyClusters()
        if report:
            self.print_report(report,self.key)
        self.setChanged()
        
    def rearrange_nodes(self,species_list):
        print
        counter = 1
        for species in species_list:
            oPattern = self.trigger("Get pattern",[species,self.trigger("Get pattern type"),"","",None])
            if oPattern:
                oGroup = self.cluster_trees[self.key].getGroups()
                index = oGroup.getSpeciesIndex(species)
                self.rearrange_node(index,species,oPattern)
                print (str(counter)+"\t" + species + " re-added")
                counter += 1
        
    def rearrange_node(self,node_index,name="",oPattern=None):
        if self.key in self.cluster_trees:
            if oPattern:
                if node_index != None:
                    self.cluster_trees[self.key].delete_cluster(node_index)
                self.cluster_trees[self.key].AddNewPattern(name)
            elif node_index != None:
                refToDelete,RefSize = self.cluster_trees[self.key].isReference(node_index)
                if RefSize < 3:
                    tkMessageBox.showerror("Inappropriate Command!","The remained reference strains cannot be deleted!")
                    return
                self.cluster_trees[self.key].delete_cluster(node_index,refToDelete)
            self.buildRightPanel()
        
    def export_genome_fragments(self,path="example"):
        months = ("JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","NOV","DEC")
        clustSeq = self.oViewer.getClusterSequences()
        if not clustSeq:
            return
        clusters = []
        for clustername in clustSeq:
            clusters.append([len(clustSeq[clustername]['members']),clustername])
        if clusters:
            clusters.sort()
            clusters.reverse()
        counter = 1
        for item in clusters:
            n,cluster = item
            if n < 10:
                continue
            if not clustSeq[cluster]["sequence"]:
                continue
            generic_name = tools.basename(path)+str(counter)+"_("+str(n)+" fragments out of 100)"
            fname = path+"_#"+str(counter)+"_("+str(n)+").gbk"
            counter += 1
            body = "LOCUS       " + cluster
            if len(body) > 34:
                body = body[:34]
            body += " "*(34-len(body)) + str(len(clustSeq[cluster]["sequence"])) + " bp    DNA     linear   VRL "
            mytime = time.localtime()
            body += "-".join([str(mytime[2]),months[mytime[1]-1],str(mytime[0])])+"\nDEFINITION  "+generic_name+"\n"
            body += "FEATURES             Location/Qualifiers\n"
            for i in range(len(clustSeq[cluster]["members"])):
                body += "     misc_feature    " + str(clustSeq[cluster]["coordinates"][i][0]) + ".." + str(clustSeq[cluster]["coordinates"][i][1])+"\n"
                pos1 = string.find(clustSeq[cluster]["members"][i],"SOURCES=")
                pos2 = string.find(clustSeq[cluster]["members"][i],"FIRST_SOURCE=")
                body += "                     /note=\"" + clustSeq[cluster]["members"][i][:pos1] + "\n"
                body += "                     " + clustSeq[cluster]["members"][i][pos1:pos2] + "\n"
                body += "                     " + clustSeq[cluster]["members"][i][pos2:] + "\"\n"
            body += "ORIGIN      \n"
            n = math.ceil(len(clustSeq[cluster]["sequence"])/60)
            for i in range(int(n)):
                body += " "*(9-len(str(i+1))) + str(i+1)
                substring = clustSeq[cluster]["sequence"][i*60:(i+1)*60]
                for j in range(6):
                    body += " " + string.lower(substring[j*10:(j+1)*10])
                body += "\n"
            body += "//"
            f = open(fname,"w")
            f.write(body)
            f.close()


    def exportClustersToFASTA(self,clustSeq):
        #clustSeq = {leafname:{"members":[],"sequence":"","coordinates":[],"pattern":None},...}
        path = tkFileDialog.askdirectory()
        if not path:
            return
        dialog = dialogs.RadioButtonDialog(self.root,"Sequence output format",
                            ["Concatenated sequence","Multiple sequences"],{},
                            "Generic file name:",None,("OK","Cancel"),'checkbutton','multiple')
        dialog.showAppModal()
        result = dialog.get()
        if not result or len(result) < 2:
            return
        generic_name = result.pop()
        if generic_name:
            for symbol in ("\\","/",":","*","?","<",">","|"):
                generic_name = generic_name.replace(symbol,"_")
        else:
            generic_name = ""
        seq_tackling_modes = result[0]
        for cluster in clustSeq:
            if not clustSeq[cluster]["sequence"]:
                continue
            if "Concatenated sequence" in seq_tackling_modes:
                fname = generic_name+"_"+cluster+".fasta"
                fname = str.replace(fname," ","_")
                fname = os.path.join(path,fname)
                f = open(fname,"w")
                f.write(">"+generic_name+"_"+cluster+"\n"+clustSeq[cluster]["sequence"])
                f.close()
            if "Multiple sequences" in seq_tackling_modes:
                for cluster in clustSeq:
                    if not clustSeq[cluster]["sequence"]:
                        continue
                    output = []
                    for i in range(len(clustSeq[cluster]["members"])):
                        seq = clustSeq[cluster]["sequence"][clustSeq[cluster]["coordinates"][i][0]-1:clustSeq[cluster]["coordinates"][i][1]-1]
                        output.append(">"+clustSeq[cluster]["members"][i]+"\n"+seq)
                fname = generic_name+"_"+cluster+".fst"
                fname = str.replace(fname," ","_")
                fname = os.path.join(path,fname)
                f = open(fname,"w")
                f.write("\n".join(output))
                f.close()
            
    def exportClustersToGBK(self,clustSeq):
        #clustSeq = {leafname:{"members":[],"sequence":"","coordinates":[],"pattern":None},...}
        path = tkFileDialog.askdirectory()
        if not path:
            return
        dialog = dialogs.CustomEntry(self.root,"Enter generic name for the clusters?",[["Generic name",""],])
        dialog.showGlobalModal()
        generic_name = dialog.get()
        if generic_name == None:
            generic_name = ""
        months = ("JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","NOV","DEC")
        for cluster in clustSeq:
            if not clustSeq[cluster]["sequence"]:
                continue
            body = "LOCUS       " + cluster
            if len(body) > 34:
                body = body[:34]
            body += " "*(34-len(body)) + str(len(clustSeq[cluster]["sequence"])) + " bp    DNA     linear   VRL "
            mytime = time.localtime()
            body += "-".join([str(mytime[2]),months[mytime[1]-1],str(mytime[0])])+"\nDEFINITION  "+generic_name+"_"+cluster+"\n"
            body += "FEATURES             Location/Qualifiers\n"
            for i in range(len(clustSeq[cluster]["members"])):
                body += "     misc_feature    " + str(clustSeq[cluster]["coordinates"][i][0]) + ".." + str(clustSeq[cluster]["coordinates"][i][1])+"\n"
                body += "                     /note=\"" + clustSeq[cluster]["members"][i] + "\"\n"
            body += "ORIGIN      \n"
            n = math.ceil(len(clustSeq[cluster]["sequence"])/60)
            for i in range(int(n)):
                body += " "*(9-len(str(i+1))) + str(i+1)
                substring = clustSeq[cluster]["sequence"][i*60:(i+1)*60]
                for j in range(6):
                    body += " " + string.lower(substring[j*10:(j+1)*10])
                body += "\n"
            body += "//"
            fname = generic_name+"_"+cluster+".gbk"
            fname = string.replace(fname," ","_")
            fname = os.path.join(path,fname)
            f = open(fname,"w")
            f.write(body)
            f.close()
            
    def exportClustersToGbff(self,clustSeq):
        #clustSeq = {leafname:{"members":[],"sequence":"","coordinates":[],"pattern":None},...}
        path = tkFileDialog.askdirectory()
        if not path:
            return
        dialog = dialogs.CustomEntry(self.root,"Enter generic name for the clusters?",[["Generic name",""],])
        dialog.showGlobalModal()
        generic_name = dialog.get()
        if generic_name == None:
            generic_name = ""
        months = ("JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","NOV","DEC")
        for cluster in clustSeq:
            if not clustSeq[cluster]["sequence"]:
                continue
            body = "LOCUS       " + cluster
            if len(body) > 34:
                body = body[:34]
            body += " "*(34-len(body)) + str(len(clustSeq[cluster]["sequence"])) + " bp    DNA     linear   VRL "
            mytime = time.localtime()
            body += "-".join([str(mytime[2]),months[mytime[1]-1],str(mytime[0])])+"\nDEFINITION  "+generic_name+"_"+cluster+"\n"
            body += "FEATURES             Location/Qualifiers\n"
            for i in range(len(clustSeq[cluster]["members"])):
                body += "     misc_feature    1.." + str(clustSeq[cluster]["coordinates"][i][1]-clustSeq[cluster]["coordinates"][i][0])+"\n"
                body += "                     /note=\"" + clustSeq[cluster]["members"][i] + "\"\n"
                body += "ORIGIN      \n"
                seq = clustSeq[cluster]["sequence"][clustSeq[cluster]["coordinates"][i][0]-1:clustSeq[cluster]["coordinates"][i][1]-1]
                n = math.ceil(len(seq)/60)
                for i in range(int(n)):
                    body += " "*(9-len(str(i+1))) + str(i+1)
                    substring = seq[i*60:(i+1)*60]
                    for j in range(6):
                        body += " " + string.lower(substring[j*10:(j+1)*10])
                    body += "\n"
                body += "//\n"
            fname = generic_name+"_"+cluster+".gbff"
            fname = string.replace(fname," ","_")
            fname = os.path.join(path,fname)
            f = open(fname,"w")
            f.write(body[:-1])
            f.close()

    def getDistanceMatrix(self, pattern_list):
        dmatrix = {"table": {}, "members": []}
        if self.mode == "tree":
            for i in range(len(pattern_list) - 1):
                dmatrix['members'].append([pattern_list[i]])
                for j in range(i, len(pattern_list)):
                    if pattern_list[i] not in dmatrix['table']:
                        dmatrix['table'][pattern_list[i]] = {}
                    if pattern_list[j] not in dmatrix['table']:
                        dmatrix['table'][pattern_list[j]] = {}
                    dist = self.trigger("Compare patterns", [pattern_list[i], pattern_list[j]])
                    dmatrix['table'][pattern_list[i]][pattern_list[j]] = dist
                    dmatrix['table'][pattern_list[j]][pattern_list[i]] = dist
            dmatrix['members'].append([pattern_list[-1]])
            for i in range(len(pattern_list)):
                ptname = dmatrix['members'][i][0]
                sum_dist = sum(dmatrix['table'][ptname].values())
                dmatrix['members'][i].insert(0, sum_dist)
        elif self.mode == "projection":
            dmatrix = self.projections[self.key].getDistMatrix(pattern_list)
        elif self.mode == "cluster":
            dmatrix = self.cluster_trees[self.key].getDistMatrix("patterns", pattern_list)
        if dmatrix:
            dmatrix['members'].sort(reverse=True)
        return dmatrix
       
    def add_patterns(self,pattern_list):
        if not pattern_list:
            return
        oIdentifier = auxiliaries.Identifier(self.root,self.do)
        result = oIdentifier.select_tables()        
        if not result:
            return
        tables,supplementary = result
        oInfo = self.trigger("Get sequence location info")
        for names in tables:
            tbname,pattern_type = string.split(names,":")
            for seqname in pattern_list:
                print ("\tAdd sequence " + seqname)
                fname = oInfo[seqname]['path']
                oPattern = self.trigger("Get pattern",[seqname,pattern_type,fname,"",None])
                oIdentifier.add_pattern(seqname,oPattern,tbname,pattern_type,fname)
        self.trigger("Open database editor",oIdentifier.getUpdatedTables())
        del oIdentifier
        
    def setCutoff(self,val):
        self.cutoff = val

    def exit(self,event=None):
        if self.has_changed():
            self.setChanged(0)
            result = tkMessageBox.askyesno("Warning!","Do you want to save the workspace " + self.name + "?")
            if result:
                self.menu_file_saveWorkspace()
        self.root.destroy()
                    
    # EVENTS
    def listboxOnClick(self,event):
        if not self.options:
            return
        item = self.options[self.listbox.nearest(event.y)]
        self.set_selected_item(item)
        
    def btn_saveworkspace_onclick(self):
        self.menu_file_saveWorkspace()
        
    def btn_savepicture_onclick(self):
        pass
        
    def btn_tree_recalculate_onclick(self):
        self.recalculate_dataset()
        
    def btn_tree_projection_onclick(self):
        self.show_projection()
        
    def btn_projection_generatetree_onclick(self):
        self.generate_clustertree()
        
    def btn_open_onclick(self):
        ind = int(self.listbox.curselection()[0])
        self.open_option_from_list(self.options[ind])
        
    def btn_rename_onclick(self):
        pos = string.find(self.selected_item,":")
        mode = self.selected_item[:pos]
        name = self.selected_item[pos+1:]
        while 1 > 0:
            dialog = dialogs.CustomEntry(self.root,"Rename " + mode,[[mode,name],])
            dialog.showGlobalModal()
            newname = dialog.get()
            if newname == None or newname == name:
                return
            if newname == "":
                continue
            else:
                break
        if mode == "pattern":
            self.rename_pattern(name,newname)
        elif mode == "projection":
            self.rename_projection(name,newname)
        elif mode == "cluster":
            pos = str.rfind(name,":")
            projection_name = name[:pos]
            if str.find(newname,projection_name+":") != 0 and projection_name in self.projections:
                newname = projection_name + ":" + newname
            if projection_name in self.projections:
                try:
                    self.projections[projection_name].renameChildTree(name,newname)
                except:
                    self.projections[projection_name]['Child trees'].append(newname)
                    ind =  self.projections[projection_name]['Child trees'].index(name)
                    del self.projections[projection_name]['Child trees'][ind]
            self.rename_clusterTree(name,newname)
            if self.key == name:
                self.key = newname
            self.reconfigure_window()
            self.select(" ..."+newname)
        elif mode == "report":
            pos = str.rfind(name,":")
            clustertree_name = name[:pos]
            if str.find(newname,clustertree_name+":") != 0 and clustertree_name in self.cluster_trees:
                newname = clustertree_name + ": " + newname
            if clustertree_name in self.cluster_trees:
                self.cluster_trees[clustertree_name].renameChildReport(name,newname)
            self.rename_report(name,newname)
            if self.key == name:
                self.key = newname
            self.reconfigure_window()
            self.select(" ..."+newname)
        else:
            return
        self.selected_item = mode + ":" + newname
        
    def btn_delete_onclick(self):
        pos = str.find(self.selected_item,":")
        mode = self.selected_item[:pos]
        name = self.selected_item[pos+1:]
        if mode == "top":
            result = tkMessageBox.askyesno("Warning","Do you want to delete the category\n" + 
                name + " with all child elements?")
            if not result:
                return
            if name == "MULTI-D PROJECTIONS":
                self.projections = {}
                if self.mode == "projection":
                    self.reset()
            elif name == "CLUSTER TREES":
                self.cluster_trees = {}
                if self.mode == "cluster":
                    self.reset()
            elif name == "REPORTS":
                self.reports = {}
                if self.mode == "report":
                    self.reset()
        elif mode in ("projection", "cluster","report"):
            result = tkMessageBox.askyesno("Warning","Do you want to delete the " + 
                mode + " " + name + "?")
            if not result:
                return
            if mode == "projection":
                del self.projections[name]
                if self.key == name:
                    self.reset()
            elif mode == "cluster":
                del self.cluster_trees[name]
                if self.key == name:
                    self.reset()
            elif mode == "report":
                del self.reports[name]
                if self.key == name:
                    self.reset()
        else:
            pass
        self.reconfigure_window()
        self.setChanged()
        
    def btn_importTable_onclick(self):
        self.oViewer.import_table()
        
    def btn_identify_clusters_onclick(self):
        self.identifyClusters()
        
    def btn_export_pattern_onclick(self):
        report = self.oViewer.export()
        ouplib.TextEditor("Word distribution",report)

    def viewertype_onselect(self, option):
        if option == "Tree":
            self.mode = "tree"
        elif option == "Stat":
            self.mode = "dataset"
        else:
            return
        if self.oViewer:
            self.reconfigure_window()

    # Tree menu commands
    def menu_tree_file_merge(self):
        fname = tkFileDialog.askopenfilename(filetypes=[("Watchtowers' files", "*.wtw"),])
        if not fname:
            return
        self.trigger("Merge dataset file",fname)
        
    def menu_tree_file_copy(self):
        elements = self.oViewer.getElements()
        if not elements:
            return
        self.trigger("Copy",[elements,self.trigger("Get sequence location info")])
        
    def menu_tree_file_saveAs(self):
        fname = tkFileDialog.asksaveasfilename(filetypes=[("Binary files", "*.wtw")])
        if not fname:
            return
        if len(fname) < 4 or fname[-4:] != ".wtw":
            fname += ".wtw"
        self.save_dataset(fname)
        
    def menu_tree_command_recalculate(self):
        self.recalculate_dataset()
        
    def menu_tree_command_identify(self):
        self.identifyPatterns()

    def menu_tree_command_projection(self):
        self.show_projection()
        
    def menu_tree_view_showOutermosts(self):
        self.oViewer.showOutermosts()
        
    def menu_tree_view_select(self):
        self.oViewer.select()
        
    # Projection menu commands
    def menu_projection_file_save(self):
        fname = self.oViewer.getFileName()
        if not fname:
            self.menu_projection_file_saveAs()
        self.save_projection(fname)
        
    def menu_projection_file_saveAs(self):
        fname = tkFileDialog.asksaveasfilename(filetypes=[("Binary files", "*.dvw")])
        if not fname:
            return
        if len(fname) < 4 or fname[-4:] != ".dvw":
            fname += ".dvw"
        self.save_projection(fname)
        
    def menu_projection_command_exportTree(self):
        self.generate_clustertree()
        
    def menu_projection_command_identify(self):
        self.identifyPatterns()
        
    def menu_projection_command_recalculate(self):
        self.projections[self.key].recalculate()

    def menu_projection_edit_setReferences(self):
        self.projections[self.key].set_references()
        
    def menu_projection_edit_setDimentions(self):
        self.projections[self.key].set_dimention()
        self.setChanged()
        
    def menu_projection_edit_setGeometry(self):
        self.projections[self.key].set_geometry()
        self.setChanged()
        
    def menu_projection_edit_deletePatterns(self):
        self.projections[self.key].selectPatternsForDeletion()
        
    def menu_projection_edit_setOutgroups(self):
        self.projections[self.key].set_outgroups()
        self.setChanged()
        
    def menu_projection_view_select(self):
        self.projections[self.key].select()
        
    def menu_projection_view_unselect(self):
        self.projections[self.key].unselect()
        
    def menu_projection_view_exportTable(self):
        self.projections[self.key].exportTable()
        
    def menu_projection_view_exportCoordinates(self):
        self.projections[self.key].exportCoordinates()
    
    # Cluster tree menu commands
    def menu_cluster_file_save(self):
        fname = self.oViewer.getFileName()
        if not fname:
            self.menu_cluster_file_saveAs()
        else:
            self.save_clusterTree(fname)
        
    def menu_cluster_file_saveAs(self):
        fname = tkFileDialog.asksaveasfilename(filetypes=[("Binary files", "*.clu")])
        if not fname:
            return
        if len(tools.basename(fname)) <= 4 or tools.basename(fname)[-4:] != ".clu":
            fname += ".clu"
        self.save_clusterTree(fname)
        
    def menu_cluster_file_exportToFASTA(self):
        clustSeq = self.oViewer.getClusterSequences()
        if not clustSeq:
            return
        self.exportClustersToFASTA(clustSeq)
        
    def menu_cluster_file_exportToGBK(self):
        clustSeq = self.oViewer.getClusterSequences()
        if not clustSeq:
            return
        self.exportClustersToGBK(clustSeq)
        
    def menu_cluster_file_exportToGbff(self):
        clustSeq = self.oViewer.getClusterSequences()
        if not clustSeq:
            return
        self.exportClustersToGbff(clustSeq)
        
    def menu_cluster_file_showLeafList(self):
        self.oViewer.showLeafList()
        
    def menu_cluster_file_toString(self):
        if self.key in self.cluster_trees:
            self.cluster_trees[self.key].toString()
        
    def menu_cluster_command_recalculate(self):
        self.oViewer.recalculate()
        
    def menu_cluster_command_identify(self):
        self.identifyPatterns()
        
    def menu_cluster_command_identify_clusters(self):
        self.identifyClusters()
        
    def menu_cluster_edit_setReferences(self):
        self.oViewer.setReferences()
        
    def menu_cluster_edit_hide_rename(self):
        self.oViewer.hide_rename()
        
    def menu_cluster_edit_rearrange(self):
        self.oViewer.rearrange()
        
    def menu_cluster_edit_revise(self):
        self.oViewer.revise()
        
    def menu_cluster_edit_delete(self):
        self.oViewer.delete()
        
    def menu_cluster_view_hideOutliers(self):
        self.oViewer.hide_outliers()
        
    def menu_cluster_view_showOutliers(self):
        self.oViewer.show_outliers()
        
    def menu_cluster_view_showAll(self):
        self.oViewer.show_all()
        
    def menu_cluster_view_select(self):
        self.oViewer.highlight()
        
    def menu_cluster_view_unselect(self):
        self.oViewer.dim()
        
    def menu_cluster_phylogeny_clusterDistanceMatrix(self):
        clusters = self.oViewer.select_clusters()
        if clusters:
            dmatrix = self.cluster_trees[self.key].getDistMatrix("clusters",clusters.keys())
            dmatrix["replacements"] = clusters
            self.trigger("Show distance matrix",dmatrix)
        
    def menu_cluster_database_new(self):
        self.oViewer.import_table()
        
    def menu_cluster_database_addClusters(self):
        self.oViewer.addClusters()
        
    # Pattern commands
    def menu_pattern_file_export(self):
        report = self.oViewer.export()
        ouplib.TextEditor("Word distribution",report)
        
    # Report commands
    def menu_report_file_saveReport(self):
        fname = tkFileDialog.asksaveasfilename(filetypes=[("Report files", "*.rep")])
        if not fname:
            return
        if len(tools.basename(fname)) <= 4 or tools.basename(fname)[-4:] != ".rep":
            fname += ".rep"
        self.save_report(fname)
        
    def menu_report_file_export(self):
        self.oViewer.export_report(self.reports[self.key]["report"])
        
    # General menu commands    
    def menu_file_saveWorkspace(self):
        if not self.wsp_fname:
            self.menu_file_saveWorkspaceAs()
        else:
            self.save_workspace(self.wsp_fname)

    def menu_file_saveWorkspaceAs(self):
        fname = tkFileDialog.asksaveasfilename(filetypes=[("Workspase files", "*.wsp")])
        if not fname:
            return
        if len(fname) < 4 or fname[-4:] != ".wsp":
            fname += ".wsp"
        self.save_workspace(fname)
        
    def menu_file_savePicture(self):
        if not self.oViewer:
            return
        cv = self.oViewer.get_canvas()
        if not cv:
            return
        
        self.trigger("Save image",cv)
        self.reconfigure_window()

    def menu_file_exit(self):
        self.exit()
        
    def menu_phylogeny_distanceMatrix(self):
        pattern_list = self.select_patterns()
        if pattern_list:
            dmatrix = self.getDistanceMatrix(pattern_list)
            self.trigger("Show distance matrix",dmatrix)
        
    def menu_database_editTable(self):
        self.trigger("Open database editor")
        
    def menu_database_addPatterns(self):
        pattern_list = self.select_patterns()
        self.add_patterns(pattern_list)
        
    def menu_help_get(self):
        self.trigger("Help","get")
        
    def menu_help_about(self):
        self.trigger("Help","about")
        
    def menu_help_license(self):
        self.trigger("Help","license")

#########################################################################################################
class DatabaseInterface(GUI):
    def __init__(self,parent,trigger):
        GUI.__init__(self,parent,trigger)
        self.root.title("Database Editor")
        self.db = auxiliaries.Identifier(self.root,self.do)
        self.store = Store(500,self.do)
        self.oViewer = None
        self.pattern_type = ""
        self.tbname = ""
        
        # mode = "Tree" or "Associations"
        self.mode = "top"
        
        self.options = []
        self.menuList = []
        
        # FLAGS
        self.flags_toshow = []
        self.flg_showHiddenTables = 0

        self.buildMenu()
        self.buildWindow()
        self.specifyUI()
        if self.options:
            self.selected_item = self.options[0]
        
    def buildMenu(self):
        if self.menuList:
            for menuName in self.menuList:
                self.menuBar.deletemenu(menuName)
        self.menuList = []
        # Menu File
        self.menuBar.addmenu('File', 'Working with database files')
        self.menuList.append('File')
        self.menuBar.addmenuitem('File', 'command', 'Import file',
            command = self.menu_file_importTable,
            label = 'Import tables...')
        self.menuBar.addmenuitem('File', 'command', 'Export selected file',
            command = self.menu_file_exportTable,
            label = 'Export selected table...')
        '''
        self.menuBar.addmenuitem('File', 'command', 'Export all database',
            command = self.menu_file_updateDatabase,
            label = 'Update')
        '''
        #### TEMP
        self.menuBar.addmenuitem('File', 'command', 'Update database',
            command = self.menu_file_exportDatabase,
            label = 'Export all database...')
        if self.mode == "Associations":
            self.menuBar.addmenuitem('File', 'command', 'Save database changes',
                command = self.menu_file_save,
                label = 'Save associations...')
            self.menuBar.addmenu('Edit', 'Edit functions')
            self.menuList.append('Edit')
            self.menuBar.addmenuitem('Edit', 'command', 'Create a new table from the cluster and set association with this cluster',
                command = self.menu_edit_converCluster,
                label = 'Conver cluster to table...')
            self.menuBar.addmenuitem('Edit', 'command', 'Create new tables from the clusters and set association with these clusters',
                command = self.menu_edit_converAllCluster,
                label = 'Conver all clusters to tables')
        if self.mode != "top":
            self.menuBar.addmenuitem('File', 'command', 'Save the table as a cluster tree',
                command = self.menu_file_saveAsClusterTree,
                label = 'Save as cluster tree file')
            self.menuBar.addmenuitem('File', 'command', 'Save picture in JPG',
                command = self.menu_file_savePicture,
                label = 'Save picture')
        self.menuBar.addmenuitem('File', 'separator')
        self.menuBar.addmenuitem('File', 'command', 'Set reference patterns',
            command = self.menu_file_organize,
            label = 'Organize...')
        self.menuBar.addmenuitem('File', 'command', 'Check source files',
            command = self.menu_file_checkSources,
            label = 'Check sources')
        self.menuBar.addmenuitem('File', 'separator')
        self.menuBar.addmenuitem('File', 'command', 'Exit the application',
            command = self.menu_file_exit,
            label = 'Exit')
                
        if self.mode == "Tree":
            self.menuBar.addmenu('Edit', 'Edit functions')
            self.menuList.append('Edit')
            self.menuBar.addmenuitem('Edit', 'command', 'Set reference patterns',
                command = self.menu_edit_setReferences,
                label = 'Set references...')
            self.menuBar.addmenuitem('Edit', 'command', 'Rename or hide elements',
                command = self.menu_edit_hide_rename,
                label = 'Rename/Hide...')
            self.menuBar.addmenuitem('Edit', 'command', 'Delete elements',
                command = self.menu_edit_deleteElements,
                label = 'Delete elements...')
            self.menuBar.addmenuitem('Edit', 'separator')
            self.menuBar.addmenuitem('Edit', 'command', 'Recalculate',
                command = self.menu_edit_recalculate,
                label = 'Recalculate...')

            self.menuBar.addmenu('View', 'Different helpful statistics')
            self.menuList.append('View')    
            self.menuBar.addmenuitem('View', 'command', 'Search for end-node elements in this and child tables by a key word',
                command = self.menu_view_searchEndNodes,
                label = 'Search...')
            self.menuBar.addmenuitem('View', 'command', 'Search for elements on all levels of the tree by a key word',
                command = self.menu_view_searchOnLevels,
                label = 'Global search...')
            self.menuBar.addmenuitem('View', 'command', 'Show list of endnode elements',
                command = self.menu_view_showLeafList,
                label = 'Show end-node elements...')
            self.menuBar.addmenuitem('View', 'command', 'Show list of endnode elements',
                command = self.menu_view_showChildLeafList,
                label = 'Show subordinate end-node elements...')
            self.menuBar.addmenuitem('View', 'separator')
            self.menuBar.addmenuitem('View', 'command', 'Select elements',
                command = self.menu_view_select,
                label = 'Select...')
            self.menuBar.addmenuitem('View', 'command', 'Find element in this table and all child tables',
                command = self.menu_view_find,
                label = 'Find...')
            self.menuBar.addmenuitem('View', 'command', 'Unselect elements',
                command = self.menu_view_unselect,
                label = 'Unselect all')

            self.menuBar.addmenu('Identify', 'Identify nodes and clusters')
            self.menuList.append('Identify')    
            self.menuBar.addmenuitem('Identify', 'command', 'Identify nodes',
                command = self.menu_identify_nodes,
                label = 'Identify nodes...')
            self.menuBar.addmenuitem('Identify', 'command', 'Identify clusters',
                command = self.menu_identify_clusters,
                label = 'Identify clusters...')

    def specifyUI(self):
        self.balloon_x = Pmw.Balloon(self.root)
        
        # Command buttons
        self.command_buttons = Tkinter.Frame(self.frame_commands)
        self.command_buttons.pack(side=Tkinter.TOP,expand=0,fill=Tkinter.X)
        self.viewerType = Pmw.RadioSelect(self.command_buttons,
                    buttontype = 'radiobutton',
                    orient = 'horizontal',
                    labelpos = 'w',
                    command = self.viewertype_onselect,
                    label_text = 'Viewer:',
                    hull_borderwidth = 0,
                    hull_relief = None,
                    selectmode = 'single',
            )
        self.viewerType.pack(side=Tkinter.LEFT, padx=2)
        # Add some buttons to the RadioSelect.
        for text in ("Tree","Associations"):
            self.viewerType.add(text)
        self.viewerType.setvalue("Tree")
        
        # Check button 'Show hidden'
        checkbutton = Tkinter.Checkbutton(self.frame_buttons, text="Show hidden", command=self.show_hidden_oncheck)
        checkbutton.pack(side=Tkinter.LEFT)

        # Add buttons
        imagepath = "images"
        try:
            self.img_open = Tkinter.PhotoImage(file=os.path.join(imagepath,"open.gif"))
            self.img_delete = Tkinter.PhotoImage(file=os.path.join(imagepath,"delete.gif"))
            self.img_edit = Tkinter.PhotoImage(file=os.path.join(imagepath,"edit.gif"))
        except:
            imagepath = os.path.join("lib","images")
            self.img_open = Tkinter.PhotoImage(file=os.path.join(imagepath,"open.gif"))
            self.img_delete = Tkinter.PhotoImage(file=os.path.join(imagepath,"delete.gif"))
            self.img_edit = Tkinter.PhotoImage(file=os.path.join(imagepath,"edit.gif"))
        # button 'Open'
        btn_open = Tkinter.Button(self.frame_buttons, image=self.img_open, command=self.btn_open_onclick)
        btn_open.pack(side=Tkinter.LEFT)
        self.balloon_x.bind(btn_open,"Open")
        # button 'Edit'
        self.btn_edit = Tkinter.Button(self.frame_buttons, image=self.img_edit, command=self.btn_rename_onclick)
        self.btn_edit.pack(side=Tkinter.LEFT)
        self.balloon_x.bind(self.btn_edit,"Rename")
        self.btn_edit['state'] = Tkinter.DISABLED
        # button 'Delete'
        self.btn_delete = Tkinter.Button(self.frame_buttons, image=self.img_delete, command=self.btn_delete_onclick)
        self.btn_delete.pack(side=Tkinter.LEFT)
        self.balloon_x.bind(self.btn_delete,"Delete")
        
        # Add radiobuttons
        
        self.listbox['width'] = 40
        self.list_title['text'] = "Identification tables:"
        self.listbox['selectmode'] = 'single'
        
    def reconfigure_window(self):
        self.buildMenu()
        
    def remove_rPanel(self):
        if self.oViewer and self.oViewer.has_changed():
            self.oViewer.setChanged(0)
            result = tkMessageBox.askyesno("Warning!","Do you want to save associations set?")
            if result:
                self.save_associations()
        self.oViewer = None
        try:
            self.frame_right.destroy()
        except:
            pass
        self.mode = "top"
        self.reconfigure_window()
        
    def buildRightPanel(self,pattern_type=None,tbname=None):
        if pattern_type:
            self.pattern_type = pattern_type
        if not self.pattern_type:
            return
        if tbname:
            self.tbname = tbname
        else:
            if not self.selected_item or self.isPatternType(self.selected_item):
                return
            self.tbname = self.selected_item[4:]
        self.mode = self.viewerType.getcurselection()
        if self.oViewer and self.oViewer.has_changed():
            result = tkMessageBox.askyesno("Warning!","Do you want to save set associations?")
            if result:
                self.save_associations()
            self.oViewer.setChanged(0)
        if self.frame_right:
            self.frame_right.destroy()
        self.frame_right = Tkinter.Frame(self.frame_mainWindow,bd=2,relief=Tkinter.SUNKEN)
        self.frame_right.pack(side=Tkinter.RIGHT, expand=1, fill=Tkinter.BOTH)
        oTable,oGroup,oInfo = self.db.get_table(self.pattern_type,self.tbname,self.do)
        if self.mode == "Tree":
            self.oViewer = reports.DatabaseViewer(self.frame_right,self.do,None,tbname)
            self.oViewer.setGroups(oGroup)
            self.oViewer.setInfo(oInfo)
            oTable.setCutoff(0)
            self.oViewer.showTree(oTable)
        elif self.mode == "Associations":
            self.oViewer = reports.AssociationPanel(self.frame_right,self.db,self.do,self.balloon,tbname)
            self.oViewer.set_table(self.tbname + ":" + self.pattern_type)
        self.reconfigure_window()
        
    def setlistbox(self):
        self.listbox.delete(0,Tkinter.END)
        self.options = []
        for ptype in self.db.getPatternTypeList():
            self.listbox.insert(Tkinter.END,ptype)
            self.options.append(ptype)
            if ptype in self.flags_toshow:
                for tbname in self.db.getTableList(ptype,self.flg_showHiddenTables):
                    option = " ..." + tbname
                    self.listbox.insert(Tkinter.END,option)
                    self.options.append(option)
        
    def do(self,option,ArgList=None):
        if option == "Remove page":
            self.remove_rPanel()
        elif option == "Get visible tables":
            return self.db.getVisibleTables()
        elif option == "Get table info":
            names,flg_showLeaves = ArgList
            self.db.setTableInfo(names,flg_showLeaves)
            if self.has_changed():
                self.oViewer.setChanged()
            return self.db.getTableInfo(names)
        elif option == "Get pattern":
            seqname = ArgList[0]
            pattern_type = ArgList[1]
            return self.getPattern(seqname,pattern_type)
        elif option == "Compare patterns":
            first_name,second_name = ArgList
            return self.compare_patterns(first_name,second_name)
        elif option == "Update window":
            self.update_window()
        elif option == "Save associations":
            self.save_associations()
            self.setChanged(0)
        elif option == "Save table":
            result = self.db.do("Save table",ArgList)
            return result
        elif option == "Rename identification table":
            old_names,new_names = ArgList
            pattern_type,old_name = self.db.parse_tablename(old_names)
            pattern_type,new_name = self.db.parse_tablename(new_names)
            self.rename_table(old_name,new_name,pattern_type)
        elif option == "Rename":
            mode,old_name,new_name = ArgList
            if mode == "Clusters":
                self.rename_cluster(old_name,new_name)
            elif mode == "Leaf elements":
                self.rename_pattern(old_name,new_name)
            else:
                pass
        elif option == "Parse table names":
            return self.db.parse_tablename(ArgList)
        elif option == "Get pattern type":
            return self.pattern_type
        elif option == "Set changed":
            self.setChanged(ArgList)
        elif option == "Delete nodes":
            self.delete_nodes(ArgList)
        elif option == "Rearange nodes":
            for node in ArgList:
                oPattern = self.trigger("Get pattern",[node[0],self.trigger("Get pattern type"),"","",None])
                if oPattern:
                    self.rearrange_node(node,node[0],oPattern)
        elif option == "Import table":
            oTable,oInfo = ArgList
            return self.db.ask_save_table(oTable,oInfo)
        elif option == "Get sequence location info":
            if self.oViewer:
                return self.oViewer.getInfo()
            else:
                return None
        elif option == "Get available patterns":
            return self.db.getAvailablePatterns(self.pattern_type,self.tbname)
        elif option == "Select":
            self.oViewer.highlight()
            #self.buildRightPanel()
        elif option == "Unselect":
            #self.oViewer.dim()
            self.buildRightPanel()
        else:
            return self.trigger(option,ArgList)
        
    def save_associations(self):
        tableset = self.oViewer.getTableSet()
        self.db.saveRelatedTables(tableset)
        self.oViewer.setChanged(0)
        
    def save_clusterTree(self,fname):
        oTable,oGroup,oInfo = self.db.get_table(self.pattern_type,self.tbname)
        SupplementaryMaterials = {"Info":oInfo,"Group":None}
        tools.saveDBFile(oTable.getTableDictionary(),fname,SupplementaryMaterials)
        
    def saveTableSet(self,tableset):
        fname = tkFileDialog.asksaveasfilename(filetypes=[("Set of identification tables", "*.itb")])
        if not fname:
            return
        if len(tools.basename(fname)) <= 4 or tools.basename(fname)[-4:] != ".itb":
            fname += ".itb"
        tools.saveDBFile(tableset,fname)
        
    def importTableSet(self):
        fname = tkFileDialog.askopenfilename(filetypes=[("Set of identification tables", "*.itb")])
        if not fname:
            return
        tableset = tools.openDBFile(fname)[0]
        for pattern_type in tableset:
            for tbname in tableset[pattern_type]:
                oTable = nodes.MultidimensionalTable(tbname,self.do)
                oTable.loadTable(tableset[pattern_type][tbname]['table'])
                self.db.import_table(pattern_type,
                    tbname,
                    oTable,
                    #tableset[pattern_type][tbname]['groups'],
                    tableset[pattern_type][tbname]['info']
                )
        return 1
        
    def getTableSet(self,tbname,pattern_type,tableset={}):
        fname = self.db.getTableFileName(pattern_type,tbname)
        oTable,oGroup,oInfo = self.db.open_table(tbname,fname,self.do)
        oGroup = oTable.getGroups()
        if pattern_type not in tableset:
            tableset[pattern_type] = {}
        if tbname not in tableset[pattern_type]:
            tableset[pattern_type][tbname] = {"table":{},"groups":None,"info":{}}
            tableset[pattern_type][tbname]['table'].update(oTable.getTableDictionary())
        if oInfo:
            tableset[pattern_type][tbname]["info"].update(oInfo)
        tables = oGroup.get_child_nodes()
        for parent_node in tables:
            pattern_type,tbname = self.db.parse_tablename(tables[parent_node])
            tableset.update(self.getTableSet(tbname,pattern_type,tableset))
        return tableset
    
    def exportAllDatabase(self):
        tableset = {}
        for pattern_type in self.db.getPatternTypeList():
            for tbname in self.db.getTableList(pattern_type,1):
                fname = self.db.getTableFileName(pattern_type,tbname)
                oTable,oGroup,oInfo = self.db.open_table(tbname,fname,self.do)
                if pattern_type not in tableset:
                    tableset = {pattern_type:{tbname:{"table":oTable.getTableDictionary(),"groups":oGroup.copy(),"info":{}}}}
                else:
                    tablest[pattern_type] = {tbname:{"table":oTable.getTableDictionary(),"groups":oGroup.copy(),"info":{}}}
                if oInfo:
                    tableset[pattern_type][tbname]["info"].update(oInfo)
        return tableset
                
    def open_option_from_list(self,option):
        if self.isPatternType(option):
            if option in self.flags_toshow:
                self.flags_toshow.remove(option)
            else:
                self.flags_toshow.append(option)
            self.selected_item = self.pattern_type = option
            self.setlistbox()
            self.listbox.select_set(self.options.index(self.selected_item))
        else:
            ptype = self.definePatternType(option)
            self.buildRightPanel(ptype,option[4:])
            
    def definePatternType(self,option):
        pattern_list = self.db.getPatternTypeList()
        ptype = ""
        for i in range(len(pattern_list)-1,-1,-1):
            ptype = pattern_list[i]
            if self.options.index(option) > self.options.index(ptype):
                break
        return ptype
    
    def getPattern(self,seqname,pattern_type):
        if self.store.has(seqname):
            return self.store.get(seqname)
        oPattern = self.db.getPattern(self.pattern_type,self.tbname,seqname)
        if oPattern and pattern_type != self.pattern_type:
                oPattern = oPattern.convert(pattern_type[0],int(pattern_type[1]))
        if not oPattern:
            oInfo = self.oViewer.getInfo()
            fname = oInfo[seqname]['path']
            oPattern = self.trigger("Get pattern",[seqname,pattern_type,fname])
        if oPattern:
            self.store.add(oPattern,seqname)
        return oPattern
    
    def compare_patterns(self,first_name,second_name):
        return self.getPattern(first_name,self.pattern_type)-self.getPattern(second_name,self.pattern_type)

    def organize(self):
        visible_tables = self.db.getVisibleTables()
        hidden_tables = self.db.getHiddenTables()
        dialog = dialogs.dialog_TableOrganizer(self.root,visible_tables,hidden_tables,self.do)
        dialog.showGlobalModal()
        hidden_tables = dialog.get()
        if hidden_tables == None:
            return
        self.db.setHiddenTables(hidden_tables)
        self.setlistbox()
        if self.selected_item == "":
            pass
        elif self.selected_item[4:]+":"+self.pattern_type in hidden_tables:
            self.selected_item = self.pattern_type
            self.listbox.select_set(self.options.index(self.selected_item))
            self.btn_edit['state'] = Tkinter.DISABLED
        else:
            try:
                self.listbox.select_set(self.options.index(self.selected_item))
            except:
                pass
                
    def checkSources(self,flg_alert=False,flg_wholeDB=False):
        selected_tables = {}
        if flg_wholeDB:
            tblist = self.db.getAllTableList()
            for item in tblist:
                tbname,ptype = string.split(item,":")
                if ptype not in selected_tables:
                    selected_tables[ptype] = []
                selected_tables[ptype].append(tbname)
        else:
            selection = self.listbox.curselection()
            if not selection:
                return
            for i in selection:
                option = self.options[int(i)]
                if self.isPatternType(option) and option not in selected_tables:
                    selected_tables[option] = []
                else:
                    ptype = self.definePatternType(option)
                    if ptype not in selected_tables:
                        selected_tables[ptype] = [option[4:],]
                    else:
                        selected_tables[ptype].append(option[4:])
        for ptype in selected_tables:
            result = self.db.checkSources(ptype,selected_tables[ptype],flg_alert)
            if not result:
                return
            if result == 2 and len(selected_tables[ptype])==1:
                try:
                    oTable,oGroup,oInfo = self.db.get_table(ptype,selected_tables[ptype])
                    self.oViewer.setInfo(oInfo)
                except:
                    continue
        return 1
            
    def setReferences(self):
        self.oViewer.setReferences()
        if self.oViewer.has_changed():
            self.db.save_table(self.db.getTableFileName(self.pattern_type,self.tbname),
                self.oViewer.getTable(),self.oViewer.getInfo())
            self.oViewer.setChanged(0)
        
    def rename_table(self,old_name,new_name,pattern_type=None):
        if not pattern_type:
            pattern_type = self.pattern_type
        if self.selected_item[4:] == old_name:
            self.selected_item = " ..."+new_name
        if " ..."+old_name in self.options:
            self.options.append(" ..."+new_name)
            self.options.remove(" ..."+old_name)
        old_name += ":"+pattern_type
        new_name += ":"+pattern_type
        self.db.rename_table(old_name,new_name)
        self.setlistbox()
        self.listbox.select_set(self.options.index(self.selected_item))
        
    def rename_cluster(self,old_name,new_name):
        self.oViewer.rename_cluster(old_name,new_name)
        if self.oViewer.has_changed():
            self.db.save_table(self.db.getTableFileName(self.pattern_type,self.tbname),
                self.oViewer.getTable(),self.oViewer.getInfo())
            self.oViewer.setChanged(0)
        
    def rename_pattern(self,old_name,new_name):
        #self.db.rename_pattern(self.tbname,self.pattern_type,old_name,new_name)
        self.oViewer.rename_pattern(old_name,new_name)
        if self.oViewer.has_changed():
            self.db.save_table(self.db.getTableFileName(self.pattern_type,self.tbname),
                self.oViewer.getTable(),self.oViewer.getInfo())
            self.oViewer.setChanged(0)
            
    def hide_rename(self):
        self.oViewer.hide_rename()
        if self.oViewer.has_changed():
            self.db.save_table(self.db.getTableFileName(self.pattern_type,self.tbname),
                self.oViewer.getTable(),self.oViewer.getInfo())
            self.oViewer.setChanged(0)
        self.buildRightPanel()
        
    def delete_table(self,tablesToDelete):
        for i in range(len(tablesToDelete)):
            tablesToDelete[i] = int(tablesToDelete[i])
        tablesToDelete.sort()
        tablesToDelete.reverse()
        for i in tablesToDelete:
            selected_item = self.options[i]
            if self.isPatternType(selected_item):
                self.db.delete_pattern_type(selected_item)
                self.setlistbox()
            else:
                pattern_type = self.definePatternType(selected_item)
                result = self.db.delete_table(pattern_type,selected_item[4:])
                if not result:
                    self.db.delete_pattern_type(pattern_type)
                    self.setlistbox()
                else:
                    selected_item = pattern_type
                    self.setlistbox()
                    try:
                        self.listbox.select_set(self.options.index(selected_item))
                    except:
                        pass
                    self.btn_edit['state'] = Tkinter.DISABLED
    
    # nodes_todelete - list of node indecis
    def delete_nodes(self,nodes_todelete):
        respond = tools.askyesno("Do you want to delete "+str(len(result["All"]))+" selected elements?\n"+
            "Remember, that these elements will be removed from the database immediately!")
        if not respond:
            return
        oTable = self.oViewer.getTable()
        oInfo = self.oViewer.getInfo()
        for node_index in nodes_todelete:
            oTable.delete(node_index)
        result = self.db.import_table(self.pattern_type,
                self.tbname,
                oTable,
                oInfo,
                True, # Flag 'save patterns'
                True, # Flag 'replace table'
            )
        if not result:
            tools.alert("Table " + tbname + " was not saved!")
        self.buildRightPanel(self.pattern_type,self.tbname)

    def delete_elementsInSubordinates(self):
        collection = self.showChildLeafList()
        elements = {"All":collection.keys()}
        dialog = dialogs.dialog_scrolledListBox(self.root,elements,None,"Select element to delete",False,)
        dialog.showDialogNoGrab()
        result = dialog.get()
        if not result or not result["All"]:
            return
        respond = tools.askyesno("Do you want to delete "+str(len(result["All"]))+
            " selected elements in this and all subordinate trees?\n"+
            "Remember, that these elements will be removed from the database immediately!")
        if not respond:
            return
        to_delete = {}
        for name in result["All"]:
            for tb_ids in collection[name]:
                if tb_ids not in to_delete:
                    to_delete[tb_ids]=[]
                to_delete[tb_ids].append(name)
        for tb_ids in to_delete:
            ptype,tbname = string.split(tb_ids,":")
            tableset = self.db.get_table(ptype,tbname)
            if not tableset:
                continue
            oTable,oGroup,oInfo=tableset
            oGroup = oTable.getGroups()
            for species in to_delete[tb_ids]:
                node_index = oGroup.getSpeciesIndex(species)
                oTable.delete(node_index)
            fname = self.db.getTableFileName(ptype,tbname)
            if not fname:
                continue
            result = self.db.import_table(ptype,
                    tbname,
                    oTable,
                    oInfo,
                    True, # Flag 'save patterns'
                    True, # Flag 'replace table'
                )
            if not result:
                tools.alert("Table " + tbname + " was not saved!")
        self.buildRightPanel(self.pattern_type,self.tbname)
        
    def exit(self,event=None):
        if self.oViewer and self.oViewer.has_changed():
            self.oViewer.setChanged(0)
            result = tkMessageBox.askyesno("Warning!","Do you want to save associations set?")
            if result:
                self.save_associations()
        self.trigger("Remove database editor")
        self.root.destroy()
        
    def search_by_keyword(self, word, flg_onlevels=False):
        collection = {}
        tables = [self.oViewer.getTable()]
        used_tables = []
        while tables:
            oGroup = tables[-1].getGroups()
            for name in tables[-1].getLeaves():
                tb_ids = oGroup.get_child(name)
                if tb_ids:
                    if flg_onlevels and string.find(name,word) >= 0:
                        if name not in collection:
                            collection[name] = []
                        collection[name].append(tables[-1].getPatternType()+":"+tables[-1].getTableName())
                    if tb_ids in used_tables:
                        continue
                    used_tables.append(tb_ids)
                    tbname,ptype = string.split(tb_ids,":")
                    tables.insert(0,self.db.get_table(ptype,tbname)[0])
                elif str.find(name,word) >= 0:
                    if name not in collection:
                        collection[name] = []
                    collection[name].append(tables[-1].getPatternType()+":"+tables[-1].getTableName())
                else:
                    pass
            tables.pop()
        return collection
        
    def showChildLeafList(self):
        collection = {}
        tables = [self.oViewer.getTable()]
        used_tables = []
        while tables:
            oGroup = tables[-1].getGroups()
            for name in tables[-1].getLeaves():
                if name not in collection:
                    collection[name] = []
                collection[name].append(tables[-1].getPatternType()+":"+tables[-1].getTableName())
                tb_ids = oGroup.get_child(name)
                if tb_ids:
                    if tb_ids in used_tables:
                        continue
                    used_tables.append(tb_ids)
                    tbname,ptype = string.split(tb_ids,":")
                    tables.insert(0,self.db.get_table(ptype,tbname)[0])
            tables.pop()
        return collection
        
    def find(self):
        collection = self.showChildLeafList()
        elements = {"All":collection.keys()}
        dialog = dialogs.dialog_scrolledListBox(self.root,elements,None,"Select element to find",
            False,"single",)
        dialog.showDialogNoGrab()
        result = dialog.get()
        if not result:
            return
        name = result["All"][0]
        # report = {name:'pattern_type:table_name'}
        report = self.search_by_keyword(name)
        if not report:
            return
        ptype,tbname = str.split(report[name][0],":")
        if ptype not in self.flags_toshow:
            self.open_option_from_list(ptype)
        self.selected_item = " ..."+tbname
        self.open_option_from_list(self.selected_item)
        self.setlistbox()
        try:
            self.listbox.select_set(self.options.index(self.selected_item))
            self.oViewer.select(result["All"])
        except:
            pass
        
    def display_foundElements(self,title,collection):
        elements = collection.keys()
        if elements:
            elements.sort()
        report = []
        counter = 1
        for name in elements:
            if len(collection[name]) > 1:
                report.append("\t".join([str(counter),name,"{"+", ".join(collection[name])+"}"]))
            else:
                report.append("\t".join([str(counter),name,collection[name][0]]))
            counter += 1
        ouplib.TextEditor(title,"\n".join(report))

    def identifyNodes(self):
        result = self.trigger("Warn sequence length")
        if not result:
            return
        patterns = self.oViewer.getElements()
        if not patterns:
            return
        report = self.db.identify_patterns(patterns)
        if report:
            self.print_report(report)
        
    def identifyClusters(self):
        report = self.oViewer.identifyClusters()
        if report:
            self.print_report(report)
            
    def update_window(self):
        result = self.db.import_table(self.pattern_type,
                self.tbname,
                self.oViewer.getTable(),
                self.oViewer.getInfo(),
                True, # Flag 'save patterns'
                True, # Flag 'replace table'
            )
        if not result:
            tools.alert("Table " + tbname + " was not saved!")
        self.buildRightPanel(self.pattern_type,self.tbname)
        
    def isPatternType(self,option):
        if len(option) == 7 and option[0] in ("n","d","s") and option[2] == "_" and option[4:]=="mer":
            return 1
        else:
            return 0
        
    def print_report(self,report):
        self.trigger("Pickup report",report)
    
    # EVENTS
    def listboxOnClick(self,event):
        if not self.options:
            return
        item = self.options[self.listbox.nearest(event.y)]
        if self.isPatternType(item):
            self.btn_edit['state'] = Tkinter.DISABLED
        else:
            self.btn_edit['state'] = Tkinter.ACTIVE
        self.selected_item = item
        
    def listboxOnShiftClick(self,event):
        selected_item = self.listbox.nearest(event.y)
        if not self.selected_item:
            self.listboxOnClick(event)
        else:
            self.listbox.select_clear(0,Tkinter.END)
            index = self.options.index(self.selected_item)
            step = abs(index-selected_item)/(index-selected_item)
            for i in range(selected_item,index+step,step):
                if self.isPatternType(self.options[selected_item]) != self.isPatternType(self.options[i]):
                    i -= step
                    break
            self.listbox.select_set(i,selected_item)
            self.selected_item = self.options[selected_item]
            if self.isPatternType(self.selected_item):
                self.btn_edit['state'] = Tkinter.DISABLED
            else:
                self.btn_edit['state'] = Tkinter.ACTIVE
        
    def btn_open_onclick(self):
        if not self.selected_item:
            return
        self.open_option_from_list(self.selected_item)
        
    def btn_rename_onclick(self):
        name = self.selected_item[4:]
        while 1 > 0:
            dialog = dialogs.CustomEntry(self.root,"Rename identification table",[["Table",name],])
            dialog.showGlobalModal()
            newname = dialog.get()
            if newname == None or newname == name:
                return
            if newname == "":
                continue
            else:
                break
        ptype = self.definePatternType(self.selected_item)
        self.rename_table(name,newname,ptype)
        
    def btn_delete_onclick(self):
        selected_objects = self.currselection()
        if not selected_objects:
            return
        result = tkMessageBox.askyesno("Warning","Do you really want to delete selected objects?")
        if not result:
            return
        self.delete_table(selected_objects)
        
    def viewertype_onselect(self, option):
        self.mode = option
        if self.oViewer:
            self.buildRightPanel(self.pattern_type,self.tbname)
        
    def show_hidden_oncheck(self):
        self.flg_showHiddenTables = abs(self.flg_showHiddenTables-1)
        self.setlistbox()
        
    def menu_file_importTable(self):
        result = self.importTableSet()
        if result:
            self.setlistbox()
        
    def menu_file_exportTable(self):
        if not self.selected_item or self.isPatternType(self.selected_item):
            return
        if self.oViewer and self.oViewer.has_changed():
            result = tkMessageBox.askyesno("Warning!","Do you want to save associations set?")
            if result:
                self.save_associations()
                self.oViewer.setChanged(0)
        tbname = self.selected_item[4:]
        tableset = self.getTableSet(tbname,self.pattern_type)
        self.saveTableSet(tableset)
        
    def menu_file_exportDatabase(self):
        tableset = self.exportAllDatabase()
        self.saveTableSet(tableset)
        
    def menu_file_updateDatabase(self):
        for names in self.db.getAllTableList():
            ptype,tbname = self.db.parse_tablename(names)
            fname = self.db.getTableFileName(ptype,tbname)
            oTable,oGroup,oInfo = self.db.open_table(names,fname,self.do)
            oTable.parent_tables = []
            self.db.save_table(fname,oTable,oInfo,False)
        for names in self.db.getAllTableList():
            ptype,tbname = self.db.parse_tablename(names)
            fname = self.db.getTableFileName(ptype,tbname)
            oTable,oGroup,oInfo = self.db.open_table(names,fname,self.do)
            associations = oTable.getAssociations()
            child_tables = []
            flg_hasChanged = False
            for key in associations:
                child_names = associations[key]
                if child_names in child_tables:
                    continue
                child_ptype,child_tbname = self.db.parse_tablename(child_names)
                child_fname = self.db.getTableFileName(child_ptype,child_tbname)
                oChildTable,oChildGroup,oChildInfo = self.db.open_table(child_names,child_fname,self.do)
                oChildTable.addParentTable(names)
                self.db.save_table(child_fname,oChildTable,oChildInfo,False)
                flg_hasChanged = True
                child_tables.append(child_names)
            if flg_hasChanged:
                self.db.save_table(fname,oTable,oInfo,False)
        
    def menu_file_save(self):
        self.save_associations()
    
    def menu_file_saveAsClusterTree(self):
        if self.oViewer and self.oViewer.has_changed():
            result = tkMessageBox.askyesno("Warning!","Do you want to save set associations?")
            if result:
                self.save_associations()
                self.oViewer.setChanged(0)
        fname = tkFileDialog.asksaveasfilename(filetypes=[("Binary files", "*.clu")])
        if not fname:
            return
        if len(tools.basename(fname)) <= 4 or tools.basename(fname)[-4:] != ".clu":
            fname += ".clu"
        self.save_clusterTree(fname)
        
    def menu_file_savePicture(self):
        if not self.oViewer:
            return
        cv = self.oViewer.get_canvas()
        if not cv:
            return
        
        self.trigger("Save image",cv)
        self.buildRightPanel()
        
    def menu_file_organize(self):
        self.organize()
    
    def menu_file_checkSources(self):
        dialog = dialogs.RadioButtonDialog(self.root,"Which tables to check?",
                ["Selected tables","Whole database"],)
        dialog.showGlobalModal()
        respond = dialog.get()
        if not respond:
            return
        mode = respond[0]
        flg_wholeDB = False
        if mode == "Whole database":
            flg_wholeDB = True
        result = self.checkSources(False,flg_wholeDB)
        if result:
            self.remove_rPanel()
            tools.message("Success!","Source files have been checked successfully!")
        
    def menu_file_exit(self):
        self.exit()

    def menu_edit_setReferences(self):
        self.setReferences()
        
    def menu_edit_hide_rename(self):
        self.hide_rename()
        
    def menu_edit_deleteElements(self):
        dialog = dialogs.RadioButtonDialog(self.root,"Deletion options",
            ["Delete only in this tree","Delete in all subordinate trees"])
        dialog.showAppModal()
        result = dialog.get()
        if not result:
            return
        elif result[0] == "Delete only in this tree":
            self.oViewer.delete()
        else:
            self.delete_elementsInSubordinates()
        
    def menu_edit_recalculate(self):
        result = self.checkSources(True)
        if result:
            self.oViewer.recalculate()
        
    def menu_edit_converCluster(self):
        result = self.oViewer.converCluster2Table()
        if result:
            self.setlistbox()
        
    def menu_edit_converAllCluster(self):
        result = self.oViewer.converAllClusters2Tables()
        if result:
            self.setlistbox()
    
    def menu_view_searchEndNodes(self):
        word = tools.user_prompt(self.root,"Search for elements","Key word","")
        if not word:
            return
        report = self.search_by_keyword(word)
        self.display_foundElements("Elements found on this level",report)
    
    def menu_view_searchOnLevels(self):
        word = tools.user_prompt(self.root,"Search for elements","Key word","")
        if not word:
            return
        report = self.search_by_keyword(word,True)
        self.display_foundElements("Elements found on all levels",report)
    
    def menu_view_showLeafList(self):
        self.oViewer.showLeafList()
        
    def menu_view_showChildLeafList(self):
        report = self.showChildLeafList()
        self.display_foundElements("End-node elements on all levels",report)
        
    def menu_view_select(self):
        self.oViewer.highlight()
        
    def menu_view_find(self):
        self.find()
        
    def menu_view_unselect(self):
        self.buildRightPanel()
        
    def menu_identify_nodes(self):
        self.identifyNodes()
        
    def menu_identify_clusters(self):
        self.identifyClusters()
        
#########################################################################################################
class ChangedTablesInterface(GUI):
    def __init__(self,parent,tablesToUpdate,trigger,):
        GUI.__init__(self,parent,trigger)
        self.root.title("Changed tables")
        self.tablesToUpdate = tablesToUpdate
        self.unsaved_tables = self.tablesToUpdate.keys()
        self.oViewer = None
        self.frame_right = None
        self.mode = "top"
        self.tbname = ""
        self.menuList = []
        self.options = []
        
        # FLAGS
        self.flag_toshow = 1

        self.buildMenu()
        self.buildWindow()
        self.specifyUI()
        self.setChanged()
        
    def do(self,option,ArgList=None):
        if option == "Get pattern type":
            return self.parse_tablename(self.tbname)[1]
        elif option == "Remove page":
            self.oViewer = None
        elif option == "Save":
            self.save_table()
        else:
            pass
        
    def buildMenu(self):
        if self.menuList:
            for menuName in self.menuList:
                self.menuBar.deletemenu(menuName)
        self.menuList = []
        # Menu File
        self.menuBar.addmenu('File', 'Working with database files')
        self.menuList.append('File')
        self.menuBar.addmenuitem('File', 'command', 'Save file',
            command = self.menu_file_saveTable,
            label = 'Save selected table')
        self.menuBar.addmenuitem('File', 'command', 'Save file',
            command = self.menu_file_saveAllTables,
            label = 'Save all tables')
        self.menuBar.addmenuitem('File', 'separator')
        self.menuBar.addmenuitem('File', 'command', 'Exit the application',
            command = self.menu_file_exit,
            label = 'Exit')
                        
    def specifyUI(self):
        self.balloon_x = Pmw.Balloon(self.root)
        
        # Command buttons
        self.command_buttons = Tkinter.Frame(self.frame_commands)
        self.command_buttons.pack(side=Tkinter.TOP,expand=0,fill=Tkinter.X)
        btnSave = Tkinter.Button(self.command_buttons,text="Save all tables and close",command=self.btn_saveAll_onclick)
        btnSave.pack(side=Tkinter.LEFT, padx=2)

        # Add buttons
        imagepath = "images"
        try:
            self.img_open = Tkinter.PhotoImage(file=os.path.join(imagepath,"open.gif"))
        except:
            imagepath = os.path.join("lib","images")
            self.img_open = Tkinter.PhotoImage(file=os.path.join(imagepath,"open.gif"))
        btn_open = Tkinter.Button(self.frame_buttons, image=self.img_open, command=self.btn_open_onclick)
        btn_open.pack(side=Tkinter.LEFT)
        
        #self.balloon.bind(btn_open,"Open")
        self.balloon_x.bind(btn_open,"Open")
        
        self.listbox['width'] = 40
        self.list_title['text'] = "Identification tables:"
        self.listbox['selectmode'] = 'single'
        
    def reconfigure_window(self):
        self.buildMenu()
    
    def buildRightPanel(self,tbname):
        self.tbname = tbname
        if self.frame_right:
            self.frame_right.destroy()
        self.frame_right = Tkinter.Frame(self.frame_mainWindow,bd=2,relief=Tkinter.SUNKEN)
        self.frame_right.pack(side=Tkinter.RIGHT, expand=1, fill=Tkinter.BOTH)
        self.tbname = tbname
        oTable = self.tablesToUpdate[tbname]['table']
        oGroup = self.tablesToUpdate[tbname]['group']
        oInfo = self.tablesToUpdate[tbname]['info']
        self.oViewer = reports.DatabaseViewer(self.frame_right,self.do,None,tbname,"tablesToUpdate")
        self.oViewer.setGroups(oGroup)
        if self.isTableModified(self.tbname):
            self.oViewer.setChanged()
        self.oViewer.showTree(oTable)
        self.oViewer.select(self.tablesToUpdate[tbname]["seqnames"].keys())
        self.mode = "tree"
        self.reconfigure_window()
        
    def setlistbox(self):
        self.listbox.delete(0,Tkinter.END)
        self.options = []
        self.listbox.insert(Tkinter.END,"TABLES")
        self.options.append("TABLES")
        if self.flag_toshow:
            for tbname in self.tablesToUpdate:
                option = " ..." + tbname
                self.listbox.insert(Tkinter.END,option)
                self.options.append(option)

    def open_option_from_list(self,option):
        if option == "TABLES":
            self.flag_toshow = abs(self.flag_toshow-1)
            self.setlistbox()
        else:
            self.buildRightPanel(option[4:])
            
    def parse_tablename(self,names):
        pos = str.rfind(names,":")
        tbname = names[:pos]
        pattern_type = names[pos+1:]
        return tbname,pattern_type
            
    def save_table(self,tbname=None):
        if tbname:
            self.tbname = tbname
        if not self.tbname:
            tools.alert("Table was not selected!")
            return
        tbname,pattern_type = self.parse_tablename(self.tbname)
        for seqname in self.tablesToUpdate[self.tbname]["seqnames"]:
            self.tablesToUpdate[self.tbname]['info'][seqname] = {
                    "path":self.tablesToUpdate[self.tbname]["seqnames"][seqname]["fname"],
                    "seqname":seqname,
                    "index":1,
                    "stat":{
                        "GC":self.tablesToUpdate[self.tbname]["seqnames"][seqname]["GC"],
                        "PS":self.tablesToUpdate[self.tbname]["seqnames"][seqname]["PS"],
                        "OUV":self.tablesToUpdate[self.tbname]["seqnames"][seqname]["OUV"],
                        "length":self.tablesToUpdate[self.tbname]["seqnames"][seqname]["length"],
                    }
                }
        self.tablesToUpdate[self.tbname]['table'].setAssociations()
        oIdentifier = auxiliaries.Identifier(self.root,self.do)
        result = oIdentifier.import_table(pattern_type,
                tbname,
                self.tablesToUpdate[self.tbname]['table'],
                self.tablesToUpdate[self.tbname]['info'],
                True, # Flag 'save patterns'
                True, # Flag 'replace table'
            )
        if not result:
            tools.alert("Table " + self.tbname + " was not saved!")
            return
        try:
            self.unsaved_tables.remove(self.tbname)
        except:
            pass
        if self.oViewer:
            self.oViewer.setChanged(0)
        
    def save_all(self):
        tblist = []
        tblist.extend(self.unsaved_tables)
        for tbname in tblist:
            self.save_table(tbname)
        del tblist
        
    def exit(self,event=None):
        for tbname in self.tablesToUpdate:
            if self.isTableModified(tbname):
                result = tkMessageBox.askyesno("Warning!","One or more modified tables still are not saved\nDo you want to save them?")
                if result:
                    self.save_all()
                else:
                    break
        self.trigger("Remove database editor")        
        self.root.destroy()
        
    def isTableModified(self,tbname):
        if tbname not in self.unsaved_tables:
            return 0
        leaves = self.tablesToUpdate[tbname]['table'].getLeaves()
        for seqname in self.tablesToUpdate[tbname]['seqnames'].keys():
            if seqname in leaves:
                return 1
        self.unsaved_tables.remove(tbname)
        return 0
            
    #EVENTS
    def listboxOnClick(self,event):
        if not self.options:
            return
        item = self.options[self.listbox.nearest(event.y)]
        if len(item) > 4 and item[:4] == " ...":
            self.tbname = item[4:]
        
    def btn_open_onclick(self):
        pass
        
    def btn_saveAll_onclick(self):
        self.save_all()
        self.exit()
        
    def menu_file_saveTable(self):
        self.save_table()
        
    def menu_file_saveAllTables(self):
        self.save_all()
        
    def menu_file_exit(self):
        self.exit()
        
#########################################################################################################
class WorkSpace:
    # Constructor
    # ArgList = [datatype, [dataparameters]]
    def __init__(self,trigger,id="",parent=None,name=""):
        self.id = id
        if name:
            self.name = name
        else:
            self.name = id
        self.root = parent
        self.trigger = trigger
        self.pattern_type = None
        self.outermost = []
        self.dataset = {'Sequence name':'',
                    'Sequence description':'',
                    'Accession':'',
                    'Total sequence length':0,
                    'Locus length':0,
                    'Left border':0,
                    'Gene map':{},
                    }
        self.oViewer = None
        self.oTree = None
        self.oInfo = {}
        self.store = Store(self.trigger("Get buffer size"),self.do)
        
    def do(self,option,ArgList=None):
        if option == "Get pattern":
            if len(ArgList) <= 2:
                seqname = ArgList[0]
                if len(ArgList)==2:
                    pattern_type = ArgList[1]
                else:
                    pattern_type = self.pattern_type
                fname = ""
                sequence = ""
                oPattern = None
            else:
                seqname,pattern_type,fname,sequence,oPattern = ArgList
            return self.getPattern(seqname,pattern_type,fname,sequence,oPattern)
        elif option == "Compare patterns":
            first = ArgList[0]
            second = ArgList[1]
            if len(ArgList)>2 and ArgList[2]:
                pattern_type = ArgList[2]
            else:
                pattern_type = self.pattern_type
            return self.comparePatterns(first,second,pattern_type)
        elif option == "Get sequence location info":
            return self.getSeqLocationInfo()
        elif option == "Recalculate":
            self.trigger("Recalculate",[self.id,self.getSeqLocationInfo(),ArgList])
        elif option == "Merge dataset file":
            self.mergeDatasetFiles(ArgList)
            self.showTree()
        elif option == "Get pattern type":
            return self.pattern_type
        elif option == "Rename pattern":
            oldname,newname = ArgList
            return self.rename_pattern(oldname,newname)
        elif option == "Show distance matrix":
            self.showDistanceMatrix(ArgList)
        else:
            return self.trigger(option,ArgList)
            
    def exit(self):
        if self.oViewer:
            self.oViewer.exit()
        self.oViewer = None

    def processSequences(self,filelist,flg_append=0):
        temporary_database_folder = self.trigger("Get temporary database folder")
        tmpPath = os.path.join(os.path.curdir,temporary_database_folder,self.id)
        if not os.path.isdir(tmpPath):
            os.mkdir(tmpPath)
        self.oInfo = {}
        # if tmp folder exists, it must be deleted
        if os.path.isdir(tmpPath):
            for file_to_delete in os.listdir(tmpPath):
                try:
                    os.remove(os.path.join(tmpPath,file_to_delete))
                except:
                    pass
        else:
            os.mkdir(tmpPath)
        # save tmp files in the tmpPath folder
        counter = 1
        file_counter = 1
        seq_names = []
        patterns = {}
        pattern_type,normalization,wlength = self.parsePatternType()
        for fname in filelist.keys():
            seqlist = self.getSequence(fname,filelist[fname])
            if not seqlist:
                continue
            for seqname in seqlist:
                try:
                    if len(seqlist[seqname]) < 300:
                        print ("\tThe sequence " + seqname + " is too short - " + str(len(seqlist[seqname])) + " bp.")
                        continue
                    newseqname = self.check_seqname(seqname,seq_names)
                    print (counter, newseqname)
                    patterns[newseqname] = ouplib.Pattern(wlength)
                    patterns[newseqname].setPattern(seqlist[seqname],normalization,pattern_type)
                    self.oInfo[newseqname] = {"path":fname,"seqname":newseqname,"index":file_counter,"stat":{}}
                    self.oInfo[newseqname]['stat'].update(self.getPatternStat(patterns[newseqname]))
                    if counter%500 == 0:
                        tools.saveDBFile(patterns,os.path.join(tmpPath,"patterns#"+str(file_counter)))
                        patterns = {}
                        file_counter += 1
                    counter += 1
                    seq_names.append(newseqname)
                except:
                    continue
        if patterns:
            tools.saveDBFile(patterns,os.path.join(tmpPath,"patterns#"+str(file_counter)))
                        
    def setWatchtowers(self,elements=[],oTree=None,top_entries = "ALL"):
        maindir = self.trigger("Get main directory")
        curDir = self.trigger("Get current directory")
        if not oTree:
            oTree = nodes.Node(0,self.do)
        distance = 0
        i = 1
        curTime = time.clock()
        for fname in self.oInfo.keys():
            if fname == "fileinfo.dbf" or (elements and tools.basename(fname) not in elements):
                continue
            print (i,fname)
            try:
                oTree.add(fname)
            except:
                print ("\tError processing " + fname)
                continue
            #oTree.check()
            i += 1
            if top_entries != "ALL" and i >= top_entries+1:
                break
        return oTree
    
    def append(self, elements, set_id):
        oTree = self.setWatchtowers(elements)
        oViewer = reports.TreeViewer(None,self.do)
        oViewer.setTreeObject(oTree,self.pattern_type)
        oViewer.saveTable(self.id + "_" + str(set_id) + ".wtw")
        
    def openWorkspaceFile(self,fname):
        temporary_database_folder = self.trigger("Get temporary database folder")
        tmpPath = os.path.join(os.path.curdir,temporary_database_folder,self.id)
        # if tmp folder exists, it must be deleted
        if os.path.isdir(tmpPath):
            for file_to_delete in os.listdir(tmpPath):
                try:
                    os.remove(os.path.join(tmpPath,file_to_delete))
                except:
                    pass
        else:
            os.mkdir(tmpPath)
        WSP,SupplementaryMaterials = tools.openDBFile(fname)
        if not self.setSeqLocationInfo(WSP["info"]):
            tkMessageBox.showerror("Error!","Error opening the file " + fname)
            return 0
        for key in WSP["patterns"].keys():
            ptfile = os.path.join(tmpPath,"patterns#"+str(key))
            tools.saveDBFile(WSP["patterns"][key],ptfile)
        self.pattern_type = WSP["pattern type"]
        self.oViewer = WorkSpaceInterface(Tkinter.Toplevel(self.root),self.do,tools.basename(fname))
        self.oViewer.setWorkSpace(WSP,fname)
        
    def openTreeFile(self, fname):
        temporary_database_folder = self.trigger("Get temporary database folder")
        tmpPath = os.path.join(os.path.curdir,temporary_database_folder,self.id)
        # if tmp folder exists, it must be deleted
        if os.path.isdir(tmpPath):
            for file_to_delete in os.listdir(tmpPath):
                try:
                    os.remove(os.path.join(tmpPath,file_to_delete))
                except:
                    pass
        else:
            os.mkdir(tmpPath)
        DB,SupplementaryMaterials = tools.openDBFile(fname)
        if not self.setSeqLocationInfo(SupplementaryMaterials["Info"]):
            tkMessageBox.showerror("Error!","Error opening the file " + fname)
            return 0
        for key in SupplementaryMaterials["Patterns"].keys():
            fname = os.path.join(tmpPath,"patterns#"+str(key))
            tools.saveDBFile(SupplementaryMaterials["Patterns"][key],fname)
        self.pattern_type = SupplementaryMaterials["Pattern type"]
        self.oTree = nodes.Node(0,self.do)
        self.oTree.importTree(DB)
        
    def openProjectionFile(self, fname):
        try:
            DataSet,info = tools.openDBFile(fname)
        except:
            tools.alert("File " + tools.basename(fname) + " is corrupted!")
            return None
        if not self.setSeqLocationInfo(info):
            tkMessageBox.showerror("Error!","Error opening the file " + fname)
            return 0
        self.oViewer = WorkSpaceInterface(Tkinter.Toplevel(self.root),self.do,self.name)
        self.oViewer.open_projection(DataSet)
        
    def openClusterTreeFile(self,fname):
        try:
            table,SupplementaryMaterials = tools.openDBFile(fname)
        except:
            tools.alert("File " + tools.basename(fname) + " is corrupted!")
            return
        if table:
            if not self.setSeqLocationInfo(SupplementaryMaterials["Info"]):
                tkMessageBox.showerror("Error!","Error opening the file " + fname)
                return 0
            oTable = nodes.MultidimensionalTable(table["Name"],self.do)
            oTable.loadTable(table)
            #oTable.setGroups(SupplementaryMaterials["Group"])
        else:
            tools.alert("File " + tools.basename(fname) + " is corrupted!")
            return
        self.oViewer = WorkSpaceInterface(Tkinter.Toplevel(self.root),self.do,self.name)
        self.oViewer.open_clusterTree(oTable)
        
    def openReportFile(self,fname):
        try:
            report,SupplementaryMaterials = tools.openDBFile(fname)
        except:
            tools.alert("File " + tools.basename(fname) + " is corrupted!")
            return
        self.pickup_report(report)
        
    def pickup_report(self,report):
        if report:
            self.oViewer = WorkSpaceInterface(Tkinter.Toplevel(self.root),self.do,self.name)
            self.oViewer.open_report(report)
            self.oViewer.setChanged()
        else:
            tools.alert("File " + tools.basename(fname) + " is corrupted!")
            return
        
    def showTree(self,counter=0,oTree=None,flg_blind=0):
        if oTree:
            self.oTree = oTree
        if not self.oViewer:
            if flg_blind:
                self.oViewer = WorkSpaceInterface(None,self.do,self.name)
            else:
                self.oViewer = WorkSpaceInterface(Tkinter.Toplevel(self.root),self.do,self.name)
        if counter:
            self.merge_datasets(counter)
        else:
            try:
                os.remove(tmp_fname)
            except:
                pass
        self.oViewer.set_data(self.oTree)
        return self.oViewer
    
    def showDistanceMatrix(self,dmatrix,flg_showoutput=1,flg_showstat=1):
        abbreviations = {}
        # Create distance table
        output = str(len(dmatrix['members']))+"\n"
        data = [[],[]]
        for item in dmatrix['members']:
            ptname = item[1]
            if "replacements" in dmatrix:
                name = dmatrix["replacements"][ptname]
            else:
                name = ptname
            data[0].append(name)
            data[1].append([])
            abbr = self.getAbbreviation(name,abbreviations.keys(),10)
            abbreviations[abbr] = name
            output += abbr + " "
            values = []
            for element in dmatrix['members']:
                second_pattern = element[1]
                if ptname == second_pattern:
                    values.append("0.0")
                    data[1][-1].append(0)
                else:
                    values.append(str(dmatrix['table'][ptname][second_pattern]))
                    data[1][-1].append(dmatrix['table'][ptname][second_pattern])
            output += " ".join(values) + "\n"
        output += "\n\n"

        # Check additivness and ultrametry
        if len(abbreviations) >= 4:
            oTester = distmatrixtype.DistMatrixType(data)
            output += oTester.getReport()
            del oTester
        
        # Add list of abbreviations
        output += "#"*45 + "\n" + "Abbreviations:" + "\n"
        for abbr in abbreviations.keys():
            output += abbr + "\t" + abbreviations[abbr] + "\n"
            
        # Show table
        if flg_showoutput:
            ouplib.TextEditor("Distance matrix "+self.name,output,Tkinter.Toplevel(self.root))
            
        return output
        
    def showPhylogeneticTree(self, mode, counter=0, output=None):
        import subprocess
        path = os.path.join(os.path.curdir,"lib","phylip")
        # Remove old tmp files
        for item in ("outfile","outtree","intree.phy"):
            tmpfile = os.path.join(os.path.curdir,item)
            if os.path.isfile(tmpfile):
                try:
                    os.remove(tmpfile)
                except:
                    pass
        fname = os.path.join(os.path.curdir,"infile")
        self.prepare_infile(fname,counter,output)
        while not os.path.isfile(fname):
            pass
        if mode == "neighbour":
            subprocess.call(os.path.join(path,"neighbor.exe"))
        elif mode == "fitch":
            subprocess.call(os.path.join(path,"fitch.exe"))
        elif mode == "kitsch":
            subprocess.call(os.path.join(path,"kitsch.exe"))
        else:
            return
        if os.path.isfile(os.path.join(os.path.curdir,"outtree")):
            intree = os.path.join(os.path.curdir,"intree.phy")
            os.rename(os.path.join(os.path.curdir,"outtree"),intree)
            while not os.path.isfile(intree):
                pass
            try:
                os.startfile(intree)
            except:
                tools.alert("Problem with starting the tree file!\nYou have to install a TreeViewer to view '.phy' files.")
        for item in ("outfile","outtree","infile"):
            tmpfile = os.path.join(os.path.curdir,item)
            if os.path.isfile(tmpfile):
                try:
                    os.remove(tmpfile)
                except:
                    pass
        
    def prepare_infile(self,fname,counter=0,output=None):
        if not output:
            output = self.showDistanceMatrix(counter,None,None)
        ofp = open(fname, "w")
        ofp.write(output)
        ofp.flush()
        ofp.close()
                
    def getAbbreviation(self,word,used,limit):
        if len(word) <= limit:
            return word + " "*(limit-len(word))
        abbr = word[:limit]
        if abbr not in used:
            return abbr
        count = 2
        abbr = word[:limit-2] + "#1"
        while abbr in used:
            suffix = "#" + str(count)
            ending = limit - len(suffix)
            abbr = abbr[:ending] + suffix
            count += 1
        return abbr
        
    def getDistanceMatrix(self,counter=0):
        if counter:
            self.merge_datasets(counter)
        else:
            try:
                os.remove(tmp_fname)
            except:
                pass
        pattern_list = self.oTree.getLeaves()
        dmatrix = {"table":{},"members":[]}
        for i in range(len(pattern_list)-1):
            dmatrix['members'].append([pattern_list[i]])
            for j in range(i,len(pattern_list)):
                if pattern_list[i] not in dmatrix['table']:
                    dmatrix['table'][pattern_list[i]] = {}
                if pattern_list[j] not in dmatrix['table']:
                    dmatrix['table'][pattern_list[j]] = {}
                dist = self.comparePatterns(pattern_list[i],pattern_list[j])
                dmatrix['table'][pattern_list[i]][pattern_list[j]] = dist
                dmatrix['table'][pattern_list[j]][pattern_list[i]] = dist
        dmatrix['members'].append([pattern_list[-1]])
        for i in range(len(pattern_list)):
            ptname = dmatrix['members'][i][0]
            sum = 0
            for key in dmatrix['table'][ptname].keys():
                sum += dmatrix['table'][ptname][key]
            dmatrix['members'][i].insert(0,sum)
        if len(dmatrix['members']) > 1:
            dmatrix['members'].sort(reverse=True)
        
    def merge_datasets(self, counter):
        for i in range(counter):
            tmp_fname = self.id + "_" + str(i) + ".wtw"
            self.mergeDatasetFiles(tmp_fname)
            try:
                os.remove(tmp_fname)
            except:
                pass
        
    def mergeDatasetFiles(self, fname):
        temporary_database_folder = self.trigger("Get temporary database folder")
        if not self.oTree:
            self.openTreeFile(fname)
            return
        tmpPath = os.path.join(os.path.curdir,temporary_database_folder,self.id)
        DB,SupplementaryMaterials = tools.openDBFile(fname)
        if SupplementaryMaterials["Pattern type"] != self.pattern_type:
            tools.alert("Pattern type mismatch!\nThe file " + tools.basename(fname) + " cannot be merged.")
            return
        oInfo = SupplementaryMaterials["Info"]
        file_index = self.getFileIndex()+1
        for key in SupplementaryMaterials["Patterns"].keys():
            fname = os.path.join(tmpPath,"patterns#"+str(file_index))
            tools.saveDBFile(SupplementaryMaterials["Patterns"][key],fname)
            for pattname in SupplementaryMaterials["Patterns"][key].keys():
                oInfo[pattname]["index"] = file_index
        self.oInfo.update(oInfo)
        node = nodes.Node(0,self.do)
        node.importTree(DB)
        outermosts = node.getListOfOutermosts()
        all_species = node.getLeaves()
        for species in outermosts:
            print ("\t" + species)
            self.oTree.add(species)
        for species in all_species:
            if species not in outermosts:
                print ("\t" + species)
                self.oTree.add(species)

    def check_seqname(self,seqname,names):
        for symb in ("\\","/",":","*","?","\"","<",">","|"):
            seqname = str.replace(seqname,symb," ")
        while seqname and seqname[0] == " ":
            seqname = seqname[1:]
        pos = str.find(seqname,", complete")
        if pos != -1:
            seqname = seqname[:pos]
        while seqname and (seqname[-1] == "." or seqname[-1]) == " ":
            seqname = seqname[:-1]
        if not seqname:
            seqname = "#1"
        if not names:
            return seqname
        while string.upper(seqname) in names:
            sep = string.rfind(seqname,"#")+1
            if sep == 0:
                seqname += " #1"
            else:
                try:
                    n = int(seqname[sep:])
                except:
                    return seqname + " #1"
                seqname = seqname[:sep] + str(n+1)
        return seqname
       
    def getSequence(self,fname,names=[]):
        # seqlist = {seqname:sequence}
        seqlist = {}
        if (len(fname) > 3 and fname[-3:] == ".gb") or (len(fname) > 4 and fname[-4:] == ".gbk"):
            try:
                dataset,sequence = self.getSequenceFromGBK(fname)
            except:
                return None
            seqname = dataset["Sequence name"]
            seqlist[seqname] = sequence
        elif len(fname) > 5 and fname[-5:] == ".gbff":
            seqlist.update(self.getSeqFromGBFF(fname,names))
        else:
            seqlist.update(self.getSeqFromFASTA(fname,names))
        return seqlist
    
    def getSeqFromFASTA(self,fname,names=[]):
        seqlist = {}
        objFile = open(fname)
        line = objFile.read()
        objFile.close()
        genomes = string.split(line,">")
        if len(genomes) < 2:
            return seqlist
        for g in range(1,len(genomes)):
            genome = genomes[g]
            pos = string.find(genome,'\n')
            if pos == -1:
                continue
            seqname = self.parse_seqname(genome[:pos],seqlist.keys())
            if names and seqname not in names:
                continue
            sequence = genome[pos:]
            sequence = string.replace(sequence,'\n','')
            sequence = string.upper(sequence)
            seqlist[seqname] = sequence
        return seqlist
    
    def addGene(self, gene, seqlendigits):
        subkeys = ('start','stop','direction','name','description','remark')
        key = (seqlendigits - len(str(gene[0])))*" " + str(gene[0]) + "-" + str(gene[1])
        self.dataset["Gene map"][key] = {}
        for i in range(len(subkeys)):
            self.dataset["Gene map"][key][subkeys[i]] = gene[i]
        
    def getSequenceFromGBK(self,fname):
        file = open(fname,'r')
        line = "line"
        seqlendigits = 7
        gene = []
        ind = None
        CDS = None
        while line:
            line = file.readline()
            if (line == '' or line == '\n'):
                if CDS==1 and len(gene) == 6:
                    self.addGene(gene,seqlendigits)
                break
            elif line[:5] == 'LOCUS':
                self.dataset['Accession'] = line[12:string.find(line," ",12)]
                seqlendigits = len(line[34:string.find(line," ",34)])
            elif line[:10] == 'DEFINITION':
                if string.find(string.upper(line),"PLASMID") > -1:
                    self.dataset['Sequence description'] = "plasmid";
                else:
                    self.dataset['Sequence description'] = "chromosome";
                seq_name = line[12:-1]
                self.dataset['Sequence name'] = seq_name
            elif line[:6] == 'SOURCE' and not self.dataset['Sequence name']:
                source = line[12:-1]
                source = string.replace(source,"str. ","")
                self.dataset['Sequence name'] = source
            elif line[:11] == "     source":
                pos = string.rfind(line,".")
                if pos > 11:
                    seqlendigits = len(line)-pos-2
            elif line[5:8] == 'CDS':
                ind = None
                CDS = 1
                if len(gene) == 6:
                    self.addGene(gene,seqlendigits)
                    gene = []
                values = line[21:].split('.')
                if values[2][0] == ">" or values[2][0] == "<":
                    values[2] = values[2][1:]
                if values[0].find('complement') >= 0:
                    if values[0].find('join') >= 0:
                        try:
                            gene.append(int(values[0][16:]))
                        except:
                            try:
                                gene.append(int(values[0][17:]))
                            except:
                                print ('Error value fot int(): ' + values[0][17:])
                                return None
                        gene.append(int(values[len(values)-1][:-3]))
                        gene.append('rev')
                    else:   
                        try:
                            gene.append(int(values[0][11:]))
                        except:
                            try:
                                gene.append(int(values[0][12:]))
                            except:
                                print ('Error value fot int(): ' + values[0][12:])
                                return None
                        gene.append(int(values[2][:-2]))
                        gene.append('rev')
                elif values[0].find('join') >= 0:
                    try:
                        gene.append(int(values[0][5:]))
                    except:
                        try:
                            gene.append(int(values[0][6:]))
                        except:
                            print ('Error value fot int(): ' + values[0][6:])
                            return None
                    gene.append(int(values[len(values)-1][:-2]))
                    gene.append('dir')
                else:
                    try:
                        gene.append(int(values[0]))
                    except:
                        try:
                            gene.append(int(values[0][1:]))
                        except:
                            print ('Error value for int(): ' + values[0][1:])
                            return None
                    gene.append(int(values[2]))
                    gene.append('dir')
                for i in range(3):
                    gene.append('')
            elif line[21:22] == r"/" and CDS == 1:
                if line[21:27] == '/gene=' and len(gene) == 6:
                    ind = 3
                    gene[ind] = line[28:-1]
                    if gene[ind] != '' and  gene[ind][-1] == "\"":
                        gene[ind] = gene[ind][:-1]
                        ind = None
                elif line[21:30] == '/product=' and len(gene) == 6:
                    ind = 5
                    gene[ind] = line[31:-1]
                    if gene[ind] != '' and  gene[ind][-1] == "\"":
                        gene[ind] = gene[ind][:-1]
                        ind = None
                elif line[21:27] == '/note=' and len(gene) == 6:
                    ind = 4
                    gene[ind] = line[28:-1]
                    if gene[ind] != '' and gene[ind][-1] == "\"":
                        gene[ind] = gene[ind][:-1]
                        ind = None
                elif line[21:34] == '/translation=':
                    CDS = None
                else:
                    pass
            elif line[:6] == 'ORIGIN':
                ind = None
                if len(gene) == 6:
                    self.addGene(gene,seqlendigits)
                seq = file.read()
                for num in range(10):
                    seq = str.replace(seq,str(num),'')
                seq = str.replace(seq,' ','')
                seq = str.replace(seq,'//','')
                seq = str.replace(seq,'\n','')
                seq = str.upper(seq)
                break
            else:
                if ind and CDS == 1:
                    gene[ind] = gene[ind] + " " + line[21:-1]
                    if gene[ind][-1] == "\"":
                        gene[ind] = gene[ind][:-1]
                        ind = None
                    
        file.close()
        return self.dataset,seq

    # check if the proposed fname already exists in the database
    # if so, change the name or return the proposed name
    
    def getSeqFromGBFF(self,fname,names=[]):
        try:
            f = open(fname,"r")
            data = f.read()
            f.close()
        except:
            return {}
        data = string.split(data,"\n")
        seqlist = {}
        seqname = ""
        sequence = ""
        counter = 0
        END_COUNT = len(data)
        while counter < END_COUNT:
            if not data[counter]:
                counter += 1
                continue
            if len(data[counter]) >= 12 and data[counter][:12] == "DEFINITION  ":
                seqname = data[counter][12:]
                if names and seqname not in names:
                    continue
                i = 1
                if seqname in seqlist:
                    seqname += " #" + str(i)
                while seqname in seqlist:
                    seqname = seqname[:-len(str(i))] + str(i+1)
                    i += 1
                seqlist[seqname] = ""
            if len(data[counter]) >= 12 and data[counter][:12] == "ORIGIN      ":
                counter += 1
                while data[counter] != "//":
                    line = data[counter][10:]
                    line = str.replace(line," ","")
                    line = str.upper(line)
                    seqlist[seqname] += line
                    counter += 1
                seqname = ""
            counter += 1
        return seqlist
        

    def  getNewFileName(self,tmpPath,seqname,sequence):
        return os.path.join(tmpPath,seqname)
    
    def addToTemporaryDatabase(self,sequence,fname):
        pattern_type,normalization,wlength = self.parsePatternType()
        # Create new object Sequence
        objSeq = ouplib.Sequence(tools.basename(fname),"",sequence)
        pattName = pattern_type + str(normalization) + "_" + str(wlength) + "mer"
        objPattern = objSeq.generatePattern(wlength,pattern_type,normalization)
        objSeq.addPattern(objPattern,pattName+",0-"+str(len(sequence))+" bp.")
        try:
            tools.saveDBFile(objPattern,fname)
        except:
            print ("Error saving temporary database file",fname)
            
    def getPatternType(self):
        return self.pattern_type
    
    def setPatternType(self,ptype):
        self.pattern_type = ptype
    
    def parsePatternType(self):
        pattern_type = self.pattern_type[0]
        normalization = int(self.pattern_type[1])
        wlength = int(self.pattern_type[3])
        return pattern_type,normalization,wlength

    def parse_seqname(self,line,seq_names):
        if line > 3 and line[:3]=="gi|":
            seqname_elements = str.split(line,"|")
            if len(seqname_elements)==5:
                seqname = seqname_elements[4]
                pos = str.find(seqname,", complete sequence")
                if pos > -1:
                    seqname = seqname[:pos]
                if str.find(seqname_elements[3],"NC_")==0:
                    accession = seqname_elements[3]
                    pos = str.find(accession,".")
                    if pos > -1:
                        accession = accession[:pos]
                    seqname += " [" + accession + "]"
            else:
                seqname = seqname_elements[0]
        else:
            seqname = line
        seqname = self.check_seqname(seqname,seq_names)
        return seqname
        
    def getPattern(self,name,pattern_type,fname="",sequence="",oPattern=None):
        maindir = self.trigger("Get main directory")
        temporary_database_folder = self.trigger("Get temporary database folder")
        path = os.path.join(maindir,temporary_database_folder,self.id)
        if oPattern: 
            if oPattern.getPatternName()==pattern_type:
                return oPattern
            else:
                oPattern = oPattern.convert(pattern_type[0],int(pattern_type[1]))
                if oPattern:
                    return oPattern
        oPattern = self.store.get(name,path)
        if oPattern and oPattern.getPatternName() != pattern_type:
            oPattern = oPattern.convert(pattern_type[0],int(pattern_type[1]))
        if oPattern:
            return oPattern
        if not fname and name in self.oInfo:
            fname = self.oInfo[name]['path']
        if fname or sequence or oPattern:
            return self.trigger("Get pattern",[name,pattern_type,fname,sequence,oPattern])
        else:
            return None

    def comparePatterns(self,first,second,pattern_type=None):
        if not pattern_type:
            pattern_type = self.pattern_type
        temporary_database_folder = self.trigger("Get temporary database folder")
        try:
            path = os.path.join(temporary_database_folder,self.id)
        except:
            path = temporary_database_folder + "\\" + self.id
        if type(first) == type("text"):
            if self.store.hasDistance(first,second):
                return self.store.getDistance(first,second)
            else:
                patterns = []
                for pattern in (first,second):
                    if self.store.has(pattern):
                        patterns.append(self.store.get(pattern,path))
                    else:
                        patterns.append(self.getPattern(pattern,pattern_type))
                dist = patterns[0] - patterns[1]
                if dist != None:
                    self.store.setDistance(first,second,dist)
                else:
                    print ("gui:4667",patterns,patterns[0].getPatternName(),patterns[1].getPatternName())
                return dist
        else:
            return first - second
    
    def getSeqLocationInfo(self):
        return self.oInfo
        
    def setSeqLocationInfo(self,info):
        # check info
        flg_checked = 0
        while flg_checked == 0:
            for key in info:
                if not os.path.exists(info[key]['path']):
                    respond = tkMessageBox.askyesno("File persistance problem!","Information about location of the source sequence files is not correct!\nDo you want to select a current folder with the source files?")
                    if respond:
                        info = self.updateSequenceLocationInfo(info)
                        if not info:
                            return 0
                        flg_checked = 0
                        break
                    else:
                        return 0
                else:
                    flg_checked = 1
        self.oInfo = {}
        self.oInfo.update(info)
        return 1
    
    def updateSequenceLocationInfo(self,info):
        folder = tkFileDialog.askdirectory()
        if not folder:
            return None
        for key in info:
            info[key]['path'] = os.path.join(folder,tools.basename(info[key]['path']))
        return info
        
    def getPatternStat(self,oPattern):
        stat = {"length":oPattern.getSeqLength(),
                "GC":oPattern.getPercentage('GC'),
                "PS":oPattern.getPS(),
                "OUV":oPattern.getOUV(),
            }
        return stat
    
    def rename_pattern(self,oldname,newname):
        if newname in self.oInfo:
            tools.alert("Name " + newname + " already exists!")
            return 0
        self.oInfo[newname] = {}
        self.oInfo[newname].update(self.oInfo[oldname])
        del self.oInfo[oldname]
        self.store.rename_pattern(oldname,newname)
        return 1
    
    def getFileIndex(self):
        ind = 1
        for pattname in self.oInfo:
            if self.oInfo[pattname]['index'] > ind:
                ind = self.oInfo[pattname]['index']
        return ind
        
    def copy(self,workspace_id):
        maindir = self.trigger("Get main directory")
        temporary_database_folder = self.trigger("Get temporary database folder")
        currdir = os.path.join(maindir,temporary_database_folder,self.id)
        newdir = os.path.join(maindir,temporary_database_folder,workspace_id)
        if os.path.isdir(newdir):
            for fname in os.listdir(newdir):
                try:
                    os.remove(os.path.join(newdir,fname))
                except:
                    pass
        else:
            os.mkdir(newdir)
        for fname in os.listdir(currdir):
            data,stat = tools.openDBFile(os.path.join(currdir,fname))
            tools.saveDBFile(data,os.path.join(newdir,fname),stat)

    def setFileName(self,fname):
        self.oViewer.setFileName(fname)
        
    def setChanged(self):
        if self.oViewer:
            self.oViewer.setChanged()
        
######################################################################################################
class Store:
    def __init__(self,buffer_size=500,trigger=None):
        # container of patterns and distances
        self.container = {}
        # currently open file of patterns of the workspace
        self.patterns = {}
        # Buffer size
        self.buffer_size = buffer_size
        # Sequence location info - points to the same object as the workspace self.oInfo
        self.trigger = trigger
        
    def reset(self):
        self.container = {}
        self.patterns = {}
        
    def rename_pattern(self,oldname,newname):
        if oldname in self.patterns:
            self.patterns[newname] = {}
            self.patterns[newname] = self.patterns[oldname].copy()
            del self.patterns[oldname]
        if oldname in self.container:
            self.container[newname] = {}
            self.container[newname].update(self.container[oldname])
            del self.container[oldname]
        else:
            pass
        
    def add(self,pattern,key):
        self.container[key] = {"value":pattern, "time":time.clock(), "references":{}}
        if len(self.container.keys()) > self.buffer_size:
            self.ridof()
        return
    
    def has(self,key):
        return key in self.container
            
    def get(self,key,path=None):
        if key in self.container:
            self.container[key]["time"] = time.clock()
            return self.container[key]["value"]
        elif key in self.patterns:
            return self.patterns[key]
        elif path:
            try:
                info = self.trigger("Get sequence location info")
                if not info:
                    return None
                fname = os.path.join(path,
                    "patterns#"+str(info[key]["index"]))
                self.patterns,stat = tools.openDBFile(fname)
                oPattern = self.patterns[info[key]["seqname"]]
                self.add(oPattern,key)
                return oPattern
            except:
                return None
        else:
            return None
        
    def setDistance(self,first,second,value):
        if self.has(first):
            first_time = self.container[first]["time"]
            if self.has(second):
                second_time = self.container[second]["time"]
                if first_time < second_time:
                    self.container[first]["references"][second] = value
                    self.container[first]["time"] = time.clock()
                else:
                    self.container[second]["references"][first] = value
                    self.container[second]["time"] = time.clock()
        else:
            if self.has(second):
                self.container[second]["references"][first] = value
                self.container[second]["time"] = time.clock()
                
    def hasDistance(self,first,second):
        if ((self.has(first) and second in self.container[first]["references"]) or
            (self.has(second) and first in self.container[second]["references"])):
            return 1
        else:
            return 0
                
    def getDistance(self,first,second):
        if self.has(first) and second in self.container[first]["references"]:
            self.container[first]["time"] = time.clock()
            return self.container[first]["references"][second]
        elif self.has(second) and first in self.container[second]["references"]:
            self.container[second]["time"] = time.clock()
            return self.container[second]["references"][first]
        else:
            return None
        
    def ridof(self):
        items = self.container.items()
        items.sort(self.sort_by_time)
        self.container = {}
        for i in range(self.buffer_size/3,len(items)):
            self.container[items[i][0]] = {}
            self.container[items[i][0]].update(items[i][1])
        del items
        return
    
    def sort_by_time(self,a,b):
        if a[1]["time"] > b[1]["time"]:
            return 1
        elif a[1]["time"] < b[1]["time"]:
            return -1
        else:
            return 0

#########################################################################################################
class StatusBar:
    def __init__(self, parent, trigger=None):
        self.trigger = trigger
        # Create and pack the MessageBar.
        self._messagebar = Pmw.MessageBar(parent,
            entry_width = None,
            entry_relief='groove',
            labelpos = 'w',
            label_text = 'Status:')
        self._messagebar.pack(side = 'left', fill = 'x',
            expand = 1, padx = 10, pady = 10)
        self.show()

    def show(self, text='Ready', msgType='state'):
        self._messagebar.message(msgType, text)

#app = App()
#app.mainloop()

