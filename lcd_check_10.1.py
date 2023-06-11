from cgitb import enable
from faulthandler import disable
import time
from tkinter import *
from turtle import update
from PIL import Image, ImageTk
from screeninfo import get_monitors

def checkMonitor():
    # we assume this system only has 2 monitors
    counter = 0
    for monitor in get_monitors():
        counter += 1
        if monitor.is_primary:
            global primaryDisplay_Monitor            
            primaryDisplay_Monitor = StructoMonitors()
            primaryDisplay_Monitor.resolution_width = monitor.width
            primaryDisplay_Monitor.resolution_height = monitor.height
            primaryDisplay_Monitor.coordinator_x = monitor.x
            primaryDisplay_Monitor.coordinator_y = monitor.y
            primaryDisplay_Monitor.isPrimaryScreen = True
        elif monitor.width == 1640:
            # only consider LCD if width resolution is 1640 (1640x2880)
            global secondDisplay_LCD
            secondDisplay_LCD = StructoMonitors()            
            secondDisplay_LCD.resolution_width = monitor.width
            secondDisplay_LCD.resolution_height = monitor.height
            secondDisplay_LCD.coordinator_x = monitor.x
            secondDisplay_LCD.coordinator_y = monitor.y
            secondDisplay_LCD.isPrimaryScreen = False    
    return counter

class StructoMonitors:
    resolution_width=0
    resolution_height=0
    coordinator_x=0
    coordinator_y=0
    isPrimaryScreen=False

def createMainWindow():
    #print("enter createMainWindow")
    global root
    root = Tk()
    root.title("Structo - LCD check station - 10.1 inch LCD")

    createUIMainWindow()

    # calculate coordinate and resolution of main app
    mainAppWidth = int(primaryDisplay_Monitor.resolution_width/2)
    mainAppHeight = int(primaryDisplay_Monitor.resolution_height/2)
    mainAppCoord_X = primaryDisplay_Monitor.coordinator_x + int(mainAppWidth/2)
    mainAppCoord_Y = primaryDisplay_Monitor.coordinator_y + int(mainAppHeight/2)
    stringGeometryPrimaryDisplay = str(500) + "x" + str(300) + "+" + str(mainAppCoord_X) + "+" + str(mainAppCoord_Y)

    # set main app geometry
    root.geometry(stringGeometryPrimaryDisplay)
    #print("exit createMainWindow")

def createUIMainWindow():
    #print("enter createUIMainWindow")

    # define logo
    #logo_Structo = ImageTk.PhotoImage(Image.open('icon-grey-64.png'))
    #label_logo = Label(image=logo_Structo)
    #label_logo.grid(row=0, column=0, rowspan=2)
    #label_logo.pack()

    # define main title
    label_mainTitle = Label(root, text="Structo - LCD check for 10.1\" LCD", fg='blue', font=("Arial",16))
    #label_mainTitle.grid(row=0, column=1)
    label_mainTitle.pack()

    # define version
    label_version = Label(root, text="v1.0")
    #label_version.grid(row=0,column=3)
    label_version.pack()

    # define status
    #label_status = Label(root, text="idle")
    global status_text
    status_text = StringVar()
    label_status = Label(root, textvariable=status_text, fg='yellow', bg='green', font=("Arial", 14))
    status_text.set("Status: idle")
    #label_status.grid(row=1,column=1,columnspan=2)
    label_status.pack(pady=20)
    
    # define button
    global btn_Start
    btn_Start = Button(root, text="Start", command=startLCDCheck)
    #btn_Start.grid(row=2,columnspan=3)
    btn_Start.pack(padx=20, pady=20, ipadx=40, ipady=20)

    #print("exit createUIMainWindow")

def startLCDCheck():
    # check monitors
    btn_Start.config(state="disabled")
    status_text.set("Status: Starting")
    totalDisplay = checkMonitor()
    print("Start LCD check_ number of detected monitors=" + str(totalDisplay))

    if totalDisplay == 1:
        status_text.set("Status: no LCD detected")
        print("no LCD detected")
        return
    #global lcd_image
    top = Toplevel()    
    stringGeometryLCDDisplay = str(secondDisplay_LCD.resolution_width) + "x" + str(secondDisplay_LCD.resolution_height) + "+" + str(secondDisplay_LCD.coordinator_x) + "+" + str(secondDisplay_LCD.coordinator_y)
    print("positioning of LCD display: " + stringGeometryLCDDisplay)
    top.geometry(stringGeometryLCDDisplay)    
    top.wm_attributes('-fullscreen','True')

    for i in range(1,5):        
        #print("inside loop i=" + str(i))
        image_filename = 'frame' + str(i) + '.png'
        print('image filename=' + image_filename)
        status_text.set("Status: displaying frame " + str(i))
        lcd_image = ImageTk.PhotoImage(Image.open(image_filename))        
        my_label = Label(top, image=lcd_image)
        my_label.pack()        
        top.update()
        #print("before sleep")
        # remain the image for 4 seconds before switching to a new image
        time.sleep(4)
        my_label.pack_forget()
        #print("after sleep")
        # end for loop
    top.destroy()
    status_text.set("Status: completed !")
    btn_Start.config(state="active")
    print("completed LCD checks")    

if __name__ == "__main__":
    #print("enter main function")   

    # check monitors
    totalDisplay = checkMonitor()
    print("Application started, number of detected monitors=" + str(totalDisplay))

    # display main window app on primary screen
    createMainWindow()

    # add UI components
    #createUIMainWindow()

    # run UI
    root.mainloop()

    #print("exit main function")
    exit(0)
#------------------------- END -------------------------