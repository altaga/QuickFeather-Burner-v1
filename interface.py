from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pathlib
import subprocess
import sys
import glob
import serial

path = ""
script_path = str(pathlib.Path(__file__).parent.absolute()) + \
                  "/TinyFPGA-Programmer-Application/tinyfpga-programmer-gui.py"
serial_array = []
combobox = ""


def browseFiles():
    global path
    path = filedialog.askopenfilename(
        initialdir=str(pathlib.Path(__file__).parent.absolute()),
                                      title = "Select a File",
                                      filetypes = (("Text files",
                                                  "*.bin*"),
                                                 ("all files",
                                                  "*.*")))

    label_file_explorer.configure(text = "File path:\n"+path)
    print("Browse Correct")

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports=['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports=glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports=glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result=[]
    for port in ports:
        try:
            s=serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def program():
    if(path == ""):
        return
    command=["python3", script_path, "--port",
        combobox.get(), "--m4", path, "--mode", "m4"]
    T.insert(END, subprocess.run(
        command, stdout=subprocess.PIPE).stdout.decode())
    print("Programming Complete")

def updateSerial():
    global serial_array
    serial_array=serial_ports()
    combobox["values"]=serial_array
    if(len(serial_array) > 0):
        combobox.current(0)
    else:
        combobox.set('No Ports')
    print("Refresh Correct")

def install_dep():
    command=["git", "clone", "--recursive","https://github.com/QuickLogic-Corp/TinyFPGA-Programmer-Application.git"]
    result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode()
    T.insert(END, result)
    command=["pip3", "install", "tinyfpgab"]
    result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode()
    T.insert(END, result)
    print("Install Correct")


serial_array=serial_ports()
window=Tk()
window.geometry('800x720')  # anchura x altura

# window.configure(bg = 'beige')
window.title('QuickFeather Programmer')

label_file_explorer= Label(window, text = "File path:", width = 0,
      height=4, fg="blue")

T=Text(window, height=20, width=100)

myFont = ("Arial", 17)

button1 = Button(window, width=20, height=2, text="Browse Bin File",
       command=browseFiles,font=myFont)

button2 = Button(window, width=20, height=2, text="Program",
       command=program,font=myFont)

button3 = Button(window, width=20, height=2, text="Refresh Ports",
       command=updateSerial,font=myFont)

button4 = Button(window, width=20, height=2, text="Install Dep",
       command=install_dep,font=myFont)

combobox = ttk.Combobox(window, values=serial_array,font=myFont)

if(len(serial_array) > 0):
    combobox.current(0)
else:
    combobox.set('No Ports')

label_file_explorer.grid(column=1, row=1)
combobox.grid(column=1, row=2)
T.grid(column=1, row=3)
button1.grid(column=1, row=4)
button2.grid(column=1, row=5)
button3.grid(column=1, row=6)
button4.grid(column=1, row=7)

window.mainloop()
