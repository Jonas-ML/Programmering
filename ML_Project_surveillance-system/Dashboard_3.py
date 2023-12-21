import cv2
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import paho.mqtt.client as mqtt
# UKOMMENTER MQTT KODE HVIS BROKER OPSAT - INKLUSIV LOOP.START NEDE I BUNDEN
""""
def subscribe(klient, userdata, flags, rc):
    klient.subscribe(topic)
    print("Forbundet")

def on_message(klient, userdata, msg):
    besked = str(msg.payload)
    if "open" in besked:
        opdater("åben")     
    elif "closed" in besked:
        opdater("lukket")

def taendt_mode():
    state = True
    klient.publish("alarm", state)

def slukket_mode():
    state = False
    klient.publish("alarm", state)

def opdater(dørstatus):
    label_status.config(text=f"Døren er {dørstatus}")

state = bool
topic = "sensor"


#Paho MQTT
klient = mqtt.Client()

#Her sættes kodeord osv. til, hvis dette er valgt i projektet
#klient.username_pw_set(username="gruppe3", password="gruppe3")

klient.on_connect = subscribe
klient.on_message = on_message

#Forbinder til broker med IP og standard port uden SSL. Med SSL (port=8883)
klient.connect("192.168.0.193", port=1883)
"""

# Credentials til rtp
rtp_username = 'jonasml'
rtp_password = 'jonasml0104'
rtp_endpoint = 'stream1'
rtp_ip = '192.168.0.185:554'


# Cap objekter
cap = None
cap1 = None


def start_stream():
    global cap, cap1

    cap = cv2.VideoCapture(f'rtsp://{rtp_username}:{rtp_password}@{rtp_ip}/{rtp_endpoint}')
    cap1 = cv2.VideoCapture(0)
    #frame og ret variabler bruges til at sørge for at cap.read() virker
    def update_frame():
        global frame, ret, frame1, ret1

        # Update frame for kamera 1
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized_frame = cv2.resize(frame, (560, 340))
            image = Image.fromarray(resized_frame)
            imgtk = ImageTk.PhotoImage(image=image)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        
        # Update frame for kamera 2
        ret1, frame1 = cap1.read()
        if ret1:
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            resized_frame1 = cv2.resize(frame1, (560, 340))
            image1 = Image.fromarray(resized_frame1)
            imgtk1 = ImageTk.PhotoImage(image=image1)
            label1.imgtk = imgtk1
            label1.configure(image=imgtk1)

        # Frame update tid i ms
        label.after(10, update_frame)

    # Start updating frames
    update_frame()

# Releaser cap objekter og tømmer frames i GUI
def stop_stream():
    global cap, cap1
    if cap:
        cap.release()
        label.config(image='')
    if cap1:
        cap1.release()
        label1.config(image='')

# Funktion til at oprette og tjekke user_credentials
file_name = 'pass.txt'
# Billig måde at undgå direkte file path til pass.txt - Den opretter pass.txt i samme folder som scriptet køres i
file_path = os.path.join(os.path.dirname(__file__), file_name)

def check_login():
    #Laver en ny pass.txt fil hvis denne ikke allerede findes
    if not os.path.exists(file_path):
        messagebox.showinfo(title='New Login', message='New User Detected')
        with open(file_path, 'w') as file:
            userid = entry_user.get()
            password = entry_PW.get()
            file.write(f"{userid}:{password}")
            file.close()
            messagebox.showinfo(title='New Login', message='New login created')
    else:
        #Tjekker den eksisterende
        userid = entry_user.get()
        password = entry_PW.get()
        with open(file_path, 'r') as file:
            for line in file:
                stored_userid, stored_password = line.strip().split(':')
                if userid == stored_userid and password == stored_password:
                    messagebox.showinfo(title="login", message="Login successful")
                    tab_state(True)
                    return
                else:
                    messagebox.showinfo(title="Login", message="Login Failed")

# sætter tabs til låst/ulåst - starter ved 1 da den ikke skal låse loginsiden
def tab_state(enabled):
    tabs = tabsystem.tabs()
    start_index = 1
    for tab_id in tabs[start_index:]:
        tabsystem.tab(tab_id, state="normal" if enabled else "disabled")

# Root window
root = Tk()
root.title("Dashboard")
root.configure(background="white")
root.minsize(200, 200)
root.maxsize(1920, 1080)
root.geometry("1200x400+50+50")
tabsystem = ttk.Notebook(root)




# Tab 1 - Login
tab1 = Frame(tabsystem)
tabsystem.add(tab1, text="Login")
tabsystem.pack(expand=1, fill="both")
#Labels og entries til login - entry er input kasser.
label_user = Label(tab1, text="UserID")
label_user.grid(column=1, row=1, padx=40, pady=40)
entry_user = ttk.Entry(tab1)
entry_user.grid(column=2, row=1, padx=40, pady=40)

label_info = Label(tab1, text='If this is your first login. Your credentials will be your new custom login')
label_info.grid(column=5, row=1, padx=40, pady=40)

label_PW = Label(tab1, text="Password")
label_PW.grid(column=1, row=2, padx=40, pady=40)
entry_PW = ttk.Entry(tab1, show="*")
entry_PW.grid(column=2, row=2, padx=40, pady=40)

# Login knapper
login_button = ttk.Button(tab1, text="Login", command=check_login)
login_button.grid(column=1)



# Tab 2 - Cams
tab2 = Frame(tabsystem)
tabsystem.add(tab2, text="Cam-feed")
tabsystem.pack(expand=1, fill="both")

# inner frame til kamera 1
inner_frame = Frame(tab2, bg="black")
inner_frame.place(x=50, y=50)
label = Label(inner_frame)
label.pack(padx=0, pady=0)

# inner frame til kamera 2
inner_frame1 = Frame(tab2, bg="black")
inner_frame1.place(x=920, y=50) 
label1 = Label(inner_frame1)
label1.pack(padx=0, pady=0)

# Knapper til streams
start_button = ttk.Button(tab2, text="Start Stream", command=start_stream)
start_button.pack()
stop_button = ttk.Button(tab2, text="Stop Stream", command=stop_stream)
stop_button.pack()



# Tab 3 - Overview
tab3 = Frame(tabsystem)
tabsystem.add(tab3, text="Overview")
tabsystem.pack(expand=1, fill="both")

#Sluk facial label
label_mode1 = Label(tab3, text="Sluk facial-verification")
label_mode1.place(x=150, y=50)

# Tænde facial label
label_mode3 = Label(tab3, text="Tænd facial-verification")
label_mode3.place(x=150, y=150)

label_status = Label(tab3,text=f"Venter på status fra bagdør", bg='#fff', fg='#f00')
label_status.place(x=600, y=100)  

# Funktioner til tænd/sluk

def taendt_mode():
    state = True
    klient.publish("alarm", state)

def slukket_mode():
    state = False
    klient.publish("alarm", state)

# Knapper til at tænd/sluk
slukket_button = ttk.Button(tab3, text="Sluk", command=slukket_mode)
slukket_button.place(x=50, y=50)

taend_button = ttk.Button(tab3, text="Tænd", command=taendt_mode)
taend_button.place(x=50, y=150)
##########################################################################


# Delayed kald til at disable tabs. Man skal vente på notebook er initialiseret før det virker
root.after(100, tab_state(False)) # COMMENT/UNCOMMENT FOR AT FÅ LOGIN TIL AT DEACTIVATE/ACTIVATE #

#klient.loop_start()

root.mainloop()