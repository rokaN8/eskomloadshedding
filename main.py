import time
import datetime

from classes.lookup import Lookup
from classes.webscraper import Webscraper
from classes.lcddisplay import LCDDisplay

lcd = LCDDisplay()
lcd.lcd_display()

def blank_display(status, now):
    group = 2

    future_list = Lookup.stage_group_lookup(None, 2, group, 3)
    next_displayed = False

    lcd.write("No Remaining", lcd.LCD_LINE_1)
    print("No Loadshedding Remaining Today")
    display_status = "Current Stage: " + str(status)
    print(display_status)
    lcd.write(display_status, lcd.LCD_LINE_2)
    time.sleep(20)

    for future_item in future_list:
        if future_item[0] != now.day:
            if next_displayed == False:
                # next_displayed = True
                next = str(
                    datetime.datetime(now.year, now.month, future_item[0], int(future_item[1].split(":")[0]), 0, 0))

                future_display = "Next: " + future_item[3]
                print(future_display)
                lcd.write(future_display, lcd.LCD_LINE_1)
                print(next)
                lcd.write(next, lcd.LCD_LINE_2)
                time.sleep(7)
            # print(datetime.datetime(now.year, now.month, future_item[0], int(future_item[1].split(":")[0]), 0, 0), future_item[3])

def checker():
    counter = 0
    status = 0  #

    while True:
        group = 2
        sleep_timer_multiplier = 1
        update_time = 10
        if (counter % update_time) == 0:
            status = Webscraper.get_loadshedding_status(None)
            counter = 0
        counter += 1
        list = Lookup.stage_group_lookup(None, status, group, 1)

        now = datetime.datetime.now()
        print("Current status", status)
        if status == 0 or list.__len__() == 0:
            blank_display(status, now)
            return

        if list.__len__() > 0:
            for item in list:
                start_hour = int(item[1].split(":")[0])

                start = datetime.datetime(now.year, now.month, now.day, start_hour, 0, 0)

                tdelta = start - now
                tdelta = tdelta.total_seconds()
                diff = tdelta

                if status == 0 or diff < 0:
                    blank_display(status, now)
                    break
                else:
                    display_status = "Stage: " + str(status)
                    lcd.write(display_status, lcd.LCD_LINE_1)
                    time.sleep(20)
                    print("Time till next loadshedding (minutes):", diff, "at", item[1])

                    m, s = divmod(diff, 60)
                    h, m = divmod(m, 60)
                    hms = "%d:%02d" % (h, m)
                    display_next = "Next at: " + str(start_hour) + ":00"
                    print(display_next)
                    lcd.write(display_next, lcd.LCD_LINE_1)
                    display_countdown = "Countdown: " + hms
                    print(display_countdown)
                    lcd.write(display_countdown, lcd.LCD_LINE_2)
                    '''
                    if diff < 10 and diff > 0:
                        #winsound.MessageBeep(winsound.MB_OK)
                        break
                    '''
        break
        #time.sleep(60*sleep_timer_multiplier)

def main():
    print("Starting Eskom Loadshedding checker")
    checker()
    print("End")
    '''
    items = Lookup.stage_group_lookup(None, 2, 2, 5)
    for item in items:
        print(item)
    '''
    return
    #winsound.Beep(winsound.MB_OK.,100)


if __name__ == "__main__":
    main()
