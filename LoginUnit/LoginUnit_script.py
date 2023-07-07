from time import sleep
from mfrc522 import SimpleMFRC522
from datetime import date
import mysql.connector
from sshtunnel import SSHTunnelForwarder
from RPLCD.i2c import CharLCD

reader = SimpleMFRC522()

# SSH tunnel konfiguration
ssh_host = '79.171.148.163'  
ssh_port = 22  
ssh_user = 'kim' 
ssh_password = '@gruppe3' 

# MariaDB konfiguration
db_host = '127.0.0.1'  
db_port = 3306  
db_user = 'kim'  
db_password = 'gruppe3' 
db_database = 'test2' 

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_password,
        remote_bind_address=('127.0.0.1', db_port)
) as tunnel:
    conn = mysql.connector.connect(
        host=db_host,
        port=tunnel.local_bind_port,
        user=db_user,
        password=db_password,
        database=db_database
    )
    

    while True:
        try:
            lcd.write_string("Placer tag")
            _, sid = reader.read()  # Ignorerer uid på RFID-tag ved at bruge underscore, da dette vil være pladsspild i databasen.
            sleep(2)

            cur = conn.cursor()

            # Henter klasse for den studerende baseret på sid
            cur.execute("SELECT klasse FROM studerende WHERE sid = %s", (sid,))
            klasse_result = cur.fetchone()
            

            if klasse_result:
                # Hvis der er en klasse tilknyttet til den pågældende studerende
                klasse = klasse_result[0]
                skemaNavn = "skema" + klasse
                dato = date.today()
                cur.execute("SELECT dato FROM {} WHERE dato = %s".format(skemaNavn),(dato,))
                result = cur.fetchone()
                if result:
                    # Hvis der er et resultat, betyder det, at der er undervisning i dag
                    fm = 1  # Sætter fm til 1, hvilket betyder fremmøde

                    # Tjekker om rækken allerede eksisterer i tabellen
                    cur.execute("SELECT sid FROM {} WHERE dato = %s AND sid = %s".format(klasse) ,(dato,sid))
                    existing_row = cur.fetchone()

                    if existing_row:
                        # Hvis rækken allerede eksisterer
                        lcd.clear()
                        lcd.write_string("OK tjek.")
                        sleep(3)
                        lcd.clear()

                    else:
                        # Hvis rækken ikke eksisterer, indsættes data i tabellen
                        cur.execute("INSERT INTO {} (dato, sid, fm) VALUES (%s, %s, %s)".format(klasse),(dato, sid, fm))
                        conn.commit()
                        lcd.clear()
                        lcd.write_string("Indtjekning ok.")
                        sleep(3)
                        lcd.clear()

                else:
                    # Hvis den studerende forsøger at tjekke ind, når der ikke er undervisning ifølge skemaet.
                    lcd.clear()
                    lcd.write_string("Du har ikke undervisning i dag.")
                    sleep(3)
                    lcd.clear()

            else:
                # Hvis der ikke er nogen klasse tilknyttet til den pågældende studerende
                lcd.clear()
                lcd.write_string("Ugyldig studerende.")
                sleep(3)
                lcd.clear()

        except KeyboardInterrupt:
            break
        

