#initialization
import RPi.GPIO as GPIO
import time
import schedule
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
soil_in = 21  #PIN for reading soil moisture
soil_out = 18 #PIN for turning on/off soil moisture sensor
motor = 20    #PIN for water pump

#setting up PINS
GPIO.setup(soil_out,GPIO.OUT) 
GPIO.setup(soil_in,GPIO.IN)
GPIO.setup(motor,GPIO.OUT)
GPIO.output(motor,1)


#logging 
print("---Starting the program---")
temp_time = datetime.datetime.now() #current time
temp_str = temp_time.strftime('%Y/%m/%d %H:%M:%S') #time to string
with open('water_log.txt','a') as file_object: 
    file_object.write("Program Started: "+temp_str+"\n")

#User input
lim = int(input("What is the limit for sucsessive watering?"))
freq = int(input("How often do you want to check the soil?(Hour):"))

#reads soil moisture sensor Dry:1 Wet:0
def read_moisture():
    GPIO.output(soil_out,1)
    time.sleep(5)
    moisture = GPIO.input(soil_in)
    #for sensor testing 
    """
    if(moisture): #soil is dry when sensor is 1 wet when 0
        print('Soil is dry.')
    else:
        print('Soil is wet.')
    """
    GPIO.output(soil_out,0)
    return moisture

#gives water for 10 seconds (default)
def water(seconds=10):
    GPIO.output(motor,0)
    time.sleep(seconds)
    GPIO.output(motor,1)

#process to be repeatedly executed
#limit: maximum successive  watering
def process(limit = lim): 
    moisture =read_moisture()
    temp_time = datetime.datetime.now()
    temp_str = temp_time.strftime('%Y/%m/%d %H:%M:%S')
    if(moisture):
        with open('water_log.txt', 'a') as file_object:
            file_object.write("WATERED:"+temp_str+"\n")
    count = 0 #counts number of consecutive watering 
    while(moisture):
        if(count>=limit):
            time.sleep(15)
            return
        elif (not moisture):
            return
        water()
        moisture = read_moisture()
        count = count + 1


#program starting time
temp_time = datetime.datetime.today()
print(temp_time)
schedule.every(freq).hours.do(process)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
GPIO.cleanup()

