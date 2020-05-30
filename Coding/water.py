import RPi.GPIO as GPIO
import datetime
import time
import sqlite3
import atexit

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

trigger = 21
echo = 16
water_level = 1

GPIO.setup(17,GPIO.IN)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

def db_entry(on,off,total,ws):
    conn = sqlite3.connect('/var/www/AWS/AWS_db.db')
    curs = conn.cursor()
    curs.execute("""INSERT INTO History(OnTime,OffTime,TotalTime,WaterSupplied) values((?),(?),(?),(?))""",(on,off,total,ws))
    conn.commit()
    conn.close()
    
def water_supplied():
    conn = sqlite3.connect('/var/www/AWS/AWS_db.db')
    curs = conn.cursor()
    curs.execute("select ROUND(CAST(SUM(WaterSupplied) AS FLOAT)/1000,1) from History where date(OffTime) = date('now')")
    ws = curs.fetchone()
    ws = str(ws)
    ws = ws.replace('(',"")
    ws = ws.replace(',)',"")
    ws = ws + ' ℓ'
    print(ws)
    conn.commit()
    conn.close()
    return ws

def history_table():
    conn = sqlite3.connect('/var/www/AWS/AWS_db.db')
    curs = conn.cursor()
    curs.execute("select * from History order by SrNo desc")
    db_contents = curs.fetchall()
    print (db_contents)
    conn.commit()
    conn.close()
    return db_contents
    
def last_water():
    conn = sqlite3.connect('/var/www/AWS/AWS_db.db')
    curs = conn.cursor()
    curs.execute("select OffTime from History where SrNo = (select max(SrNo) from History)")
    lw = curs.fetchone()
    lw = str(lw)
    lw = lw.replace("('","")
    lw = lw.replace("',)","")
    conn.commit()
    conn.close()
    return lw

def pump_on():
    print("Dry")
    GPIO.output(27,GPIO.LOW)

def pump_off():
    print("Wet")
    GPIO.output(27,GPIO.HIGH)
	
def soil_status():
    return GPIO.input(17)

def water_once():
    GPIO.output(27,GPIO.LOW)
    time.sleep(5)
    GPIO.output(27,GPIO.HIGH)
    
def water_level_check():
    trigger = 21
    echo = 16
    strt = 0
    endt = 0
    GPIO.output(trigger,True)
    time.sleep(0.00001)
    GPIO.output(trigger,False)
    print ("Hello")
    while GPIO.input(echo)==0:
        # print ("Hello1")
        strt = time.time()
            
    while GPIO.input(echo)==1:
        # print ("Hello2")
        endt = time.time()
            
    tof = endt - strt
        
    distance = (tof * 34300.0) / 2.0
        
    distance = round(distance,2)
    #print ("Object distance = ",distance," cm")
    return distance

def auto_water():
    GPIO.output(27,GPIO.HIGH)
    a = 0
    
    #for i in range(10):
    while 0 < 1:
        distance = water_level_check()
        print ("Object distance = ",distance," cm")
        if distance < 17:
            water_level = 1
            if GPIO.input(17):
                pump_on()
                if a == 0:
                    f_on = open("pump_on_time.txt","w")
                    f_on.write("{}".format(datetime.datetime.today().replace(microsecond=0)))
                    
                    pump_on_time = time.time()
                    
                    f_on = open("pump_on_time.txt","r")
                    db_pump_on = f_on.readline()
                    print(db_pump_on)
                    f_on.close()
                    a=1
            else:
                pump_off()
                if a == 1:
                    f_off = open("pump_off_time.txt","w")
                    f_off.write("{}".format(datetime.datetime.today().replace(microsecond=0)))
                    
                    pump_off_time = time.time()
                    
                    f_off = open("pump_off_time.txt","r")
                    db_pump_off = f_off.readline()
                    print(db_pump_off)
                    
                    total_time = int(pump_off_time) - int(pump_on_time)
                    print (total_time)
                    
                    water_supplied = round((total_time/65)*1000)
                    
                    
                    f_off.close()
                    a=0
                    
                    db_entry(db_pump_on,db_pump_off,total_time,water_supplied)
            #time.sleep(1)
        else:
            print ("No Water")
            GPIO.output(27,GPIO.HIGH)
            water_level = 0
        time.sleep(1)
    GPIO.output(27,GPIO.HIGH)
    
def clean():
    print("Exiting")
    GPIO.output(27,GPIO.HIGH)
    
atexit.register(clean)




