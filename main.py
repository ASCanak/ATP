import time, curses
from ctypes import *

cmodule = CDLL('./clibrary.so')

# Defining c-types of readTemperature(None) -> float {};
cmodule.readTemperature.restype = c_float

# Defining c-types of readLightLevel(None) -> float {};
cmodule.readLightLevel.restype  = c_float

# Defining c-types of getStatus(None) -> bool {} from the Rolluik class;
cmodule.Rolluik_getStatus.restype = c_bool

# Defining c-types of getStatus(None) -> bool {} from the Koeler class;
cmodule.Koeler_getStatus.restype = c_bool

class Ochtendwekker:
    def __init__(self):
        self.alarmSet      = False
        self.nextAlarm     = -1
        self.time          = 0
        self.lightLevel    = None
        self.shutterClosed = cmodule.Rolluik_getStatus()

    def setAlarm(self, hours):
        if hours > 0:
            self.alarmSet  = True
            self.nextAlarm = hours

    def update(self): # Het wijzigen/opvragen van data uit de logic gehaald zodat het testbaar is.
        self.time          = self.time + 1 if self.time < 23 else 0
        self.lightLevel    = round(cmodule.readLightLevel(), 1)
        self.shutterClosed = cmodule.Rolluik_getStatus()

        if self.alarmSet and (self.nextAlarm > 0): self.nextAlarm -= 1 
        else: self.alarmSet = False

        if self.logic(self.shutterClosed, self.alarmSet, self.nextAlarm, self.lightLevel):
            self.alarmSet = False
            cmodule.Rolluik_open()

    @staticmethod # Pure function that doesn't require class instance.
    def logic(shutterClosed, alarmSet, nextAlarm, lightLevel):
        if shutterClosed and alarmSet and nextAlarm <= 1 and lightLevel >= 100:
            return True
        return False

class Thermostaat: #Thermostaat met alleen een Koelunit geen Verwarmunit.
    def __init__(self, desiredTemp = 23.0):
        self.actualTemp  = round(cmodule.readTemperature(), 1)
        self.desiredTemp = 23.0
        self.coolerOn = cmodule.Koeler_getStatus()

    def setDesiredTemp(self, offset):
        self.desiredTemp += offset

    def update(self): # Het wijzigen/opvragen van data uit de logic gehaald zodat het testbaar is.
        self.actualTemp = round(cmodule.readTemperature(), 1)
        self.coolerOn = cmodule.Koeler_getStatus()
        
        result = self.logic(self.actualTemp, self.desiredTemp, self.coolerOn)
        
        if result == "start":
            cmodule.Koeler_start()
        elif result == "stop":
            cmodule.Koeler_stop()

    @staticmethod # Pure function that doesn't require class instance.
    def logic(actualTemp, desiredTemp, coolerOn):
        if coolerOn:
            if actualTemp < desiredTemp - 1.0: # -1.0 is a buffer so it doesn't constantly switch.
                return "stop"        
        else: 
            if actualTemp > desiredTemp + 1.0: # +1.0 is a buffer so it doesn't constantly switch.
                return "start"
        return "none"

if __name__ == "__main__":
    wekker = Ochtendwekker()
    thermostaat = Thermostaat()

    def simulator_loop(stdscr):
        stdscr.nodelay(1)  # Set non-blocking mode
        while True:
            stdscr.clear()
            
            wekker.update()
            thermostaat.update()
            
            stdscr.addstr("\nWekker Module\n")
            stdscr.addstr("--------------------------------------------------------------------------------------------------\n")
            stdscr.addstr("It's currently {}:00, ".format(wekker.time))
            
            if wekker.alarmSet: stdscr.addstr("The next alarm is in {} hours\n".format(wekker.nextAlarm))
            else:               stdscr.addstr("Alarm unavailable | Press '6' for an alarm\n")

            if cmodule.Rolluik_getStatus(): stdscr.addstr("The roller shutters are closed\n")   
            else:                           stdscr.addstr("The roller shutters are opened | Press 'c' to close\n") 

            stdscr.addstr("Current light level is {} Lux | Desired light level is 100 Lux\n".format(wekker.lightLevel))            
            
            stdscr.addstr("\nThermostaat Module\n")
            stdscr.addstr("--------------------------------------------------------------------------------------------------\n")
            stdscr.addstr("Press '-' to lower desired temp by 0.5 °C | Press '+' to increase desired temp by 0.5 °C\n")
            stdscr.addstr("Current temperature is {} °C  | Desired temperature is {} °C\n".format(thermostaat.actualTemp, thermostaat.desiredTemp))

            if cmodule.Koeler_getStatus(): stdscr.addstr("The cooler is on\n")   
            else:                          stdscr.addstr("The cooler is off\n") 

            # Check for keyboard input
            ch = stdscr.getch()
            if ch != curses.ERR:
                if ch == ord('6'):
                    wekker.setAlarm(6)
                if ch == ord('c'):
                    cmodule.Rolluik_close()
                if ch == ord('-'):
                    thermostaat.setDesiredTemp(-0.5)
                if ch == ord('+'):
                    thermostaat.setDesiredTemp(0.5)
            
            stdscr.refresh()

            time.sleep(1)
    
    curses.wrapper(simulator_loop)