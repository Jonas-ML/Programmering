import mariadb
import datetime
import mysql.connector
from time import sleep
import tkinter as tk
from tkinter import ttk
from tkinter import *
from sshtunnel import SSHTunnelForwarder
import re

ssh_host = '79.171.148.163'
ssh_port = 22
ssh_user = 'Benjamin'
ssh_pw = '@gruppe3'

db_host = '127.0.0.1'
db_port = 3306
db_user = 'root'
db_password = 'gruppe3'
db_database = 'test2'

with SSHTunnelForwarder(
                        (ssh_host, ssh_port),
                        ssh_username = ssh_user,
                        ssh_password = ssh_pw,
                        remote_bind_address=('127.0.0.1', db_port)
                        ) as tunnel:
    

    conn = mysql.connector.connect( 
                        host = db_host,
                        port = tunnel.local_bind_port,
                        user = db_user, 
                        password = db_password, 
                        database = db_database)

    cur = conn.cursor()



    #tilføjer elev til studerende
    def addElev():
        UID = input1.get()
        Navn = input2.get()
        Klasse = input3.get()
        cur.execute("INSERT INTO studerende (SID, Navn, Klasse) VALUES (%s, %s, %s)", (UID, Navn, Klasse))
        conn.commit()
        

    #sletter elev fra studerende
    def sletElev():
        UID = input4.get()
        cur.execute("DELETE FROM studerende WHERE SID = %s",(UID,))
        conn.commit()
        

    #giver en oversigt over alle klasser i databasen
    def klasseOversigt():
        cur.execute("SELECT Klasse FROM studerende")
        klasser = cur.fetchall()
        for x in set(klasser):
            klas = x[0]
            klasseOver.append(klas)
        tekst14.config(text = set(klasseOver))
            
        
            
    #Slette/tilføje klasse table
    def opretKlasse():
        klasseNavn = input5.get()
        cur.execute("CREATE TABLE IF NOT EXISTS {} (SID INTEGER UNIQUE, Fravær INT, Dato DATE DEFAULT CURRENT_TIMESTAMP())".format(klasseNavn))
        conn.commit()

    def opretSkema():
        klasseNavn = input13.get()
        cur.execute("CREATE TABLE IF NOT EXISTS {} (Dato DATE DEFAULT CURRENT_TIMESTAMP(), Fag TEXT)".format(klasseNavn))
        conn.commit()
        
    #Slet klasse table
    def sletTable():        
        tableSlet = input6.get()
        if tableSlet != "studerende":
            cur.execute("DROP TABLE {}".format(tableSlet))
            conn.commit()
        

    def indiFravær():
        x = input9.get()
        cur.execute("SELECT klasse FROM studerende WHERE sid = %s", (x,))
        klasse = cur.fetchone()[0]
        skemaNavn = "skema" + klasse
        cur.execute("SELECT start FROM studerende WHERE sid = %s", (x,))
        start = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM {} WHERE Dato BETWEEN %s AND %s".format(skemaNavn),(start, datetime.date.today()))
        resultat1 = cur.fetchone()[0]
        cur.execute("SELECT SUM(fm) FROM {} WHERE sid = %s AND dato BETWEEN %s AND %s".format(klasse), (x,start,datetime.date.today()))
        resultat2 = cur.fetchone()[0]
        if resultat2 == None:
            resultat2 = 0
        cur.execute("SELECT navn FROM studerende WHERE sid =%s", (x,))
        navn = cur.fetchone()[0]
        total = ((resultat1 - resultat2) / resultat1) * 100
        tekst16.config(text=f"{navn} har {total:.2f}% fravær")

    def klasseFravær():
        klasFravær = []
        hvilkentabel = input10.get()
    # Hent studerende fra den valgte klasse.
        klasse = "SELECT sid, navn FROM studerende WHERE klasse = %s"
        skemaNavn = "skema" + hvilkentabel
        cur.execute(klasse,(hvilkentabel,))
        studerende = cur.fetchall()
        # Gennemgå hver studerende.
        for studerende_data in studerende:
            sid = studerende_data[0]
            navn = studerende_data[1]
            #Finder start dato på elev
            cur.execute("SELECT start FROM studerende WHERE sid = %s", (sid,))
            start = cur.fetchone()[0]
    #
      
    # Hent antallet af rækker i skemaitt indtil dags dato.
            cur.execute("SELECT COUNT(*) FROM {} WHERE dato BETWEEN %s AND %s".format(skemaNavn), (start, datetime.date.today()))
            resultat1 = cur.fetchone()[0]
    # Hent summen af tilstedeværelse for den studerende.
            cur.execute("SELECT SUM(fm) FROM {} WHERE sid = %s AND dato BETWEEN %s AND %s".format(hvilkentabel), (sid,start,datetime.date.today()))
            resultat2 = cur.fetchone()[0]
    # Beregn fraværsprocenten
            total = ((resultat1 - resultat2)/ resultat1)*100
            klasFravær.append(f"{navn} har{total:.2f}% fravær\n")
    # Udskriv resultatet
        tekst19.config(text = klasFravær)

            

    def redigerFravær():
        uid = input11.get()
        cur.execute("SELECT Klasse FROM studerende WHERE SID=%s",(uid,))
        klasse = cur.fetchone()
        dato = input12.get()
        cur.execute("SELECT fm from {} WHERE dato=%s AND SID=%s".format(klasse[0]),(dato,uid))
        fravær = cur.fetchone()
        if fravær == None:
            cur.execute("INSERT INTO {} (Dato, SID, fm) VALUES (%s, %s, %s)".format(klasse[0]),(dato, uid, 1))
        elif fravær[0] == 1:
            cur.execute("DELETE FROM {} WHERE dato=%s AND SID=%s".format(klasse[0]),(dato,uid))
        conn.commit()
        

    def sletDag():
        klasse = input7.get()
        skemaNavn = "skema" + klasse
        dato = input8.get()
        cur.execute("DELETE FROM {} WHERE Dato=%s".format(skemaNavn),(dato,))
        conn.commit()

    #Vindue til GUI
    window = tk.Tk()

    #Størrelse på vindue
    window.geometry("800x800")

    #Titel på vindue
    window.title("Admin Interface")

    #Sørger for man kan lave tabs
    tabs = ttk.Notebook(window)

    #Opretter tabs
    tab1 = ttk.Frame(tabs)
    tab2 = ttk.Frame(tabs)
    tab3 = ttk.Frame(tabs)

    #Sætter tabs i GUI
    tabs.add(tab1, text="Rediger elever")
    tabs.add(tab2, text="Rediger klasse")
    tabs.add(tab3, text="Rediger i fravær")
    tabs.pack(expand = 1, fill = "both")

    #Tekst til tilføj elev til database
    tekst1 = Label(tab1, text = "Tilføj elev til database").grid(column = 0, row = 0)
    tekst2 = Label(tab1, text = "Skriv SID på elev her: ").grid(column = 0, row = 1)
    tekst3 = Label(tab1, text = "Skriv navn på elev her: ").grid(column = 0, row = 2)
    tekst4 = Label(tab1, text = "Skriv klasse på elev her: ").grid(column = 0, row = 3)

    #Tekst til at slette elev fra database
    tekst5 = Label(tab1, text = "Slet elev fra database").grid(column = 0, row = 6)
    tekst6 = Label(tab1, text = "Skriv SID på elev, du vil slette: ").grid(column = 0, row = 7)

    #Tekst til tilføj ny klasse
    tekst7 = Label(tab2, text = "Tilføj ny klasse").grid(column = 0, row = 0)
    tekst8 = Label(tab2, text = "Skriv navn på ny klasse på 3 bogstaver, f.eks. dat eller itt: ").grid(column = 0, row = 1)
    tekst23 = Label(tab2, text = "Opret nyt skema").grid(column = 0, row = 4)
    tekst24 = Label(tab2, text = "Skriv skema + navn på klasse, f.eks. skemaitt eller skemadat: ").grid(column = 0, row = 5)

    #Tekst til slet klasse
    tekst9 = Label(tab2, text = "Slet table fra database").grid(column=0,row=7)
    tekst10 = Label(tab2, text = "Skriv navn på table, der skal slettes: ").grid(column=0,row=8)

    #Tekst til slet skemadag
    tekst11 = Label(tab2, text = "Slet skemadag fra skema table").grid(column=0,row=10)
    tekst12 = Label(tab2, text = "Skriv navn på klasse, der skal have slettet dag: ").grid(column=0,row=11)
    tekst13 = Label(tab2, text="Skriv dato på skemadag, der skal slettes (YYYY-MM-DD): ").grid(column=0,row=12)

    #Tekst til at se oversigt over klasser
    tekst14 = Label(tab2,text = " ")
    tekst14.grid(column=1,row=17)

    #Tekst til at se individuel fravær
    tekst15 = Label(tab3, text="Se fravær på én elev").grid(column=0,row=0)
    tekst15 = Label(tab3, text="Skriv UID på elev, du vil have fravær for: ").grid(column=0,row=1)
    tekst16 = Label(tab3, text=" ")
    tekst16.grid(column=1,row=2)

    #Tekst til at se klassefravær
    tekst17 = Label(tab3, text = "Her kan du se en hel klasses fravær").grid(column=0,row=4)
    tekst18 = Label(tab3, text = "Skriv navn på klasse, du vil have fravær for: ").grid(column=0,row=5)
    tekst19 = Label(tab3, text = " " )
    tekst19.grid(column=0, row=6)
    tekst20 = Label(tab3, text = "Rediger i fravær").grid(column=0,row=7)
    tekst21 = Label(tab3, text = "Skriv UID på elev, der skal have ændret fravær: ").grid(column=0,row=8)
    tekst22 = Label(tab3, text = "Skriv dato på dag, der skal ændres (YYYY-MM-DD): ").grid(column=0,row=9)

    #Tomme strenge der bliver indsat for at få GUI til at se lidt mere overskuelig ud (indsætter tomme rækker, så det hele ikke står i en lang smøre)
    teksttom1 = Label(tab2, text=" ").grid(column=0,row=14)
    teksttom2 = Label(tab2, text=" ").grid(column=0,row=15)
    teksttom3 = Label(tab2, text=" ").grid(column=0,row=16)

    #Lister
    klasseOver = []
 
    #Tab 1 user inputs
    input1 = tk.Entry(tab1)
    input1.grid(column=1,row = 1)

    input2 = tk.Entry(tab1)
    input2.grid(column=1,row = 2)

    input3 = tk.Entry(tab1)
    input3.grid(column=1,row = 3)

    input4 = tk.Entry(tab1)
    input4.grid(column=1, row = 7)

    #Tab 2 user inputs
    input5 = tk.Entry(tab2)
    input5.grid(column=1, row=1)

    input6 = tk.Entry(tab2)
    input6.grid(column=1,row=8)

    input7 = tk.Entry(tab2)
    input7.grid(column=1,row=11)

    input8 = tk.Entry(tab2)
    input8.grid(column=1,row=12)

    input13 = tk.Entry(tab2)
    input13.grid(column=1,row=5)

        #Tab 3 user inputs
    input9 = tk.Entry(tab3)
    input9.grid(column=1, row=1)

    input10 = tk.Entry(tab3)
    input10.grid(column=1, row=5)

    input11 = tk.Entry(tab3)
    input11.grid(column=1, row=8)

    input12 = tk.Entry(tab3)
    input12.grid(column=1, row=9)

    #Knapper til tab 1
    knap1 = Button(tab1, text="Indsæt ny elev til database", command=addElev).grid(column = 1, row = 4)
    knap2 = Button(tab1, text="Slet elev fra database", command=sletElev).grid(column=1,row=8)

    #Knapper til tab 2
    knap3 = Button(tab2, text="Tilføj ny klasse", command=opretKlasse).grid(column=1, row=3)
    knap4 = Button(tab2, text="Slet table", command=sletTable).grid(column=1,row=9)
    knap5 = Button(tab2, text="Slet skemadag", command=sletDag).grid(column=1,row=13)
    knap6 = Button(tab2, text="Tryk her for at se klasse oversigt", command = klasseOversigt).grid(column=1,row=16)
    knap10 = Button(tab2, text="Opret skema", command = opretSkema).grid(column=1,row=6)

    #Knapper til tab 3
    knap7 = Button(tab3, text = "Se fravær", command=indiFravær).grid(column=1,row=3)
    knap8 = Button(tab3, text = "Se fravær for klasse", command=klasseFravær).grid(column=1,row=6)
    knap9 = Button(tab3, text = "Rediger fravær", command= redigerFravær).grid(column=1,row=10)

    #Kører programmet til man lukker det
    window.mainloop()