# Importerer et lib, der kan kommunikere med mysql
import mysql.connector
import time
from w1thermsensor import W1ThermSensor, Sensor
# Variablerne defineres her
location2 = "Rør"
location = "Luft"

while True:
        sensor1 = W1ThermSensor(Sensor.DS18B20, "012275b99cbf")
        sensor2 = W1ThermSensor(Sensor.DS18B20, "012275deaa14")
        temp1 = sensor1.get_temperature()
        temp2 = sensor2.get_temperature()
        temp_diff =(temp1 - temp2)
        if temp_diff > 5:
#database connection
                connection = mysql.connector.connect(host="79.171.148.146",user="kim",passwd="wB@L.hwe6RgQh]H[",database="Test" )
#Indsætter values i tables. %s er variabler, da de ikke kan indsættes normalt, da sql ikke kan læse dem.
                insertStatement =(
    "INSERT INTO SensorData(sensor,sensor2, Location,Location2,value1,value2)" "VALUES (%s, %s, %s, %s, %s,%s)"
)
    # Igen er det variabler, der indsætte istedet for %s ovenover. De skal passe numerisk.
                data = ("012275b99cbf","012275deaa14",location,location2,temp1,temp2)
                cursor = connection.cursor()
#Executer insertstatement
                cursor.execute(insertStatement,data)
#Ændringerne i databasen gemmes.    
                connection.commit()
#Row variablen bruges til at gemme resultaterne af sql quaryen    
                rows = cursor.fetchall()
                cursor.close()
  
                time.sleep(10)

