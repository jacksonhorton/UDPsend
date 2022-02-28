# udpsend.py
from logging import PlaceHolder
import socket
from tkinter import Tk, Button, LabelFrame, Label, Entry, BooleanVar, Checkbutton, Listbox, END, Toplevel, Text, Menu, IntVar
import os

from pyparsing import col


# Contains all settings so they can be accessed from any scope, good job[thumbs up]
class settings:
    # constants
    DEBUG_MODE = False
    DARK_MODE = True
    BG_COLOR = '#353535'
    DISABLED_COLOR = '#535353'
    TXT_COLOR = '#FFFFFF'
    ALPHA_AMT = 1.0     # a num between 1 and 0; how transparent window is
    # Default form values
    IP_DEFAULT = ''
    MSG_DEFAULT = ''
    PORT_DEFAULT = 5000
    USE_SAVES = False
    SAVES = []

    if DEBUG_MODE:
        PATH = './'
    else:
        PATH = os.path.join(os.path.expanduser('~'), '.udpsend')


def updateConf():
    # if config file exists
    if os.path.exists(os.path.join(settings.PATH, 'config.txt')):
        with open(os.path.join(settings.PATH, 'config.txt')) as conf:
            confEntries = [line.rstrip('\n').split('=', 1) for line in conf]
        # Checks if each line in config file contains a valid conf marker, or field that is able to be configured, such as "DARK_MODE"=True
        for conf in confEntries:
            if conf[0].upper() == 'DARK_MODE':
                if conf[1].upper() == 'TRUE':   # dark mode
                    settings.DARK_MODE = True
                    settings.BG_COLOR = '#353535'
                    settings.TXT_COLOR = '#FFFFFF'
                else:   # light mode
                    settings.DARK_MODE = False
                    settings.BG_COLOR = '#FFFFFF'
                    settings.TXT_COLOR = '#000000'
            # transparency factor, 1.0 is solid, 0.0 is transparent
            elif conf[0].upper() == 'ALPHA':
                try:    # in case it isn't a number
                    # only uses value if between 1.0 and 0.0
                    if float(conf[1]) >= 0 and float(conf[1]) <= 1:
                        settings.ALPHA_AMT = float(conf[1])
                except:
                    settings.ALPHA_AMT = 1.0
            elif conf[0].upper() == 'DEFAULT':  # default values(comma separated, no spaces)
                # splits default entry in conf file into ip, msg, and port
                defaults = conf[1].split(',', 2)
                settings.IP_DEFAULT = defaults[0]
                settings.MSG_DEFAULT = defaults[1]
                settings.PORT_DEFAULT = defaults[2]
            # use save/load functionality to use a library of values, like default values conf modifier
            elif conf[0].upper() == 'USE_SAVES':
                if conf[1].upper() == 'TRUE':
                    settings.USE_SAVES = True
                    # Makes sure the 'saves' folder exists inside the conf folder
                    if not os.path.isdir(os.path.join(settings.PATH, 'saves')):
                        # creates saves dir inside of conf folder
                        os.mkdir(os.path.join(settings.PATH, 'saves'))
                    filesInDir = [f for f in os.listdir(os.path.join(settings.PATH, 'saves')) if os.path.isfile(
                        os.path.join(os.path.join(settings.PATH, 'saves'), f))]
                    for file in filesInDir:
                        with open(os.path.join(settings.PATH, 'saves', file), 'r') as fileLine:
                            arg = fileLine.readline().split(',', 2)
                            settings.SAVES.append([file, arg])
                else:
                    settings.USE_SAVES = False

    else:   # config file or dir doesn't exist
        # if conf directory doesn't exits
        if not os.path.isdir(settings.PATH):
            # create dir
            os.mkdir(settings.PATH)
            # create blank config.txt file
            with open(os.path.join(settings.PATH, 'config.txt'), 'w') as init:
                init.write('')

        # if the config dir exists but the config.txt file does not
        elif not os.path.isfile(os.path.join(settings.PATH, 'config.txt')):
            # create blank config.txt file
            with open(os.path.join(settings.PATH, 'config.txt'), 'w') as init:
                init.write('')
    return


def udpCall():
    # gets ip address from frame
    ip = E1.get()
    # if the ip field is empty, default ip address to 127.0.0.1 to avoid errors
    if ip == '':
        ip = '127.0.0.1'

    # if the message field in the frame is still active(ON or OFF not checked), then use that field for the msg var
    if E2['state'] != 'disabled':
        msg = E2.get()
    # if on button is checked, use 'Power On' for msg
    elif CheckVar1.get():
        msg = 'Power On'
    # if off button is checked, use 'Power Off' for msg
    elif CheckVar2.get():
        msg = 'Power Off'

    # if port field in frame is empty, default to port 5000 to avoid errors.
    if E3.get() == '':
        port = 5000
    # otherwise use whatever port is in the field
    else:
        port = int(E3.get())

    print(f'>Sending "{msg}" to {ip}:{port}...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(bytes(msg, "utf-8"), (ip, port))
    return


# callback function when you press ON checkbox.
def onCheckClear():
    offCHECK.deselect()
    # Disable/reenable entry field
    if CheckVar1.get():
        # If the box is now checked, disable the entry field
        E2.config(state='disabled')
    else:
        # If the box is now unchecked, enable the entry field
        E2.config(state='normal')
    return

# callback function when you press OFF checkbox.
def offCheckClear():
    # Disable/reenable entry field
    onCHECK.deselect()
    if CheckVar2.get():
        # If the box is now checked, disable the entry field
        E2.config(state='disabled')
    else:
        # If the box is now unchecked, enable the entry field
        E2.config(state='normal')
    return


def loadSave():
    # try to selected item from listbox, if none selected, it will catch the error
    try:
        saveData = settings.SAVES[Load1.curselection()[0]][1]
    except:
        print('>Loading save data error: probably no save selected.')
        return
    # puts save data into its corresponding entry fields
    print(f'>Loading save data: {saveData}')
    E1.delete(0, END)
    E1.insert(END, saveData[0])
    E2.delete(0, END)
    if saveData[1] == 'Power On':   # ticks power on/off box if applicable, if not, puts in entry
        onCHECK.select()
        offCHECK.deselect()
    elif saveData[1] == 'Power Off':
        onCHECK.deselect()
        offCHECK.select()
    else:
        E2.insert(END, saveData[1])
    E3.delete(0, END)
    E3.insert(END, saveData[2])
    return


def saveSave():
    # we assume the conf dir and saves dir already exist because they should have been initialized during updateConf()
    # get entry values [ip, msg, port]
    if CheckVar1.get():  # if power on/off check box is checked, set msg to Power on/off insteas of entry field
        msg = 'Power On'
    elif CheckVar2.get():
        msg = 'Power Off'
    else:
        msg = E2.get()
    # puts data into a list
    dataToSave = [E1.get(), msg, E3.get()]

    # create a popup window to get the name of the save and verify the save data
    getSaveFrame = Toplevel(bg=settings.BG_COLOR)
    saveL1 = Label(getSaveFrame, text="Save Data",
                   bg=settings.BG_COLOR, fg=settings.TXT_COLOR)
    saveL1.configure(font=('', 20))
    saveL1.grid(row=1, column=1, columnspan=4, padx=10, pady=12)

    # Name entry field and label
    saveL2 = Label(getSaveFrame, text="Name:",
                   bg=settings.BG_COLOR, fg=settings.TXT_COLOR)
    saveL2.grid(row=2, column=1, padx=10, pady=10)
    saveE2 = Entry(getSaveFrame, bd=1, bg=settings.BG_COLOR,
                   fg=settings.TXT_COLOR)
    saveE2.grid(row=2, column=2, padx=10, pady=10, sticky='W', columnspan=3)

    # save data text field and label, not editable, just displays info to be stored.
    saveL3 = Label(getSaveFrame, text="Data:",
                   bg=settings.BG_COLOR, fg=settings.TXT_COLOR)
    saveL3.grid(row=3, column=1, padx=10, pady=10)
    saveT3 = Text(getSaveFrame, bg=settings.BG_COLOR,
                  fg=settings.TXT_COLOR, height=3, width=40)
    # prints dataToSave[] values in text box
    saveT3.insert(
        END, f'IP:   {dataToSave[0]}\nMSG:  {dataToSave[1]}\nPORT: {dataToSave[2]}')
    saveT3.grid(row=3, column=2, padx=10, pady=10, columnspan=3)

    # Button that saves the dataToSave[] and name to a file
    saveBTN = Button(getSaveFrame, text="Save", padx=4, pady=4,
                     command=lambda: saveDataToFile(saveE2.get(), dataToSave, getSaveFrame))
    saveBTN.grid(row=4, column=2, padx=8, pady=8)

    # cancel button, closes save window
    cancelBTN = Button(getSaveFrame, text="Cancel", padx=4,
                       pady=4, command=getSaveFrame.destroy)
    cancelBTN.grid(row=4, column=3, padx=8, pady=8)

    # Final configuration before window loop
    # makes it where when you hit enter, it is like the button was pressed
    getSaveFrame.bind('<Return>', lambda event: saveDataToFile(
        saveE2.get(), dataToSave, getSaveFrame))

    return


def saveDataToFile(name, dataToSave, frame):
    # opens a file with the given name and writes the save data to the *hopefully* loadable file
    with open(os.path.join(settings.PATH, 'saves', f'{name}'), 'w') as saveFile:
        saveFile.write(f'{dataToSave[0]},{dataToSave[1]},{dataToSave[2]}')
    print(f'>Saving: {dataToSave}')

    # update saves listbox
    settings.SAVES.clear()
    updateConf()
    Load1.delete(0, END)
    for save in settings.SAVES:
        Load1.insert(END, save[0])

    # closes window
    frame.destroy()


def saveConfigToFile(dark, saves, defaultValue, frame):
    # opens a file with the given name and writes the save data to the *hopefully* loadable file
    with open(os.path.join(settings.PATH, 'config.txt'), 'w') as saveFile:
        saveFile.write(f'DARK_MODE={dark}\nUSE_SAVES={saves}\nDEFAULT={defaultValue}')
    print(f'>Saving: DARK_MODE={dark}\nUSE_SAVES={saves}\nDEFAULT={defaultValue}')

    updateConf()

    # closes window
    frame.destroy()
    top.destroy()


def deleteSave():
    # if no save is selected, this catches error
    try:
        # gets name and position of currently selected item in listbox
        saveName = Load1.selection_get()
        id = Load1.get(0, END).index(saveName)
    except:
        save = None
        return
    
    # deletes the item in the listbox
    Load1.delete(id)
    # removes the file from the saves folder
    os.remove(os.path.join(settings.PATH, 'saves', saveName))
    return



def openSettings():
    settingsFrame = Toplevel(bg=settings.BG_COLOR)

    # dark mode checkbox
    darkModeCheckValue = BooleanVar()
    if settings.DARK_MODE:
        darkModeCheckValue.set(True)    # checked

    darkModeCheck = Checkbutton(settingsFrame, variable=darkModeCheckValue, text="Dark Mode",
                        bg=settings.BG_COLOR, fg=settings.TXT_COLOR, selectcolor=settings.BG_COLOR)
    darkModeCheck.grid(row=1, column=1, padx=10, pady=5)


    # use_saves checkbox
    useSavesCheckValue = BooleanVar()
    if settings.USE_SAVES:
        useSavesCheckValue.set(True)    # checked

    useSavesCheck = Checkbutton(settingsFrame, text="Use Saves", variable=useSavesCheckValue, 
                                bg=settings.BG_COLOR, fg=settings.TXT_COLOR, selectcolor=settings.BG_COLOR)
    useSavesCheck.grid(row=2, column=1, padx=10, pady=5)


    # def label
    defL = Label(settingsFrame, text="Default Values",
                 bg=settings.BG_COLOR, fg=settings.TXT_COLOR)
    defL.grid(row=3, column=1)
    # def ip entry
    defIpE = Entry(settingsFrame, bd=1, bg=settings.BG_COLOR, width=15,
                   fg=settings.TXT_COLOR, disabledbackground=settings.DISABLED_COLOR)
    defIpE.grid(row=3, column=2, padx=10, pady=5)
    # def msg entry
    defMsgE = Entry(settingsFrame, bd=1, bg=settings.BG_COLOR, width=15,
                   fg=settings.TXT_COLOR, disabledbackground=settings.DISABLED_COLOR)
    defMsgE.grid(row=4, column=2, padx=10, pady=5)
    # def port entry
    defPortE = Entry(settingsFrame, bd=1, bg=settings.BG_COLOR, width=15,
                   fg=settings.TXT_COLOR, disabledbackground=settings.DISABLED_COLOR)
    defPortE.grid(row=5, column=2, padx=10, pady=5)

    # sets default entry values to what is stored in settings class
    defIpE.insert(0, settings.IP_DEFAULT)
    defMsgE.insert(0, settings.MSG_DEFAULT)
    defPortE.insert(0, settings.PORT_DEFAULT)

    # Button that saves the dataToSave[] and name to a file
    saveConfBTN = Button(settingsFrame, text="Save and Close", padx=4, pady=4,
                     command=lambda: saveConfigToFile(darkModeCheckValue.get(),
                                                      useSavesCheckValue.get(),
                                                      f'{defIpE.get()},{defMsgE.get()},{defPortE.get()}',
                                                    settingsFrame)
                     )
    saveConfBTN.grid(row=6, column=1, padx=8, pady=8)

    # cancel button, closes save window
    cancelBTN = Button(settingsFrame, text="Cancel", padx=4,
                       pady=4, command=settingsFrame.destroy)
    cancelBTN.grid(row=6, column=2, padx=8, pady=8)


    settingsFrame.mainloop()


# Does pre-window loading stuff
updateConf()


# initialized window with title, bg color and makes it non-resizeable
top = Tk()
# makes it where when you hit enter, it is like the button was pressed
top.bind('<Return>', lambda event: udpCall())
top.title("UDP Sender")
top.configure(background=settings.BG_COLOR)
top.resizable(False, False)
top.attributes('-alpha', settings.ALPHA_AMT)
# top.attributes('-topmost', 1)


# a smaller frame containing the ip, msg, and port tk elements
entryFrame = LabelFrame(top, bg=settings.BG_COLOR)
entryFrame.grid(row=1, column=1, columnspan=4, padx=7, pady=7)


# IP address label and entry
L1 = Label(entryFrame, text="IP Address",
           bg=settings.BG_COLOR, fg=settings.TXT_COLOR)
L1.grid(row=0, column=0, padx=10, pady=10)
E1 = Entry(entryFrame, bd=1, bg=settings.BG_COLOR, fg=settings.TXT_COLOR)
E1.insert(0, settings.IP_DEFAULT)  # ip entry default value
E1.grid(row=0, column=1, padx=10, pady=10, columnspan=4)


# Message label and entry
L2 = Label(entryFrame, text="Message",
           bg=settings.BG_COLOR, fg=settings.TXT_COLOR)
L2.grid(row=1, column=0, padx=10, pady=10)
E2 = Entry(entryFrame, bd=1, bg=settings.BG_COLOR,
           fg=settings.TXT_COLOR, disabledbackground=settings.DISABLED_COLOR)
E2.insert(0, settings.MSG_DEFAULT)  # msg entry default value
E2.grid(row=1, column=1, padx=10, pady=10, columnspan=4)


# Stores the values of the ON and OFF checkboxes as True or False
CheckVar1 = BooleanVar()
CheckVar2 = BooleanVar()

# On and Off checkboxes for message. One of these can be used instead of the message entry field
onCHECK = Checkbutton(entryFrame, text="On", variable=CheckVar1, onvalue=True, offvalue=False,
                      bg=settings.BG_COLOR, fg=settings.TXT_COLOR, selectcolor=settings.BG_COLOR, command=lambda: onCheckClear())
onCHECK.grid(row=2, column=1)
offCHECK = Checkbutton(entryFrame, text="Off", variable=CheckVar2, onvalue=True, offvalue=False,
                       bg=settings.BG_COLOR, fg=settings.TXT_COLOR, selectcolor=settings.BG_COLOR, command=lambda: offCheckClear())
offCHECK.grid(row=2, column=2)

# Message label and entry
L3 = Label(entryFrame, text="Port",
           bg=settings.BG_COLOR, fg=settings.TXT_COLOR)
L3.grid(row=3, column=0, padx=10, pady=10)
E3 = Entry(entryFrame, bd=1, bg=settings.BG_COLOR, fg=settings.TXT_COLOR)
E3.insert(0, settings.PORT_DEFAULT)  # port entry default value
E3.grid(row=3, column=1, padx=10, pady=10, columnspan=4)

# Send button with callback to udpCall(). Used to send udp to info given in the frame.
sendBTN = Button(top, text="Send", padx=4, pady=4, command=lambda: udpCall())
sendBTN.grid(row=2, column=2, padx=8, pady=8)


if settings.USE_SAVES:

    # Frame for load saves menu
    loadFrame = LabelFrame(top, bg=settings.BG_COLOR)
    loadFrame.grid(row=1, column=5, columnspan=2, padx=10, pady=10)
    
    # binds backspace key to deleteSave function
    top.bind('<BackSpace>', lambda event: deleteSave())

    # Load Save ListBox. Only appears if the correct modifier is in the config file.
    Load1 = Listbox(loadFrame, bg=settings.BG_COLOR,
                    selectmode='single', fg=settings.TXT_COLOR, height=8)
    # Load1.insert(END, *settings.SAVES)
    for save in settings.SAVES:
        Load1.insert(END, save[0])
    Load1.grid(row=1, column=1)


    # Load save button
    loadBTN = Button(top, text="Load", padx=4, pady=4,
                     command=lambda: loadSave())
    loadBTN.grid(row=2, column=5, padx=8, pady=8)

    # Save save button, a little confusing, but it's ok
    saveBTN = Button(top, text="Save", padx=4, pady=4, command=lambda: saveSave())
    saveBTN.grid(row=2, column=6, padx=8, pady=8)


# menubar initialization
menuBar = Menu(top)
fileMenu = Menu(menuBar, tearoff=False)

# add commands to fileMenu
fileMenu.add_command(label="Settings", command=lambda: openSettings())

# adds all submenus to menu bar
menuBar.add_cascade(label="File", menu=fileMenu)

# starts window loop
top.config(menu=menuBar)
top.mainloop()
