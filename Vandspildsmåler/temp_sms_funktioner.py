import boto3 #Værktøj til amazon cloud service
import time
from w1thermsensor import W1ThermSensor, Sensor #Sensor lib
from datetime import datetime, timedelta

sensor1 = W1ThermSensor(Sensor.DS18B20, "012275b99cbf")
sensor2 = W1ThermSensor(Sensor.DS18B20, "012275deaa14")
temp1 = sensor1.get_temperature()
temp2 = sensor2.get_temperature()

client = boto3.client(
    "sns",
    )
def notifikation():
    client.publish(PhoneNumber="+4522481330", Message="Der er registreret vandspild!")

def check_temperatures():
    temp1 = sensor1.get_temperature()
    temp2 = sensor2.get_temperature()
    temp_diff =(temp1 - temp2)
    if temp_diff > 5:
        start_time = datetime.now()
        while True:
            time.sleep(1)
            temp1 = sensor1.get_temperature()
            temp2 = sensor2.get_temperature()
            temp_diff =(temp1 - temp2)
            if temp_diff > 5:
                if (datetime.now() - start_time) > timedelta(seconds=21600):
                    notifikation()
                    time.sleep(43200)
                    break
            else:
                start_time = datetime.now()
while True:
    check_temperatures()
  
    


