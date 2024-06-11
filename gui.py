import os, sys,string, math, time
#import ouplib, dialogs, tools, reports, nodes, auxiliaries, distmatrixtype, Pmw
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog
import tkinter as Tkinter
import tkinter as Tkinter
from tkinter import filedialog as tkFileDialog
from random import randint

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
        self.open


