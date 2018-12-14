import time
from Adafruit_CharLCD import Adafruit_CharLCD
import RPi.GPIO as GPIO
from signal import pause

GPIO.setmode(GPIO.BCM)

t_pk = [{'name':'A','timea': '0'},{'name':'A','timeb':'0'}]


#Ultrasonic Sensor 1
GPIO_TRIGGER_1 = 23 #16
GPIO_ECHO_1 = 24 #18
GPIO.setup(GPIO_TRIGGER_1, GPIO.OUT) #Ultrasonic transmit
GPIO.setup(GPIO_ECHO_1, GPIO.IN) #Ultrasonic receive

vacant = ['A','B'] #All Parkings Available
start_time1=0 #Car sensed by IR sensor
star=0 #Checking if car gets parked in 10sec
car_sensed = False #Car sensed by IR sensor
parkingA=False #Parking A is vacant
parkingB=False #Parking B is vacant
vac = 0 #To display the next available parking lot

#Distance calculated by Ultrasonic
def distance_1():
    GPIO.output(GPIO_TRIGGER_1, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_1, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO_1) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_1) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime

    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


#Ultrasonic Sensor 2
GPIO_TRIGGER_2 = 22 #15
GPIO_ECHO_2 = 27 #13
GPIO.setup(GPIO_TRIGGER_2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_2, GPIO.IN)
 
def distance_2():
    GPIO.output(GPIO_TRIGGER_2, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_2, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO_2) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_2) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

#LCD Code
lcd = Adafruit_CharLCD(rs=26,en=19,d4=13,d5=6,d6=5,d7=11,cols=16,lines=2)
lcd.clear()
lcd.message('Smart Car\n Parking.')
time.sleep(2)
lcd.clear()
lcd.message('Welcome.')
time.sleep(0.5)


#To check if car gets parked in the alloted parking.
def car_arrive():
    dist1 = distance_1()
    dist2 =	 distance_2()

    if car_sensed == True:
        if dist1<10:
            car_sensed
            lcd.message('Car Parked.')
            time.sleep(2)
            lcd.clear()
            lcd.message('Welcome.')
            parkingA=True #car parked in parking A
            #vacant.remove('A')
            car_sensed = False
        
        else:
            parkingA=False

    if dist2<10:
            car_sensed
            lcd.message('Car Parked.')
            time.sleep(2)
            lcd.clear()
            lcd.message('Welcome.')
            parkingB=True #car parked in parking B
            #vacant.remove('B')
            car_sensed = False
        
    else:
            parkingB=False

#To check if car left or not.    
def car_chk():
    global star
    dist1 = distance_1()
    dist2 = distance_2()
    if star > 10: #if car has been in parking more than 10sec
        if dist1 > 10: #if car has not reached or left allocated parking
            if 'A' in vacant:
                pass
            else:
                vacant.append('A')
            star = 0
            print('Car Left.')
    if star > 10: #if car has been in parking more than 10sec
        if dist2 > 10: #if car has not reached or left allocated parking
            if 'B' in vacant:
                pass
            else:
                vacant.append('B')
            star = 0
            print('Car Left.') 
      
    print ("Measured Distance = %.1f cm" % dist)
    time.sleep(1)

#Main Function
if __name__ == '__main__':
    try:
        while True:
            dist1 = distance_1()
            dist2 = distance_2()
            IR_PIN = 17 #Pin 26
            GPIO.setup(IR_PIN, GPIO.IN)

        while True:
                got_something = GPIO.input(IR_PIN) #got nothing
                car_chk()
                vac.sort()
                if got_something:
                    pass
                else:
                    car_sensed = True
                    lcd.clear() 
                    
                    if vacant == []:
                        print ("Parking Full!")
                        lcd.message('Parking Full!')
                    else:
                        vac = str(vacant[0])
                        print (vac)
                        lcd.message('Go to Parking:\n'+vac)
                        start_time1 = time.time()
                        del vacant[0]
                        time.sleep(2)
                        lcd.clear()
                star1 = time.time() - start_time1

                print (vacant)
                #star2 = time.time() - start_time2
                if car_sensed == True:
                    car_arrive()
                
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        lcd.message('Thank You!')
        GPIO.cleanup()

Dict= {name:a, time:start_time}

