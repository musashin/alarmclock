from threading import Timer, Lock

__refresh_period_in_s__ = 2


def update_alarms():
    """
    Trigger alarm if required
    :return:
    """
    return False, False

def update_display(alarms_on):
    """
    Update the clock display
    If no alarm is active, the momentary
    snooze button will cause the temperature to be displayed
    In any other situations,the current system time will be displayed
    :return:
    """
    pass

def mainloop():
    """
    Main clock loop
    :return:
    """

    update_display(update_alarms())

    Timer(__refresh_period_in_s__, mainloop).start()



if  __name__ =='__main__':

    t = mainloop()


